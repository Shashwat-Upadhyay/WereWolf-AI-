import pytest
from engine import Detective, GameEngine
from models import Phase, Role

def test_phase_transitions(game_state):
    """Verifies that the game moves from Day to Night and increments the day number."""
    engine = game_state(8)
    assert engine.phase == Phase.DAY
    assert engine.day_number == 1

    # Advance to Night
    events = engine.advance_phase()
    if engine.winner is None:
        assert engine.phase == Phase.NIGHT
        
    # Advance back to Day
    if engine.winner is None:
        events = engine.advance_phase()
        if engine.winner is None:
            assert engine.phase == Phase.DAY
            assert engine.day_number == 2

def test_winner_detection(game_state):
    """Tests winning conditions for both Village and Werewolves."""
    engine = game_state(8)
    wolves = [pid for pid, p in engine.players.items() if p.role == Role.WEREWOLF]
    villagers = [pid for pid, p in engine.players.items() if p.role != Role.WEREWOLF]

    # Test Village Win: Kill all wolves
    for pid in wolves:
        engine.players[pid].is_alive = False
    assert engine.check_winner() == "Village"

    # Test Werewolf Win: Kill all but one villager and one wolf
    for p in engine.players.values():
        p.is_alive = False
    engine.players[wolves[0]].is_alive = True
    engine.players[villagers[0]].is_alive = True
    assert engine.check_winner() == "Werewolves"

def test_day_tie_vote_elimination(game_state):
    """Verifies that a tie in voting still results in an elimination from the tied pool."""
    engine = game_state(8)
    alive = engine.living_ids()
    target_a, target_b = alive[0], alive[1]

    # Force a 50/50 split vote using the engine's AI interface
    for i, voter in enumerate(alive):
        target = target_a if i % 2 == 0 else target_b
        engine.ai[voter].vote = lambda _e, t=target: t

    events = engine.advance_phase()
    
    # Check that one of the targets was eliminated
    eliminated = next((e.payload["eliminated"] for e in events if e.kind == "elimination"), None)
    assert eliminated in [target_a, target_b]
    assert not engine.players[eliminated].is_alive

def test_night_actions_doctor_and_detective(game_state):
    """Tests that the Doctor can save a victim and the Detective successfully scans a player."""
    engine = game_state(8, random_seed=42)
    engine.phase = Phase.NIGHT

    # Identify roles
    wolf = next(pid for pid, p in engine.players.items() if p.role == Role.WEREWOLF)
    doc = next(pid for pid, p in engine.players.items() if p.role == Role.DOCTOR)
    det = next(pid for pid, p in engine.players.items() if p.role == Role.DETECTIVE)
    victim = next(pid for pid, p in engine.players.items() if p.role == Role.VILLAGER and pid != doc)
    scan_target = next(pid for pid in engine.living_ids() if pid not in (det, victim))

    # Mock actions
    engine.ai[wolf].night_action = lambda _e: victim
    engine.ai[doc].night_action = lambda _e: victim
    engine.ai[det].night_action = lambda _e: scan_target

    # Assert Detective is the correct class and track their memory
    det_brain = engine.ai[det]
    assert isinstance(det_brain, Detective)

    events = engine.advance_phase()

    # Verify outcomes
    assert engine.players[victim].is_alive  # Saved by Doctor
    assert scan_target in det_brain.investigated  # Scanned by Detective
    assert any(e.payload.get("tag") == "save" for e in events)

def test_empty_game_state_safety(game_state):
    """Ensures the engine handles edge cases like 0 players without crashing."""
    engine = game_state(4)
    for p in engine.players.values():
        p.is_alive = False
    assert engine.check_winner() is not None
