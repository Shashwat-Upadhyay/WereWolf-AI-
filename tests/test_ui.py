import pytest
from ui import GameUI

def test_ui_headless_init(mock_tkinter):
    ui = GameUI(mock_tkinter.Tk())
    # Verify standard UI initialization without crashing
    assert ui.engine is not None
    assert mock_tkinter.Tk().winfo_width() == 1000

def test_ui_next_phase(mock_tkinter):
    ui = GameUI(mock_tkinter.Tk())
    # Should kick off animations
    ui.next_phase()
    assert ui.is_busy is True
    assert len(ui.script) > 0
    
    # Process a small step to spawn the first animation
    ui._process_script(0.1)
    assert len(ui.animations.animations) > 0
    
def test_ui_animation_no_recursion(mock_tkinter):
    ui = GameUI(mock_tkinter.Tk())
    ui.next_phase()
    
    # Process the entire animated sequence in a loop to ensure no infinite recursion
    # If it exceeds a massive number of steps, there's a problem
    loops = 0
    while ui.is_busy and loops < 10000:
        ui._process_script(0.1)
        ui.animations.update(ui, 0.1)
        loops += 1
        
    assert loops < 10000
    assert ui.is_busy is False
