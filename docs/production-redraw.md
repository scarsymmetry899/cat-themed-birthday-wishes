# Marmalade production redraw — review candidate

The approved master sheet and character bible have not been edited. This vector redraw is a candidate rig source, not a replacement approval for V1.

## Delivered artwork

One frontal neutral assembly supplies all four body states. Head, ears/inner ears, eye whites, irises/pupils/catchlights, upper/lower lids, muzzle, nose, mouth, whiskers, torso, chest/belly, three-piece front/rear limbs, five tail segments and hat/anchor are named and independently controllable in native source. `parts.json` contains hierarchy and geometry. No low-resolution raster fragments deform during motion.

Focused uses lowered, slightly angled lids. Mischievous uses asymmetric lid heights. Neither changes the underlying head, muzzle, colors or markings. Static expression SVGs are included alongside the neutral assembly.

## Assembly comparison / deviations

Inspected side-by-side in the lab and saved `qa/phase-2-v2/assembly-comparison.png`.

- Oversized head, compact seated frontal silhouette, amber eyes, forehead mark, paired cheek bands, pink nose/ears, cream muzzle/chest/belly/paws and ringed tail are represented.
- Fur contour and shaded volumes are simplified into smooth paths and gradients; fine vector strokes approximate texture. The result remains visibly flatter and more geometric than the master. Premium painted softness is not fully matched.
- Eye contours, forehead stripe taper, muzzle boundary, front limb silhouette and paw forms are approximations, not proven exact matches. These remain visual acceptance issues, not unavoidable rigging exceptions.
- Neutral proportions stay fixed across states; all poses share one geometry hierarchy. The walk/trot is frontal and in-place, not the master sheet's side-view traveling gait. A polished directional walk is not delivered.
- Tail is articulated through overlapping curved segments; it is not a continuous weighted mesh. It has gentle secondary movement, not a large-range deformation test.
- Front view does not validate dorsal markings in side/back views. Do not reuse it as an approved turnaround.
- The painted sheet shows a cream tail tip while the written bible describes a dark tip. This candidate follows the image; neither reference was silently changed.

These gaps prevent claiming all production acceptance gates passed. The four-state lab makes the remaining art/motion judgments visible. Birthday-site integration and the remaining twelve body actions stay out of scope.
