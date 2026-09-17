# Marmalade's Birthday — Interactive Scroll Film

An immersive birthday experience led by one consistent orange tabby kitten. The creative goal is a tiny animated film controlled by scrolling: warm, playful, cinematic and personal, with Marmalade physically carrying the visitor from one beat to the next.

## Current status

**Marmalade V1 is approved and frozen. Phase 2 is incomplete at the neutral assembly gate.** A separated vector draft and genuine Rive neutral export now exist. Visual comparison rejected the draft: it does not yet match the approved face, muzzle, limbs or painted finish. The four states have not been built. This is not an approval-ready foundation prototype.

### Phase 2 working artifacts

- `tools/build-character.mjs`: editable vector source generator; creates SVG components and native RML.
- `assets/character/production/`: 35 component-group SVG exports, assembled SVG, component JSON and neutral `.riv` draft. Folder naming does not imply production acceptance.
- `rive-foundation/scene.rml`: editable native Rive source, built with official Rive CLI 1.0.4; no scripts or raster images embedded.
- `character-lab/`: neutral assembly comparison only; animation controls intentionally unavailable.
- `docs/qa/phase-2/`: desktop, phone and tablet assembly evidence.

Run `node tools/serve-lab.mjs`, then open `http://127.0.0.1:8137/character-lab/`. Recreate the draft using `node tools/build-character.mjs`, then `rive rive-foundation --verify`, `rive inspect rive-foundation --summary`, and `rive rive-foundation --once`. The official CLI is available from https://rive.app/docs/cli/getting-started.

Current exported artboard and machine: `Marmalade_Main`. Layer: `Body_Action`. Timeline: `Neutral`. **No runtime inputs or four-state animations exist yet.** The original state-machine contract remains planned, not implemented.

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
