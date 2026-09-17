# Marmalade — Animation Bible v1

Status: **only the four-state foundation is implemented**: Idle, Peeking, Looking, Walking (walk/trot blend), plus additive channels and Gentle/Focused/Mischievous expressions. Current timings and input ranges are in `rig-spec.md`. The table below remains the broader 16-state plan; the other twelve actions are NOT implemented.

All durations assume 60 fps design timing. Scroll-scrubbed actions use normalized progress `0…1` and must reverse cleanly. Additive blink, ears, gaze, breathing and tail layers continue unless a state explicitly overrides them.

| State | Type | Duration / cycle | Essential beats |
|---|---|---:|---|
| Idle | loop | 4.8 s | breath, slow head drift, tail sway, random ear twitch, blink |
| Peeking | one-shot + hold | 1.4 s | ears, eyes, head rise, paws grip, head tilt |
| Looking around | reactive loop | input-driven | pupils lead head; ears counter-track; `lookX/Y` clamped |
| Walking | loop | 0.9 s slow / 0.56 s trot | four-beat gait, head bob, torso bounce, tail counter-motion |
| Yarn play | variable loop | 2.1–3.0 s | track yarn, paw bats, body lean, tail flick, tiny hop |
| Pounce | one-shot | 1.15 s | crouch, launch, full extension, landing, recovery |
| Scratching | loop | 0.82 s | alternating reach, shoulder compression, focused face |
| Paper pull / tear | scroll | progress-driven | grip, brace, pull, resistance, tear, recoil |
| Hanging | loop + hold | 2.6 s | fixed paws, body hang, small bicycle legs, tail droop, blink |
| Swinging | loop | 2.8 s | pendulum, body lag, ear follow-through, tail secondary motion |
| Curling down | one-shot | 1.6 s | lower body, tuck paws, wrap tail, settle head |
| Sleeping | loop | 5.2 s | closed eyes, slow breath, dream twitch, rare ear movement |
| Waking | one-shot | 2.4 s | one eye, head lift, yawn, stretch, arch, sit |
| Excited | loop | 1.15 s | bounce, paw taps, tail flick, wide eyes, smile |
| Celebration | loop | 1.35 s | alternating paw wave, bounce, expressive party tail |
| Hat drop / hero | one-shot → loop | 1.55 s + 1.35 s | hat falls, surprise, settle, smile, wave, hero hold |

## Key pose timing

### Peeking

- `0.00–0.18`: hidden hold; ear tips break the edge.
- `0.18–0.42`: eyes and crown rise, pupils scan.
- `0.42–0.68`: paws land with 2-frame compression.
- `0.68–0.88`: head clears edge and overshoots 4°.
- `0.88–1.00`: settle into curious tilt; hold remains gaze-reactive.

### Pounce

- `0.00–0.24`: anticipation crouch; tail draws opposite action.
- `0.24–0.44`: explosive launch; 12% stretch.
- `0.44–0.66`: airborne extension; pupils stay on target.
- `0.66–0.80`: landing; paws contact 2 frames before body compression.
- `0.80–1.00`: rebound and curious recovery.

### Paper pull / tear

- `0.00–0.22`: acquire paper and set both grips.
- `0.22–0.54`: three resistance pulses, each smaller than the last.
- `0.54–0.72`: shoulder and back brace; paper fibers begin separating.
- `0.72–0.84`: tear release and 7% recoil.
- `0.84–1.00`: surprise blink, then look at revealed message.

### Curl to sleep

- `0.00–0.30`: lower torso and fold front paws.
- `0.30–0.62`: rotate hips, tuck rear legs, tail begins wrap.
- `0.62–0.84`: head settles onto paws, lids close.
- `0.84–1.00`: two settling breaths blend into sleep loop.

## Additive systems

- **Blink:** normal 110 ms close / 85 ms open; slow 210/240; sleepy 310/360; surprised 65/95. Randomize idle intervals from 2.8–6.2 s.
- **Gaze:** pupils move first within ±11% eye width and ±8% height; head follows after 90 ms; ear nearest target perks after another 70 ms.
- **Ears:** `left twitch`, `right twitch`, `perk`, `relaxed`; never fire both random twitches simultaneously.
- **Tail moods:** calm sway, curious curl, alert, excited flick, hanging drop, sleep wrap, party wag.
- **Breathing:** 0.8–2.5% torso scale; sleeping breath uses slower 4.6–5.4 s cycles.
- **Face:** neutral, curious, happy, mischief, sleepy, surprised, excited. Expressions blend with action states rather than replace them.

## Scroll integration

Scrub `Peeking`, yarn reveal/pounce setup, `Paper pull / tear`, hanging entry, curl-down and finale reveal. Loops run only while the owning scene is active. Forward scroll advances; reverse scroll restores the previous physical pose. One-shot triggers may emit sound/particles only on forward threshold crossings and must not replay while scrubbing backward.

## Foundation test set

Implement only Idle, Peeking, Looking around and Walking in the first Rive prototype. Acceptance: no identity drift, no visible seams, transitions at 60 fps on a mid-range mobile device, reverse-safe peek, stable gaze, and clean idle-to-walk blend. Only then build the remaining states.
