# Standalone SVG and image presentation

## Inline SVG sizing and color

Inline a CSS-mode exported SVG and use a shared class rather than repeating
per-icon layout rules. The exporter adds `ic-primary` / `ic-secondary` classes
only according to the actual source layers and supplies Font Awesome-compatible
CSS custom-property hooks. It does not require the Font Awesome runtime.

```css
.ic-icon {
  display: inline-block;
  height: 1em;
  width: auto;
  vertical-align: -0.125em;
  flex: none;
}
.icon-slot {
  display: inline-grid;
  place-items: center;
  inline-size: 1.5rem;
  block-size: 1.5rem;
}
.icon-accent {
  --fa-primary-color: var(--text-color);
  --fa-secondary-color: var(--accent-color);
  --fa-secondary-opacity: 1;
}
.action { display: inline-flex; align-items: center; gap: 0.5rem; }
```

```html
<button class="action" type="button">
  <span class="icon-slot icon-accent"><!-- inline the exported SVG here --></span>
  Open report
</button>
```

For an icon-only button, place the accessible action name on the button and keep
the SVG decorative. A meaningful standalone SVG gets `--title 'Meaningful name'`.
The exporter uses an accessible label without document-global IDs, avoiding title
ID collisions when several icons are inlined.

## Images, documents, and slides

Use static SVG or PNG for `<img>`, documents, and slides. External SVGs do not
inherit CSS variables from the host page. Resolve the palette to hex values
before static export. With an `<img>`, supply appropriate `alt` text or `alt=""`
when the adjacent label already says the same thing.

Full-canvas assets preserve the icon's designed surrounding space and are a good
default for image embedding. Cropped assets fit text efficiently. The selected
canvas is in the manifest. Preserve aspect ratio; set the image's height and use
automatic width unless deliberately placing a full-canvas square in a fixed slot.

The CLI `--size` is the output height in pixels. PNG preserves the canvas aspect
ratio, so a cropped icon may have a different width. Use `--canvas full` when a
square PNG is required. SVG remains scalable despite its initial dimensions.

## Motion and simple layering

Use motion to explain state or acknowledge an action. Continuous decoration can
compete with reading. A subtle feedback treatment can be plain CSS:

```css
.action:hover .ic-icon { transform: translateY(-1px); }
.ic-icon { transition: transform 160ms ease; }
@media (prefers-reduced-motion: reduce) {
  .ic-icon { animation: none !important; transition: none; transform: none; }
}
```

For a static badge or composition, position inline SVGs in a relative container
and give the whole composition one meaningful label. For native Font Awesome
transforms, masks, animated classes, counters, and layers, use the generated
SVG+JS recipes described in native-runtime.md.

Sources:
- https://docs.fontawesome.com/web/add-icons/svg-bare
- https://docs.fontawesome.com/web/style/duotone
- https://docs.fontawesome.com/web/dig-deeper/accessibility
