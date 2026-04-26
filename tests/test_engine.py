import random
import unittest

from engine import Detective, GameEngine
from models import Phase, Role


class GameEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(42)

    def test_phase_transitions_day_to_night_to_day(self) -> None:
        game = GameEngine(8)
        self.assertEqual(game.phase, Phase.DAY)

        game.advance_phase()
        if game.winner is None:
            self.assertEqual(game.phase, Phase.NIGHT)
            day_before_night = game.day_number
            game.advance_phase()
            if game.winner is None:
                self.assertEqual(game.phase, Phase.DAY)
                self.assertEqual(game.day_number, day_before_night + 1)

    def test_winner_detection_for_both_teams(self) -> None:
        game = GameEngine(8)
        wolf_ids = [pid for pid, player in game.players.items() if player.role == Role.WEREWOLF]
        good_ids = [pid for pid, player in game.players.items() if player.role != Role.WEREWOLF]

        for pid in wolf_ids:
            game.players[pid].is_alive = False
        self.assertEqual(game.check_winner(), "Village")

        for player in game.players.values():
            player.is_alive = False
        for pid in wolf_ids:
            game.players[pid].is_alive = True
        game.players[good_ids[0]].is_alive = True
        self.assertEqual(game.check_winner(), "Werewolves")

    def test_day_tie_vote_eliminates_one_of_tied_players(self) -> None:
        game = GameEngine(8)
        alive = game.living_ids()
        tied_targets = [alive[0], alive[1]]

        for index, voter in enumerate(alive):
            target = tied_targets[index % 2]
            game.ai[voter].vote = (lambda _engine, t=target: t)

        game.advance_phase()
        death_events = [entry for entry in game.timeline if entry["phase"] == Phase.DAY.value]
        self.assertTrue(death_events)
        day_entry = death_events[-1]
        self.assertIn(day_entry["eliminated"], tied_targets)
        self.assertFalse(game.players[day_entry["eliminated"]].is_alive)

    def test_night_doctor_save_and_detective_scan(self) -> None:
        game = GameEngine(8)
        game.phase = Phase.NIGHT

        wolf_id = next(pid for pid, player in game.players.items() if player.role == Role.WEREWOLF)
        doctor_id = next(pid for pid, player in game.players.items() if player.role == Role.DOCTOR)
        detective_id = next(pid for pid, player in game.players.items() if player.role == Role.DETECTIVE)
        victim_id = next(
            pid
            for pid, player in game.players.items()
            if player.role == Role.VILLAGER and pid not in (doctor_id, detective_id, wolf_id)
        )
        scan_target = next(pid for pid in game.living_ids() if pid not in (detective_id, victim_id))

        game.ai[wolf_id].night_action = lambda _engine: victim_id
        game.ai[doctor_id].night_action = lambda _engine: victim_id
        game.ai[detective_id].night_action = lambda _engine: scan_target

        detective_brain = game.ai[detective_id]
        self.assertIsInstance(detective_brain, Detective)
        game.advance_phase()

        self.assertTrue(game.players[victim_id].is_alive)
        self.assertIn(scan_target, detective_brain.investigated)


if __name__ == "__main__":
    unittest.main()
