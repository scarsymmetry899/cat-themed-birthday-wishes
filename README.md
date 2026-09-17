# Marmalade's Birthday — Interactive Scroll Film

An immersive birthday experience led by one consistent orange tabby kitten. The creative goal is a tiny animated film controlled by scrolling: warm, playful, cinematic and personal, with Marmalade physically carrying the visitor from one beat to the next.

## Current status

**Marmalade V1 remains frozen. The four-state native Rive lab is implemented; final visual/production acceptance is NOT claimed.** The riggable redraw, two expressions, separated vectors, native source/export and responsive test page are available for review. The redraw still looks flatter and more geometric than the painted direction. See [production notes](docs/production-redraw.md) and [QA](docs/qa-log.md) before approving it. No birthday scenes or other twelve body actions were built.

### Phase 2 working artifacts

- `tools/build-character.mjs`: editable vector source generator; creates SVG components and native RML.
- `assets/character/production/`: 50 component-group SVG exports, named head/torso/eye shapes, neutral and expression SVGs, component JSON and `marmalade-foundation.riv`. The old `marmalade-neutral-draft.riv` is historical, not the live asset.
- `rive-foundation/scene.rml`: editable native Rive source, built with official Rive CLI 1.0.4; no scripts or raster images embedded.
- `character-lab/`: native runtime, state/gaze/expression/speed controls, reversible transition tests, hat/blink/guides, pause and phone frame.
- `docs/qa/phase-2-v2/`: desktop, phone, tablet and motion-sequence evidence. `phase-2/` retains the rejected first draft.

Run `node tools/serve-lab.mjs`, then open `http://127.0.0.1:8137/character-lab/`. Recreate the draft using `node tools/build-character.mjs`, then `rive rive-foundation --verify`, `rive inspect rive-foundation --summary`, and `rive rive-foundation --once`. The official CLI is available from https://rive.app/docs/cli/getting-started.

Current artboard and machine: `Marmalade_Main`. Body states: `Idle`, `Peeking`, `Looking`, `Walking`. Inputs: `state`, `scrollProgress`, `lookX`, `lookY`, `moveSpeed`, `expression`, `blinkEnabled`, `hasHat`. Exact ranges and the nine-layer contract are in [rig-spec](docs/rig-spec.md). Only four body states exist; the 22 timelines include additive channels, blend endpoints and expressions.

The pinned browser runtime is vendored for offline review. To refresh it: `npm ci --ignore-scripts`, then `npm run vendor`. After compiling source, copy `rive-foundation/build/rive-foundation.riv` to `assets/character/production/marmalade-foundation.riv`. Run `npm run lab` and open `/character-lab/` on port 8137. The `.rml` is editable native source; no authenticated cloud `.rev` backup is included.

The repository also contains a legacy static V3 prototype (`index.html`, `styles.css`, `app.js`). It remains deployable for reference, but its hand-built SVG cat is not the approved final production asset.

## Foundation artifacts

- [Character bible](docs/character-bible.md)
- [Rig specification](docs/rig-spec.md)
- [Animation bible](docs/animation-bible.md)
- [Continuous-film storyboard](docs/storyboard.md)
- [QA log](docs/qa-log.md)
- [Marmalade master sheet v1](assets/character/marmalade-master-sheet-v1.png)

## Planned production architecture

- Next.js + TypeScript
- Rive Web runtime with `Marmalade_Main`
- GSAP + ScrollTrigger for reversible scene choreography
- Lenis synchronized to the GSAP ticker
- Canvas only for confetti/particles
- CSS design tokens and responsive art direction
- Vercel deployment through the connected GitHub repository

## Animation states

Idle, Peeking, Looking around, Walking, Yarn play, Pounce, Scratching, Paper pull/tear, Hanging, Swinging, Curling down, Sleeping, Waking, Excited, Celebration, and Hat drop/final hero.

## Intended delivery sequence

1. Approve Marmalade's v1 visual identity.
2. Redraw approved art into the separated Rive layer structure.
3. Build and verify Idle, Peeking, Looking around and Walking.
4. Prove the first three scroll scenes and reverse-safe transitions.
5. Add the remaining states and chapters.
6. Personalize name/photo, add optional audio, complete the viewport/accessibility matrix.
7. Deploy the verified production build to Vercel.

## Running the existing reference prototype

The current reference is dependency-free. Serve the repository directory with any static server, for example:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Deployment

Repository: `https://github.com/scarsymmetry899/cat-themed-birthday-wishes`

Legacy V3 alias: `https://cat-themed-birthday-wishes-abhitejachn-8733s-projects.vercel.app`

The legacy deployment remains unchanged in this foundation phase. The production alias will be updated only after character approval, implementation and full browser QA.
