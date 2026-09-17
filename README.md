# Paws, Purrs & Birthday Wishes

A responsive, interactive cat-led birthday greeting experience for **mobile, tablet and desktop**.

The protagonist is a warm orange tabby who guides the recipient through a playful scrolling birthday story: peeking into the page, getting tangled in yarn, chasing a ball, tearing open a hidden message, hanging from the card, slowing down for a cozy moment, creating birthday chaos and finally leading into a personalized celebration.

## Live production deployment

Production alias:

`https://cat-themed-birthday-wishes-abhitejachn-8733s-projects.vercel.app`

Production deployment created from this build:

`https://cat-themed-birthday-wishes-fo87whynx-abhitejachn-8733s-projects.vercel.app`

## Experience flow

1. **Cat arrival / hero** — editorial birthday-card opening with a peeking tabby and scroll cue.
2. **Yarn play** — animated yarn and a playful birthday wish.
3. **Ball chase** — moving toy interaction with a second short birthday note.
4. **Torn-card reveal** — scroll-driven paper panels pull apart to uncover the hidden message: “You are deeply loved.”
5. **Hanging note** — the tabby hangs from the page while delivering a paw-written birthday message.
6. **Cozy pause** — a calmer, warm-wishes chapter before the party.
7. **Birthday mischief** — balloons, party styling and user-triggered confetti.
8. **Grand finale** — photo personalization, recipient name, cake, candles, balloons, confetti and an optional Happy Birthday melody.

## Personalization

The finale supports:

- **Recipient name** — entered in the browser and immediately reflected in the Happy Birthday headline.
- **Recipient photo** — chosen from the device and previewed directly inside the final card.

The photo uses the browser `FileReader` API and is **not uploaded to a server**.

## Audio

The Happy Birthday tune is synthesized with the **Web Audio API**. It starts only after the visitor presses the play button, which keeps the experience compatible with browser autoplay restrictions.

## Animation system

The build uses lightweight browser-native animation rather than a heavy animation framework:

- CSS keyframes for cat float/swing, yarn, ball, balloons, candles and resting movement
- scroll-position-driven paper-tear animation
- DOM-generated confetti particles
- smooth scene navigation
- `prefers-reduced-motion` support

## Visual assets

The deployable source currently stores the key orange-tabby illustrations as Base64 text assets:

- `assets/cat-peek.b64`
- `assets/cat-hang.b64`

At runtime the page converts these to local WebP data URIs. The remaining motion props and scenes are composed with responsive HTML/CSS so the page remains lightweight and resizes cleanly across screen sizes.

The full high-resolution source asset set used during art direction is also preserved in the local project package and includes dedicated yarn, chase, tear, nap, party and finale artwork for future higher-fidelity iterations.

## Responsive behavior

The experience is designed around fluid breakpoints rather than a fixed phone canvas.

### Desktop

- two-column editorial compositions
- larger illustrated scenes
- generous whitespace
- wide finale with photo and celebration composition side-by-side

### Mobile

- scenes stack vertically
- artwork is prioritized before supporting copy where appropriate
- fluid typography uses `clamp()`
- controls remain touch-friendly
- finale photo card fits narrow portrait screens
- tear and hanging scenes use alternate mobile positioning

## Accessibility / UX

- semantic headings and buttons
- alt text for cat illustrations
- user-controlled sound
- no autoplay audio
- reduced-motion support
- responsive touch targets
- local-only photo handling

## Technology

- Vanilla HTML
- CSS
- JavaScript
- Web Audio API
- FileReader API
- Static hosting / Vercel

No backend or database is required.

## Repository structure

```text
cat-themed-birthday-wishes/
├── index.html
├── README.md
└── assets/
    ├── cat-peek.b64
    └── cat-hang.b64
```

## Deployment architecture

The GitHub repository is the canonical source. A Vercel production deployment has been created for the birthday experience. The deployed entry point loads the current `main` build so updates made to the canonical source can be rolled into subsequent production deployments without changing the experience architecture.

## Current build status

- [x] Responsive desktop layout
- [x] Responsive mobile layout
- [x] Orange-tabby protagonist
- [x] Scroll story
- [x] Yarn sequence
- [x] Ball sequence
- [x] Scroll-based torn-paper reveal
- [x] Hanging-cat scene
- [x] Cozy scene
- [x] Party scene
- [x] Confetti
- [x] Recipient photo picker
- [x] Recipient name personalization
- [x] Birthday cake and animated candles
- [x] Happy Birthday Web Audio melody
- [x] Reduced-motion support
- [x] GitHub source repository
- [x] Vercel production deployment
