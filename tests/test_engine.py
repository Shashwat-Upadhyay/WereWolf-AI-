import pytest
from models import Phase, Role

def test_phase_transition(game_state):
    engine = game_state(8)
    assert engine.phase == Phase.DAY
    assert engine.day_number == 1
    
    # Run Day
    events = engine.advance_phase()
    assert any(e.kind == "phase_transition" for e in events) or engine.winner is not None
    if engine.winner is None:
        assert engine.phase == Phase.NIGHT
        
    # Run Night
    if engine.winner is None:
        events = engine.advance_phase()
        assert any(e.kind == "phase_transition" for e in events) or engine.winner is not None
        if engine.winner is None:
            assert engine.phase == Phase.DAY
            assert engine.day_number == 2

def test_doctor_save(game_state):
    engine = game_state(8, random_seed=42)
    # Force roles
    wolves = []
    doctor = None
    villager = None
    for pid, p in engine.players.items():
        if p.role == Role.WEREWOLF: wolves.append(pid)
        elif p.role == Role.DOCTOR: doctor = pid
        elif p.role == Role.VILLAGER: villager = pid

    if not doctor or not wolves or not villager:
        pytest.skip("Could not find required roles in random permutation")
        
    engine.phase = Phase.NIGHT
    
    # Patch AI to force the save
    class MockWolfBrain:
        def night_action(self, e): return villager
    
    class MockDoctorBrain:
        def night_action(self, e): return villager
        
    for w in wolves:
        engine.ai[w].night_action = MockWolfBrain().night_action
    engine.ai[doctor].night_action = MockDoctorBrain().night_action
    
    events = engine.advance_phase()
    
    # The villager should be alive
    assert engine.players[villager].is_alive
    save_events = [e for e in events if e.payload.get("tag") == "save"]
    assert len(save_events) > 0

def test_game_over_0_players(game_state):
    engine = game_state(8)
    # Kill everyone
    for p in engine.players.values():
        p.is_alive = False
    
    # Shouldn't crash
    winner = engine.check_winner()
    assert winner is not None

def test_game_over_1_player(game_state):
    engine = game_state(6)
    # Kill everyone except 1 wolf
    wolf = None
    for pid, p in engine.players.items():
        if p.role == Role.WEREWOLF and not wolf:
            wolf = pid
        else:
            p.is_alive = False
            
    winner = engine.check_winner()
    assert winner == "Werewolves"
