# Marmalade 3D production assets

Status: **corrective-bind / marking-blockout checkpoint**.
Nothing in this directory is approved as the final deforming mesh yet.

## Source files

- `source/marmalade-tripo-highdetail-v01.glb` — immutable Tripo export and the
  sculpt/texture reference. It contains one fused mesh (including the painted
  facial features), about 1.9 million triangles, and 4K PBR maps.
- `blender/marmalade-source-audit-v01.blend` — isolated import used to inspect
  the Tripo result.
- `blender/marmalade-production-v01.blend` — protected production starting
  point.
- `blender/marmalade-retopo-proxy-v01.blend` — repaired, manifold volume proxy
  at 40,000 triangles. This is a planning/reference surface, not animation
  topology.
- `blender/marmalade-rig-guide-v01.blend` — unbound 32-bone joint, hierarchy,
  and naming guide. It intentionally does not deform the proxy.
- `blender/marmalade-quad-base-candidate-v05.blend` — closed manifold
  QuadriFlow candidate: 11,244 quads plus four explicitly tracked temporary
  triangle caps where the solver left tiny holes.
- `blender/marmalade-production-checkpoint-v02.blend` — current unbound visual
  checkpoint with separately controllable face parts, additive face inputs,
  and a hidden party hat.
- `blender/marmalade-deformation-audit-v03.blend` — disposable proximity-weight
  bind and joint-range action used to expose topology/weighting failures. It is
  not the production skin.
- `blender/marmalade-corrective-rig-v01.blend` — region-aware weighted candidate,
  corrected tail chain, and corrective joint-range action.
- `blender/marmalade-marked-candidate-v05.blend` — latest deformation-safe
  orange/cream/tabby color-blocking candidate. This supersedes the earlier
  marked-candidate iterations but is not the final painterly coat.
- `blender/marmalade-face-integrated-v05.blend` — current head-bone-attached
  face checkpoint with surface eyelids, amber-eye refinement, gaze, blink, and
  focus controls.

## Verified source limitations

- The source is a single fused mesh with no armature or shape keys.
- Raw topology is non-manifold and has inconsistent face normals.
- The hidden side/back markings are incomplete.
- The tail bands and dark tail tip do not match the approved character bible.
- Eyes, lids, pupils, muzzle, and mouth are painted/fused rather than separately
  controllable production parts.

## Next acceptance gate

Replace the four temporary triangle caps with authored quad patches. Refine the
current controlled weights for planted rear-paw contact, shoulder/hip weight
shift, and a stronger tail arc. Refine the new surface eyelids into the head
silhouette and correct eye contour/spacing, whisker curvature, and facial
warmth. Convert the current color blocking into the approved painterly coat and
correct the terminal tail silhouette before animation acceptance.

Current face inputs on `Marmalade_FaceRoot`:

- `lookX`: `-1..1`
- `lookY`: `-1..1`
- `blink`: `0..1`
- `focus`: `0..1`

The eye whites, irises, pupils, catchlights, upper/lower lids, muzzle lobes,
chin, nose, mouth, whiskers, and party-hat objects are separate.

Only the four foundation states remain in scope: Idle/Breathing, Peeking,
Looking Around, and Walking/Trotting.
