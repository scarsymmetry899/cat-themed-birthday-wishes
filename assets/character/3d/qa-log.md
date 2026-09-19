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
