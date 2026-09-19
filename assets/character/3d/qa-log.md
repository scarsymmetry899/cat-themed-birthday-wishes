# Marmalade 3D QA log

## 2026-09-19 — production checkpoint v02

### Geometry

- Source audit: one fused 1,908,002-face mesh; no armature or shape keys.
- Repaired proxy: closed manifold 40,000-triangle planning surface.
- Quad candidate: 11,248 vertices, 11,244 quads, four temporary triangle
  caps, zero boundary edges, zero non-manifold edges.
- Quad candidate remains a topology candidate, not an approved production skin.

### Facial split and controls

- Separate eye whites, irises, pupils, catchlights, upper/lower lids, muzzle,
  chin, nose, mouth, whiskers, and party-hat components created.
- `lookX`, `lookY`, `blink`, and `focus` inputs drive 20 facial channels.
- Gaze extremes remain within the authored eye region in the checkpoint renders.
- Focus narrows the pupils and lowers the upper lid.
- Blink v1 failed because translated lid curves crossed. Blink v2 uses curve
  shape keys with anchored corners and collapses the eye contents during full
  closure. A thin shadow slit remains; final eyelids need a surface shell rather
  than paired beveled curves.

### Binding and deformation audit

- Blender bone-heat weighting failed for the Tripo-derived posed surface.
- A disposable deterministic proximity bind was generated only for diagnosis.
- All deform groups received weights except `DEF_tail_08`; its guide segment is
  outside the usable tail volume and must be repositioned.
- Front-leg range causes unacceptable shoulder/belly denting.
- Rear-leg range loses hip/hock volume and does not preserve a clean paw plant.
- Head/neck range is usable as a guide but not approved.
- Tail test produces insufficient visible deformation; the tail chain and
  weights require a new centerline pass.

### Evidence

- `review/production-checkpoint-v02/`: neutral body/front, face neutral,
  gaze-left/right, blink, and focus PNGs.
- `review/deformation-audit-v03/`: neutral and four diagnostic joint-range PNGs.

### Acceptance status

**Not ready for animation.** The next pass must correct deformation loops,
tail joint placement, production weights, eyelid surface closure, UVs, and the
approved stripe/cream-zone textures. No additional animation states have been
started.

## 2026-09-19 — corrective rig and marking validation

### Corrective binding

- Built `Marmalade_ProductionRig_v01` with a new nine-point tail centerline and
  a region-aware deterministic bind on `Marmalade_WeightedCandidate_v01`.
- All 27 deform groups now contain weights; the prior empty tail-tip group is
  resolved.
- The joint-range audit no longer produces the severe shoulder/belly collapse
  or the large hip/torso cave-in seen in `deformation-audit-v03`.
- Measured maximum evaluated displacement is 0.037 m at the front-leg test,
  0.079 m at the rear-leg test, 0.059 m at the head/neck test, and 0.035 m at
  the tail test.
- The range remains deliberately conservative. Rear-paw contact, a grounded
  weight shift, and a stronger tail arc are not yet animation-ready.

### Texture and markings

- Direct surface-data transfer from the 1.9-million-face source crashed Blender.
  A UV-preserving 104,940-face projection source completed successfully.
- UV/material transfer to the weighted candidate succeeded, but the source
  texture itself is pale and omits most canonical side/back tabby markings.
- Added `MarmaladeColor`, a point-domain color layer that deforms with the mesh.
  It establishes an orange coat, cream muzzle/chest/belly/paws, forehead marks,
  cheek/leg/dorsal stripes, inner-ear pink, and rig-weight-driven tail bands.
- The color layer is a production-color blocking pass, not a final painted
  texture. The generated tail curls downward at its terminal segment, so the
  dark tip does not occupy the same topmost silhouette as the approved master.

### Evidence

- `review/corrective-rig-v01/`: neutral and four corrective deformation tests.
- `review/marking-validation-v01/`: transferred Tripo source texture diagnostic.
- `review/marking-validation-v06/`: final front/left/back/right/three-quarter
  color-blocking views.

### Acceptance status

**Still not ready for final animation or app integration.** Volume preservation
is materially improved and the missing marking structure is now visible, but
the face still requires its separate eye/lid/muzzle assembly, the coat requires
a painterly texture pass, the tail silhouette/tip must match the bible, and paw
contact must be proven in a real walk/trot cycle. The four-state scope remains
frozen; no additional states or birthday-site work were started.

## 2026-09-19 — integrated face checkpoint v05

### Face attachment and controls

- Attached `Marmalade_FaceRoot` to `DEF_head` while preserving the neutral
  assembly placement. The face root follows the corrective head-range pose.
- Retained `lookX`, `lookY`, `blink`, and `focus` as the additive face inputs.
- Brought the amber irises forward, increased their readable area, narrowed the
  neutral pupils, and reduced intersection with the inherited Tripo sockets.
- Hid the redundant separate muzzle/chin guide volumes because they doubled the
  fused source snout and produced visible cheek lumps.

### Eyelid replacement

- Replaced the paired beveled lid curves with subdivided eyelid surfaces.
- The upper surface expands over the full eye for closure; eye contents collapse
  beneath it and the lower surface remains a thin supporting rim.
- Neutral, half blink, full blink, and focused renders no longer show crossing
  curves or the former two-color closed-lid seam.
- Full closure is mechanically clean, but the large smooth lid cap still reads
  more graphic than the approved painterly master and requires final art polish.

### Evidence and status

- `review/face-integration-v05/`: neutral, gaze extremes, half/full blink, and
  focus PNGs.
- `blender/marmalade-face-integrated-v05.blend`: current assembled face and
  marked corrective body.

**Checkpoint only.** The face mechanics are now usable for continued rig work,
but likeness is not accepted: eye contour, eyelid-to-brow transition, whisker
curvature, and painterly facial warmth still need refinement. No animation
states or application files were added.
