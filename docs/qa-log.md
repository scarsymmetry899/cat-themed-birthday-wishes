# QA Log

## Foundation refinement — 2026-09-18

Baseline `a5b8f35e1a3cdd55b3579ca01db12fdcd6f719dd` pushed intact to the canonical repository's `codex/marmalade-phase2-foundation` branch before refinement. No production branch, approved master, bible or birthday-site files changed. **Still NOT approved for expansion.** Detailed feature-by-feature audit is in `fidelity-review.md`.

### Actual verification

- Native Rive CLI 1.0.4 verify: 0 errors, 0 warnings. Inspect: no problems. Final export 158,523 bytes, 4 body states, 37 supporting timelines, 12 layers.
- `node tools/test-foundation.mjs`: authored walk/trot target geometry, exact stance origins, closed cycle endpoints and diagonal trot pairing PASS. Walk 0.95 s, trot 0.60 s. Zero authored stance-target drift. This test does not certify intermediate native blends or aesthetic gait quality.
- Browser loaded the native export through the official low-level canvas runtime; no runtime errors were returned in the inspected log window.
- Reviewed actual live state changes, then captured eight-second 1× canvas videos and 10 Hz live paw readouts: `walk.webm`, `trot.webm`, `state-0.webm` (idle/walk/idle), `state-1.webm` (peek/look), `gait-blend.webm`, `peek-reverse.webm`, with corresponding metrics. These are real runtime captures, not image sequences assembled into fake motion. Canvas clips omit the HTML foreground ledge/guides; screenshots separately verify their compositing. The reverse clip is shorter than the full reverse-and-return test.
- Readouts show stationary support paws at their floor positions in both gait endpoints, with opposite diagonal swing pairs in trot. Runtime toe compression can move toe surfaces slightly while the paw origin stays planted. No claim of phase-locked foot constraints across every intermediate speed blend.
- Found and fixed incomplete upper-lid coverage during deterministic blink inspection. Both eyes now close; a slight closed-lid color boundary remains a visual issue.

### Browser matrix (in-app Chromium)

| CSS viewport | Result | DPR qualification |
|---|---|---|
| 1440 × 900 | Native rig, reference overlay, state/transition and debug controls exercised; screenshots saved | Actual DPR approximately 1 |
| 1920 × 1080 | Layout inspected; no horizontal overflow | Actual DPR approximately 1 |
| 834 × 1194 | Tablet two-column layout inspected; no horizontal overflow | Actual DPR approximately 1 |
| 390 × 844 | Stacked layout, character visible, controls scroll normally; no horizontal overflow | Actual DPR approximately 1 |
| 390 × 844, 2× backing | 570 × 703 canvas backing confirmed; character inspected | Artificial backing-resolution test, NOT device-DPR emulation |
| Physical mid-range phone | UNVERIFIED | No physical phone available |
| Genuine Retina/high-DPR device | UNVERIFIED | Viewport API does not expose deviceScaleFactor; default host was approximately 1.35 earlier, not a Retina acceptance test |

### Evidence and disposition

`docs/qa/phase-2-refinement/` holds neutral overlay, idle, blink midpoint, gaze samples, peek 25/50/75/100, walk/trot contact stills, viewport shots, silhouette/marking tests and videos. UI readout is requested state plus actual native input values, not a claim that a transition has finished. Some early screenshots preceded the last foreleg-band refinement; final walk/trot recordings and final review stills show the last export.

All body transitions still use one continuous vector rig and 650 ms cubic blends. Idle→peek, peek→look, look→idle and idle↔walk are exercised through buttons/sequences; walk↔trot input is now smoothed over a 280 ms response. Silhouette, head/tail/ear continuity and contact behavior have been sampled, not exhaustively certified at every interrupted transition phase. The eye-first response uses 130 ms gaze smoothing, then slower head and ear response; pointer center dead zone is 12%.

**Open gates:** exact likeness/painted warmth, final gait performance (still frontal/in-place), all-speed blend contact polish, closed-lid color integration, side/back dorsal-marking validation, physical mobile performance and genuine high-DPR verification. A dedicated reversible ear flick was added at 92% peek after the earlier captures. No acceptance is inferred from compile success or fixed-target tests.

**Preview deployment:** Vercel connector lists a different accessible project, and lookup of `cat-themed-birthday-wishes` returns 404. An untargeted deployment request was blocked by auto-review because the destination/payload were not sufficiently verified. No deployment or production promotion was performed; correct project access/ID is needed for a preview-only deployment.

## Phase 2 — four-state review candidate, 2026-09-18

The native four-state lab now exists. **Not all acceptance gates pass; do not label this production-complete.** The user allowed a clean riggable redraw after the rejected first attempt. The new assembly improves muzzle/chest boundaries, eye shape and joint overlaps, but its flatter geometric finish and frontal gait still require art/motion refinement. V1 and the birthday website are unchanged.

### Structural verification

Official Rive CLI 1.0.4: final source verified with 0 errors/0 warnings and native export built at 69,945 bytes. Inspection returned no problems. 22 timelines comprise four body states plus additive loops, expression poses and blend endpoints; no other twelve story actions were added. Browser uses actual `.riv` with local `@rive-app/canvas` 2.42.2, not an SVG animation substitute.

### Browser inspection actually performed

Codex in-app Chromium: CSS viewport sizes verified through DOM: desktop 1440 × 900, phone 390 × 844, tablet 834 × 1194. DPR approximately 1 in this environment. Phone and tablet had no horizontal document overflow. Inspected native player and side-by-side master/neutral assembly; exercised state buttons, gaze extrema, speed-to-trot, focused/mischievous expressions, hat, blink toggle, pause, neutral guides, and phone-frame control.

Motion inspection used live runtime sequences and successive screenshots, not only one compiled frame. Saved evidence in `qa/phase-2-v2/`: `desktop-idle.png`, `peek-midpoint.png`, `peek-hold.png`, `gaze-left.png`, `gaze-right.png`, `walk-0..3.png`, `peek-reverse-0..4.png`, `peek-look-0..3.png`, `idle-walk-idle-0..3.png`, `phone-idle.png`, `phone-trot-0..2.png`, `tablet-idle.png`, `tablet-gaze-left/right.png`, expression stills and `assembly-comparison.png`. Files with numeric suffixes are successive live samples, not frame-accurate video. Full-page captures may contain browser stitching repeats; viewport dimensions refer to verified CSS dimensions.

| Gate | Observation / disposition |
|---|---|
| Identity / neutral proportions | Recognizable orange tabby trait set, but exact V1 face/marking/softness match NOT passed; see production-redraw.md |
| Same character during motion | Same geometry hierarchy throughout; no swapped drawings observed |
| Limb seams / cream clipping | No open joint gaps or protruding cream patches observed in sampled frontal walk/trot and peek; not an exhaustive pose sweep |
| Tail | Gentle articulated secondary motion remains connected; large-range smooth mesh deformation not tested |
| Blink / gaze | Close/open loop visible; pupil/iris remains clipped at tested left/right extremes; focused lids lower consistently |
| Peek reverse | Sequence rises, holds, retreats, returns to hold through the same progress blend |
| Peek → looking / looking → idle | Native 550 ms blends exercised; no duplicate drawings; host ledge fades independently |
| Idle → walking → idle | Native blend sequence exercised; no open limbs observed; gait remains frontal/in-place and is not considered polished side-view locomotion |
| Frame pacing | Usually 58–60 advance callbacks/s while visible after startup; no obvious sustained hitch in sampled motion. Callback count is NOT a GPU frame-time benchmark |
| Retina / physical mobile | NOT TESTED. Vector source and DPR-aware canvas implemented, but DPR1 viewport simulation does not prove Retina sharpness or mid-range phone performance |
| Runtime logs | Found wasm streaming MIME error, corrected server to application/wasm; after reload only the existing state-input deprecation warning was new |

An occluded Edge tab ran at about 1 callback/s due to background throttling; it was not used for a mobile-performance claim. State inputs are retained for the requested contract and runtime is pinned; a future major-runtime upgrade needs data-binding migration.

### Remaining acceptance work

Art fidelity (especially forehead taper, eye/muzzle contours, limb volumes and painted softness), polished locomotion, complete high-DPR visual checks and real mid-range-mobile performance are unresolved. Dorsal/side identity is not validated by a frontal rig. No cloud editor `.rev` backup, deployment, birthday rebuild or remaining story animations are claimed. This section supersedes the historical draft findings below, which are kept as an audit trail.

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
