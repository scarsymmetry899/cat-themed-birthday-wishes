# QA Log

## Phase 2 — rejected neutral assembly, 2026-09-18

Phase 2 is **not complete**. The approved master and bible remain unchanged. The Phase 1 consistency assessment above/below was too broad: the sheet and written tail-tip specification disagree. No claim of exact production identity is valid yet.

Actual work: generated 35 separated SVG groups and assembled SVG, authored native RML through a deterministic generator, compiled a native `.riv` neutral draft using official Rive CLI 1.0.4. No raster fragments are embedded. `rive --verify` returned 0 errors/0 warnings; `rive inspect --summary` reported no problems after adding the artboard style. That proves structural validity only.

| Check | Evidence | Result |
|---|---|---|
| Native neutral render | Rive CLI screenshot inspected | Rejected: simplified silhouette, muzzle, limbs and finish differ from approved master |
| Initial eyelid masking | Forehead M obscured in first native render | Corrected with eye-region clipping; re-rendered |
| Desktop neutral comparison | Edge, actual CSS viewport 1440 × 900; `qa/phase-2/desktop-assembly.png` | Page inspected, identity mismatch remains |
| Phone neutral comparison | Edge, actual CSS viewport 390 × 844; `qa/phase-2/phone-assembly.png` | Page inspected, identity mismatch remains |
| Tablet neutral comparison | Edge, actual CSS viewport 900 × 1081; `qa/phase-2/tablet-assembly.png` | Page inspected, identity mismatch remains |
| Console | Browser logs inspected | Extension warnings observed; not attributed to lab code |
| Four states, blended transitions, reverse peek | Not implemented | NOT TESTED |
| Retina/high-DPR and mid-range mobile performance | Browser DPR approximately 0.9; no physical mobile tested | NOT TESTED |
| Tail segmentation, seams under deformation | Tail remains a single contour; no motion exists | NOT PASSED |

Screenshots show the comparison page, which renders the assembled SVG; it is not a Rive runtime player. Native Rive screenshot was checked separately. Idle/peek/gaze/walk screenshots cannot be supplied because these states do not exist. No motion QA is claimed.

Next prerequisite: a faithful vector redraw that passes side-by-side neutral comparison before any animation is authored. The current redraw is a rejected working draft, not a proposed new canonical character.

This phase validates only the character foundation and repository artifacts. Motion/browser QA begins with the four-state Rive prototype.

| Date | View / asset | Observation | Fix / decision | Result |
|---|---|---|---|---|
| 2026-09-18 | Master sheet, 1536 × 1024 | Forehead M, amber eyes, cream zones and head/body ratio remain coherent across turnarounds and actions. | Locked those traits in the bible and palette. | Pass for v1 approval candidate. |
| 2026-09-18 | Master sheet, full-size visual review | Turnarounds, actions and eight expression heads are crisp and non-overlapping. | Kept source as concept/model sheet; explicitly barred it from use as a raster pose atlas. | Pass. |
| 2026-09-18 | Rig feasibility review | Painted shading cannot be directly decomposed into a production Rive rig. | Defined a separated vector redraw, masks, pivots, mesh zones and draw-order swaps. | Plan ready; rig intentionally not started. |
| 2026-09-18 | Existing V3 source review | Current protagonist is a single hand-coded SVG and does not satisfy the new final-art bar. | Preserved V3; marked it as legacy prototype pending foundation approval. | No regression introduced. |

## Upcoming test matrix

- Desktop: 1440 × 900, 1920 × 1080.
- Laptop: 1366 × 768.
- Tablet: 1024 × 1366 and 834 × 1194.
- Mobile: 390 × 844 iPhone, 412 × 915 Android, 360 × 800 compact Android.
- Accessibility: reduced motion, keyboard-only upload/control flow, 200% zoom, high-contrast checks.
- Resilience: slow 3G asset load, Rive unavailable fallback, audio disabled, invalid/large image upload.
