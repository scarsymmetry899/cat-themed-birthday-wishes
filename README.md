# Paws, Purrs & Birthday Wishes — V3

A scroll-choreographed, Framer-style birthday story built around **one continuous orange-tabby protagonist**.

## What changed in V3

The previous card-by-card raster implementation was replaced rather than patched.

- **No blurry cat PNGs.** The protagonist is now a crisp inline SVG character that stays sharp at every screen size.
- **One continuous actor.** The same cat follows the visitor through the entire page instead of being repeated as separate static images.
- **Scroll choreography.** A requestAnimationFrame interpolation layer maps scroll position to cat position, rotation, scale and scene progress.
- **Pose transitions.** Head, body, paws, tail, eyes and party hat are independently articulated for peeking, yarn play, chasing, tearing, hanging, sleeping and celebrating.
- **Pinned cinematic chapters.** Each story beat uses a sticky viewport with long scroll travel, giving the page a continuous motion-design feel rather than a stack of greeting cards.
- **Responsive choreography.** Desktop and mobile use different cat travel coordinates and scene composition.

## Story flow

1. **Arrival** — the tabby peeks into the page and invites the visitor to follow.
2. **Yarn** — a purple yarn path physically draws itself as the visitor scrolls while the ball rolls across the scene.
3. **Chase** — a toy ball rolls and bounces while the cat changes into a chase pose.
4. **Tear reveal** — patterned paper splits apart with scroll progress to expose “You are deeply loved.”
5. **Hang** — the cat transitions into a hanging pose beneath a rope while a suspended birthday note drops into view.
6. **Nap** — the body settles, eyes close and the character breathes gently in a calmer chapter.
7. **Party** — the party hat appears, balloons enter and confetti can be released interactively.
8. **Finale** — local-only photo personalization, cake, candles, confetti and an optional Happy Birthday Web Audio melody.

## Architecture

```text
cat-themed-birthday-wishes/
├── index.html     # semantic story markup + inline vector cat
├── styles.css     # motion design, pose system, responsive layouts
├── app.js         # scroll choreography + interactions + audio
├── vercel.json
└── README.md
```

The old Base64 cat assets may remain in `assets/` for reference, but **V3 does not use them**.

## Responsive design

### Desktop
- long pinned chapters
- wide editorial composition
- chapter rail navigation
- scroll-linked character travel on the right/left of the story as needed

### Mobile
- dedicated actor coordinates rather than simply scaling desktop
- shortened scroll lengths
- centered storytelling copy
- re-positioned hanging note, balloons, finale card and cat path
- large touch targets

## Interaction details

- scroll progress bar
- chapter navigation rail on desktop
- scroll-drawn yarn
- rolling/bouncing ball
- physical two-panel tear reveal
- suspended note reveal
- sleeping-eye state and breathing motion
- balloon entrances
- generated confetti
- browser-local photo picker
- user-triggered Happy Birthday melody
- replay control
- `prefers-reduced-motion` fallback

## Privacy

Photos chosen in the finale are read with `FileReader` and remain in the visitor's browser. Nothing is uploaded to a server.

## Production

Canonical repository:

`https://github.com/scarsymmetry899/cat-themed-birthday-wishes`

Stable Vercel alias:

`https://cat-themed-birthday-wishes-abhitejachn-8733s-projects.vercel.app`

The V3 production deployment was created on 17 September 2026.
