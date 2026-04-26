import pytest
from engine import GameEngine
import tkinter as tk

@pytest.fixture
def game_state():
    """Returns a factory function to create a configured GameEngine instance."""
    def _create_engine(num_players=8, random_seed=None):
        if random_seed is not None:
            import random
            random.seed(random_seed)
        engine = GameEngine(num_players)
        return engine
    return _create_engine

@pytest.fixture
def mock_tkinter(mocker):
    """Mocks out the Tkinter framework for headless UI tests."""
    mock_tk = mocker.patch("ui.tk")
    mock_tk.Tk.return_value = mocker.MagicMock()
    mock_tk.Tk.return_value.winfo_width.return_value = 1000
    mock_tk.Tk.return_value.winfo_height.return_value = 720
    
    mock_canvas = mocker.MagicMock()
    mock_canvas.winfo_width.return_value = 1000
    mock_canvas.winfo_height.return_value = 720
    mock_canvas.bbox.return_value = (0, 0, 100, 100)
    mock_tk.Canvas.return_value = mock_canvas
    
    # Mock specific tkinter constants used in codebase
    mock_tk.LEFT = "left"
    mock_tk.RIGHT = "right"
    mock_tk.BOTH = "both"
    mock_tk.X = "x"
    mock_tk.Y = "y"
    mock_tk.END = "end"
    mock_tk.NORMAL = "normal"
    mock_tk.DISABLED = "disabled"
    mock_tk.FLAT = "flat"
    mock_tk.CENTER = "center"
    mock_tk.LAST = "last"
    mock_tk.HIDDEN = "hidden"
    
    # Mock PhotoImage properly so it doesn't crash
    mock_photo = mocker.MagicMock()
    mock_photo.width.return_value = 100
    mock_photo.height.return_value = 100
    mock_photo.zoom.return_value = mock_photo
    mock_photo.subsample.return_value = mock_photo
    mock_tk.PhotoImage.return_value = mock_photo
    
    return mock_tk
