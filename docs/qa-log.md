# QA Log

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
