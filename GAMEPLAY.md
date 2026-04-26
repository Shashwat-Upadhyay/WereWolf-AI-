# Gameplay

## Roles
- **Villager**: no night action
- **Werewolf**: coordinates attacks and deception
- **Doctor**: protects one target at night
- **Detective**: investigates one target at night

## Phase cycle

### Day
- Living players speak
- Everyone votes
- Highest-voted player is eliminated (ties are randomly resolved)
- Eliminated role is revealed
- Winner check runs

### Night
- Werewolves choose a target
- Doctor chooses a protection target
- Detective scans a target
- Night elimination resolves unless protected
- Winner check runs, then transition back to day

## Win conditions
- **Village wins**: all werewolves are eliminated
- **Werewolves win**: werewolves are equal to or outnumber good players

## AI behavior summary
- Suspicion and trust values are tracked per opponent
- Dialogue and voting outcomes adjust those values
- Role-specific heuristics drive vote and night decisions
