# Paws, Purrs & Birthday Wishes

An interactive, cat-led birthday greeting experience designed to work beautifully on **mobile, tablet, and desktop**.

This build is a **static, zero-backend web experience** with:
- responsive layouts
- scroll-based storytelling
- an orange tabby protagonist
- yarn, ball, tear-card, hanging-note, cozy-nap and party scenes
- a local-only birthday photo upload
- an optional Web Audio birthday tune
- reduced-motion support

## Story flow

1. Hero intro
2. Yarn play
3. Ball chase
4. Paper-tear reveal
5. Hanging birthday note
6. Cozy rest scene
7. Mischief/confetti scene
8. Personalized birthday finale

## Privacy

The finale photo is read with the browser `FileReader` API. The chosen photo stays in the visitor's browser and is not uploaded to a server.

## Audio

The birthday melody is synthesized with the Web Audio API and only starts after explicit user interaction.

## Deployment

This is a static Vercel-ready site. `index.html` is the entry point. The production version uses embedded visual assets so the experience remains portable and avoids broken asset paths.

## Responsive targets

- Mobile phones, including narrow portrait layouts
- Tablets
- Standard laptops
- Large desktop screens

The interaction design uses fluid typography, touch-friendly controls and responsive scene composition.
