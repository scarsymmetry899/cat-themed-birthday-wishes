# Marmalade's Birthday — Interactive Scroll Film

An immersive birthday experience led by one consistent orange tabby kitten. The creative goal is a tiny animated film controlled by scrolling: warm, playful, cinematic and personal, with Marmalade physically carrying the visitor from one beat to the next.

## Current status

**Phase 1 — character foundation ready for approval.** The master sheet, palette, fixed marking map, proportion guide, rig split and 16-state animation plan are complete. Final rigging and the Next.js/Rive rebuild intentionally have not started until the character identity is approved.

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
