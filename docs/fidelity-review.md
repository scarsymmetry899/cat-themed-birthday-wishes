# Four-state refinement: visual comparison

Reference: unchanged `assets/character/marmalade-master-sheet-v1.png`, first/front figure, crop coordinates 0…300 × 0…370. Baseline `a5b8f35e1a3cdd55b3579ca01db12fdcd6f719dd` was pushed intact to `codex/marmalade-phase2-foundation` before this refinement. No changes to main or the birthday website.

## Comparison method

The lab overlays the original front crop beneath the live native vector character. Reference opacity is adjustable 0–100%; the rig becomes partially transparent during overlay review. Guides identify eye, nose, chin, shoulders, paw baseline and tail root. These manually selected guide coordinates are inspection aids, NOT a pixel-error measurement or an assertion of exact matching.

Neutral, peek at 25/50/75/100, looking extremes and walk contact poses were inspected. The same face geometry is reused in all states; movement does not substitute a different drawing. The reference sheet's side-view walking illustration is not a matching camera angle for this frontal treadmill cycle.

## Feature audit

| Feature | Refinement and remaining assessment |
|---|---|
| Forehead width | Crown remains approximately 150 units wide across temples; softened upper contour. Still cleaner than painted fur. |
| Cheek volume | Added side-volume shapes and separate short cheek tufts; did not inflate head size. |
| Chin width / skull roundness | Shortened lower face from roughly y213 to y205; rounded jaw transitions, reduced broad lower semicircle. |
| Ear size / spacing | Kept attachment centers at ±59 relative to head; rounded tips, made right ear subtly different, reshaped inner wells. Pink still reads flatter than the painted reference. |
| Eye size / vertical placement | Asymmetric approximately 41 × 37 contours at y146. Kept the eye line at the master landmark. |
| Eye-center distance | Increased from 68 to 72 units: centers approximately (126,146) and (198,146). |
| Amber iris | 29 × 32.4 units, reduced from 31 × 35; retains amber palette. |
| Pupils | Reduced to 18.6 × 27; subtle inward bias differs by eye. Travel is limited and clipped. |
| Catchlights | Main glints moved to upper inner quadrant with small secondary glint; unequal local positions avoid perfect mirroring. |
| Eyelid curvature | Corrected incomplete closure, extended upper coverage, added curved lower lid line. Closed lids still have a slight fill-tone boundary; this is an unresolved polish issue. |
| Cream muzzle width | Retained broad cream cheeks but introduced curved, shallow fur-edge breaks and a narrower chin. |
| Cheek-to-muzzle transition | Replaced plain semicircle with asymmetric contour and radial cream shading. The softness is improved, not an exact painted match. |
| Nose size / vertical position | Reduced width from 18 to 16; center moved 1.5 units lower, near y166. |
| Mouth curvature | Shorter unequal lobes, subtle off-center philtrum; preserved closed neutral smile. |
| Forehead M | Narrowed and tapered, added an uneven outer finger. Still visibly more graphic than painted stripe edges. NOT a perfect-match pass. |
| Two cheek stripes per side | Tapered curved ends and unequal left/right boundaries; two stripes retained per cheek. |
| Dorsal stripes | Not visible in the frontal source; side/back stripe fidelity remains UNVERIFIED. No fabricated turnaround approval. |
| Leg stripes | Two foreleg bands now belong to the shin; no stripe spans the upper/lower hinge. Added local leg shading. |
| Tail bands | Remain parented to five curved segments; cream tip follows the visible sheet, despite old written dark-tip contradiction. |
| Oversized-head relationship | Kept one shared head/body rig; no state-specific scaling to fake likeness. |
| Torso width / length | Same compact frontal torso bounds, independent subtle shoulder/hip shifts in locomotion. |
| Leg length | Neutral shoulder-to-paw origin remains 80 units; shin positions compensate support motion. |
| Paw scale | Neutral geometry preserved, landing compression limited to 4%; rear paws remain partly occluded. |
| Tail thickness / length | Increased segment thickness 2.5 units; shortened distal chain by 13 units to better match the front reference. |
| Warmth / finish | Added two radial volume gradients, temple/nose/body shading, 1,200 fine head-fur curves. Still more graphic and symmetrical than V1's painted finish. |

## Pose-specific observations

- **Neutral:** major landmark registration improved, but the overall painted softness gate is still open. This is not authorization to replace the approved character.
- **Peek:** 25% shows ear tips, 25–35% pauses, 50% reveals eyes, 65% scans, 75% reaches, 85% overshoots/compresses, 92% flicks one ear, 100% holds with tilt. Progress keys reverse along the same poses; the additive ear layer continues independently.
- **Looking:** pupil smoothing precedes head response, then ear response. Automatic gaze drift is modest; pointer input has a 12% center dead zone. Max travel remains eye-clipped.
- **Walk/trot:** frontal in-place support shifts replace the original mirrored sine motion. Footfall order, landing compression and restrained head bob are improved. It is still not a polished side-view traveling walk or final character-performance approval.

## Acceptance decision

**Do not expand.** Likeness/painted softness, closed-lid color integration, final gait performance and all-speed transition acceptance remain open. Source-target tests and recordings demonstrate implementation, not an aesthetic pass. Physical mid-range-mobile performance is UNVERIFIED. Retina/device-DPR emulation is UNVERIFIED; a separately labelled 2× canvas-backing check is available and was exercised.
