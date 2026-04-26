import pytest
from engine import AIPlayer, Villager

@pytest.mark.parametrize("trust_val,suspicion_val,dialogue_kind,expected_clamped", [
    (0.0, 0.5, "accuse", 0.5),    # if trust is 0, add 0.08 * 0 = 0
    (1.0, 0.5, "accuse", 0.58),   # if trust is 1, add 0.08 * 1 = 0.08
    (0.5, 0.5, "defend", 0.53),   # defend adds 0.03
    (0.5, 0.98, "accuse", 1.0),   # clamping at 1.0 max
])
def test_ai_observe_dialogue(game_state, trust_val, suspicion_val, dialogue_kind, expected_clamped):
    engine = game_state(8)
    ai = engine.ai[1]
    speaker_id = 2
    target_id = 3
    
    # Setup state
    ai.trust[speaker_id] = trust_val
    if dialogue_kind == "defend":
        # defense modifies speaker's suspicion
        ai.suspicion[speaker_id] = suspicion_val
    else:
        ai.suspicion[target_id] = suspicion_val
        
    from models import Dialogue
    d = Dialogue(speaker_id=speaker_id, target_id=target_id if dialogue_kind != "defend" else None, text="test", kind=dialogue_kind)
    
    ai.observe_dialogue(d, engine)
    
    if dialogue_kind == "defend":
        assert abs(ai.suspicion[speaker_id] - expected_clamped) < 0.001
    else:
        assert abs(ai.suspicion[target_id] - expected_clamped) < 0.001

def test_ai_0_alive_interactions(game_state):
    engine = game_state(8)
    # Kill everyone except player 1
    for pid, p in engine.players.items():
        if pid != 1:
            p.is_alive = False
            
    # Shouldn't crash and should vote self or throw no errors calculating dialogue
    d = engine.ai[1].make_day_dialogue(engine)
    v = engine.ai[1].vote(engine)
    
    assert d is not None
    assert v == 1
