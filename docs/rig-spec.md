# Marmalade — Rive Rig Specification v1

Status: **rig-feasibility plan; implementation waits for character approval**.

## Artboard and coordinate system

- Master Rive artboard: `Marmalade_Main`, 1024 × 1024 logical units.
- Neutral floor line: `y=846`; character centerline: `x=512`.
- Root origin: `(512, 846)` at the neutral contact point between the front paws.
- Positive rotation is clockwise. Transform origins are expressed in neutral artboard coordinates.
- Author clean vector fills with local, single-piece shading. Use clipping masks for cream patches and inner-ear color only.

## Hierarchy

```text
cat_root
├── shadow_local
├── body_group
│   ├── torso
│   ├── chest_patch
│   └── belly_patch
├── rear_legs
│   ├── left_thigh → left_lower_leg → left_rear_paw
│   └── right_thigh → right_lower_leg → right_rear_paw
├── tail_rig
│   └── tail_base → tail_1 → tail_2 → tail_3 → tail_tip
├── front_legs
│   ├── left_upper_front → left_lower_front → left_paw
│   └── right_upper_front → right_lower_front → right_paw
├── head_group
│   ├── head_base
│   ├── left_ear / right_ear
│   ├── inner_ears
│   ├── eye_whites
│   ├── pupils
│   ├── lower_eyelids
│   ├── upper_eyelids
│   ├── muzzle
│   ├── nose
│   ├── mouth
│   └── left_whiskers / right_whiskers
└── accessories
    ├── birthday_hat
    ├── optional_ribbon
    └── prop_anchors
```

## Pivot map

Coordinates are the neutral starting points; final vector art may move a pivot by at most 8 units to match a contour.

| Pivot | Coordinate | Rotation envelope |
|---|---:|---:|
| Neck | `(512, 360)` | −28°…+28° |
| Left / right ear | `(430, 226)` / `(594, 226)` | −22°…+30° |
| Left / right shoulder | `(445, 500)` / `(579, 500)` | −75°…+80° |
| Elbows | `(430, 625)` / `(594, 625)` | 0°…125° |
| Wrists | `(426, 747)` / `(598, 747)` | −28°…+35° |
| Hips | `(438, 650)` / `(586, 650)` | −45°…+55° |
| Knees | `(420, 735)` / `(604, 735)` | 0°…115° |
| Rear paws | `(412, 824)` / `(612, 824)` | −24°…+28° |
| Tail base | `(642, 646)` | −85°…+80° |
| Tail joints | `(714, 612)`, `(780, 548)`, `(802, 464)` | ±55°, ±48°, ±42° |
| Hat anchor | `(512, 170)` | follows head + 18% lag |

## Layer order, back to front

`shadow_local`, far tail, far rear leg, far front leg, torso, belly, chest, near rear leg, near front leg, head, far ear, near ear, eye whites, pupils, lower lids, upper lids, muzzle, mouth, nose, whiskers, hat/ribbon, foreground paw override.

For hanging and scratching, use keyed draw-order swaps rather than duplicated full characters. The gripping paw may move to `foreground paw override`; the arm remains in its original branch.

## Deformation and masks

- Bone-rig torso, limbs, head and tail. Use meshes only on torso squash, cheek/muzzle, shoulder joins and tail silhouette.
- Torso mesh: 5 × 6 vertices; lock outer shoulder and hip columns to their nearest bones.
- Head mesh: 5 × 5; deform only cheeks and crown by ≤6%. Eyes, nose and markings remain child transforms.
- Tail: one continuous 4-segment mesh, 18–22 vertices along each edge; bind bands to the same weights.
- Cream chest and belly are clipping children of torso. Paw-tip cream is clipped inside each paw, never a separate floating piece.
- Eyelids mask the eye whites and pupils. Pupils translate inside an inset eye mask.
- Do not mesh whiskers; use transform groups with subtle scale and rotation.

## Prop anchors

`paw_l_grip`, `paw_r_grip`, `mouth_hold`, `nose_focus`, `head_top`, `back_saddle`, `tail_tip_fx`, and `floor_contact`. Yarn, toy, paper and note remain scene-level objects; attach via constraints only during contact beats.

## State machine contract

Main machine: `Marmalade_Main` with nested machines `Body_Action`, `Face_Reaction`, `Tail_Behavior`, `Accessories`, `Prop_Interaction`.

Boolean inputs: `showCat`, `isIdle`, `isPeeking`, `isWalking`, `isPlaying`, `isChasing`, `isScratching`, `isPulling`, `isHanging`, `isSwinging`, `isCurling`, `isSleeping`, `isWaking`, `isExcited`, `isParty`, `hasHat`.

Number inputs: `scrollProgress`, `lookX`, `lookY`, `moveSpeed`, `swingAmount`, `energy`, `blinkRate`, `tailMood`, `breathIntensity`.

Triggers: `peekIn`, `startWalk`, `startPlay`, `pounce`, `scratchStart`, `pullReveal`, `hangDrop`, `startSwing`, `curlDown`, `fallAsleep`, `wakeUp`, `celebrate`, `hatDrop`, `partyBurst`.

## Transition policy

- Micro reactions: 0.20–0.30 s.
- Ordinary action changes: 0.35–0.55 s.
- Cinematic body changes: 0.60–0.90 s.
- Preserve ear and tail additive motion during every blend.
- Disable inactive prop constraints and offscreen loops.
- No state may snap draw order, root scale, eye direction or tail pose.

## Rig feasibility gate

The model sheet supports the required silhouette and fixed markings, but final rig art must be redrawn as separated vectors. Before animation production, verify: clean shoulder overlap at ±70°, cream masks through torso squash, tail-band stability through 90° curl, pupil limits at all gaze extremes, and gripping-paw draw-order swaps.
