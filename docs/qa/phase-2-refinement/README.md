# Evidence provenance

Native export SHA-256: `58D833B70BADCE65AB45C6E1583E891F98060C3F8ACE2F6CE218CF5AD11B67F7`.

Canonical master SHA-256 (unchanged): `02517CBA7729283BA51F4F9D3972CCD3A802804C9298B5F8D3D49C072CC20FF5`.

PNG files are actual browser captures. WEBM files are 8-second captures from the live native Rive canvas at 1× playback, with matching 10 Hz JSON readouts. They do not include HTML overlays, foreground ledge, or diagnostic SVGs. The recordings are available for independent real-time review; they are not a claim that an animator has approved the performance.

`state-0` records idle → walk → idle. `state-1` records peek → looking. `peek-reverse` records the reversible test; 8 seconds does not cover the entire return-to-hold sequence. `gait-blend` records walk → trot → walk.

The readout's near-floor contact classification is a diagnostic, not a physics contact event. Source-target assertions are separate (`node tools/test-foundation.mjs`). Early captures preceded the final foreleg stripe and peek-ear changes; final videos/late stills supersede those for those details. Viewport and physical-device qualifications are in `../../qa-log.md`.
