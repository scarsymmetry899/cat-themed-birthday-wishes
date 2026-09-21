# Marmalade 3D production assets

Status: **Tripo-likeness recovery / four-state Blender checkpoint**.
The browser lab now uses the preserved 20K Tripo mesh and texture instead of
the rejected replacement geometry. The recovered skin is suitable for this
interactive checkpoint, but the fused source eyes and muzzle still prevent a
true separate eyelid/gaze facial rig.

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
- `blender/marmalade-contact-gaits-v11.blend` — current walk/trot contact proof
  with two-bone ankle IK, world-oriented paws, rigid paw-weight islands, and
  measured stance drift. It remains a diagnostic gait checkpoint.
- `blender/marmalade-foundation-v12.blend` — scoped four-state Blender
  checkpoint with Idle/Breathing, Peeking, Looking Around, Walk, and Trot
  actions plus the integrated face controls.
- `web/marmalade-foundation-preview-v13.glb` — browser export used by
  the earlier corrective-mesh checkpoint.
- `source/marmalade-tripo-retopo20k-v01.glb` — untouched 20K Tripo retopology
  source used for the likeness recovery.
- `blender/marmalade-tripo-recovery-v01.blend` — clean, texture-preserving
  Tripo source with the downloaded unusable skin removed.
- `blender/marmalade-tripo-foundation-v09.blend` — corrected-axis 26-joint
  Blender recovery rig with complete deterministic skin weights and the frozen
  four-state action set.
- `web/marmalade-tripo-foundation-v09.glb` — current `/character-lab/` export.
  It contains Idle/Breathing, Peeking, Looking Around, and Walking.

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
correct the terminal tail silhouette before animation acceptance. The current
front paw topology also needs a local rebuild: the far front paw exposes stacked
toe surfaces during the trot even after rigid paw weighting.

Current face inputs on `Marmalade_FaceRoot`:

- `lookX`: `-1..1`
- `lookY`: `-1..1`
- `blink`: `0..1`
- `focus`: `0..1`

The eye whites, irises, pupils, catchlights, upper/lower lids, muzzle lobes,
chin, nose, mouth, whiskers, and party-hat objects are separate.

Only the four foundation states remain in scope: Idle/Breathing, Peeking,
Looking Around, and Walking/Trotting.

The interactive GLB preview is intentionally labelled as a checkpoint. It is
not foundation acceptance: final painted-master likeness and the local
front-paw topology remain open.
