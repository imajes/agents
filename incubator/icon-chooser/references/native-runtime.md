# Native Font Awesome SVG + JS

Generate `recipes ICON --output /absolute/directory` for a working offline page.
Choose an explicit family/weight to match the intended artifact. `--topic` selects
one of sizing, alignment, duotone, rotation, lists, stacking, motion, transforms,
masking, layers, accessibility, or all.

The bundle contains Font Awesome 7.3.1's SVG+JS core, its SVG CSS, two selected
native icon definitions (the chosen icon and a circle used by masks/stacks),
recipe CSS, an HTML page, a manifest, and the supplied license. It needs no Kit,
account token, font installation, network connection, or full icon-style JS file.

Load the bundled runtime before the selected definitions and initialization code:

```html
<link rel="stylesheet" href="svg-with-js.min.css">
<link rel="stylesheet" href="recipes.css">
<script defer src="fontawesome.min.js"></script>
<script defer src="icons.js"></script>
```

The generated page displays examples and expandable HTML snippets. Its JS shows
native definitions, `library.add`, transform parsing, `icon`, masking, and DOM
conversion. Copy only the code relevant to the artifact. If it already uses Font
Awesome 7.3.1, add the selected definitions to that runtime rather than loading
another instance. Existing React/Vue integrations can consume the same native
definition shape; follow that integration's component API.

| Need | Native mechanism |
| --- | --- |
| Relative sizes | `fa-xs`, `fa-sm`, `fa-lg`, `fa-xl`, `fa-2xl` |
| Display sizes | `fa-2x` through `fa-10x`, or CSS font-size |
| Width/canvas | v7 fixed canvas by default; `fa-width-auto` for natural width |
| Lists/borders | `fa-ul`, `fa-li`, `fa-border`, `fa-pull-left/right` |
| Rotation/flips | `fa-rotate-90/180/270`, `fa-flip-horizontal/vertical/both` |
| Two layers | `--fa-primary-color`, `--fa-secondary-color`, their opacity variables, `fa-swap-opacity` |
| Motion | `fa-beat`, `fa-fade`, `fa-beat-fade`, `fa-bounce`, `fa-flip`, `fa-shake`, `fa-spin`, `fa-spin-pulse` |
| Timing | `--fa-animation-duration`, delay, direction, iteration-count, timing variables |
| Power transforms | `FontAwesome.parse.transform('shrink-6 rotate-20 right-1')` and the `icon` transform option |
| Masks | The `icon` mask option with a native mask definition and an instance-unique mask ID |
| Layers | `fa-layers`, `fa-layers-text`, `fa-layers-counter`; label meaningful compositions |

Keep native definitions intact: multi-layer path order and family prefixes matter.
The builder copies definitions from the matching Web distribution rather than
guessing a family prefix or reconstructing native geometry from SVGs.

Native CSS supports reduced-motion settings; the bundle also disables incidental
motion under `prefers-reduced-motion: reduce`. Do not animate state meaning out of
existence when reduced motion is enabled. Avoid communicating meaning only with
color or animation. Native masks generate SVG IDs; assign unique mask IDs if
copying a masked composition multiple times.

Sources:
- https://docs.fontawesome.com/web/setup/host-yourself/svg-js
- https://docs.fontawesome.com/web/style/sizing
- https://docs.fontawesome.com/web/style/icon-canvas
- https://docs.fontawesome.com/web/style/animate
- https://docs.fontawesome.com/web/style/power-transform
- https://docs.fontawesome.com/web/style/mask
- https://docs.fontawesome.com/web/style/layer
