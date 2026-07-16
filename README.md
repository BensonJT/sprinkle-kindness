# Sprinkle Kindness — Cookie Portfolio Website

A finished portfolio page for a decorated-sugar-cookie baker. Feminine "Soft Blush"
look (cream + blush pink, Cormorant Garamond + Nunito Sans). Sections: hero, About,
a 66-tile photo gallery with a caption under each photo, "What I Make", and an
Instagram footer.

## What's in this folder

- **`sprinkle-kindness.html`** — the complete, self-contained website. Open it in any
  browser; everything (styles, fonts, code) is inlined into this one file. This is the
  file to deploy.
- **`Sprinkle Kindness.dc.html`** + **`image-slot.js`** — the original editable source
  (optional; only needed if you want to rebuild rather than edit the bundled file).

## The task: wire up the real photos + captions

The gallery currently has **66 empty photo placeholders** (`<image-slot>` elements) and,
under each, an editable caption line. I need you to replace the placeholders with the
baker's real photos and set the captions.

There are 66 slots with ids `ck-01` through `ck-66`, plus one portrait slot `ck-portrait`
in the About section. Each lives inside a `<figure>` like this:

```html
<figure ...>
  <image-slot id="ck-01" ... placeholder="Photo 1"></image-slot>
  <figcaption class="ck-cap" contenteditable="true" data-ph="Add a caption…"></figcaption>
</figure>
```

### Recommended approach (clean, production-ready)

Put the photo files in an `images/` folder next to the HTML, then replace each
`<image-slot ...></image-slot>` with a plain image, and type the caption text into
its `<figcaption>`:

```html
<figure ...>
  <img src="images/wedding-set.jpg" alt="Bridal shower cookies"
       style="width:100%; aspect-ratio:1; object-fit:cover; border-radius:16px;
              box-shadow:0 12px 30px -20px rgba(120,70,80,0.45);">
  <figcaption class="ck-cap" ...>Blush florals for a spring bridal shower</figcaption>
</figure>
```

Do the same for the About portrait (`ck-portrait`) with `aspect-ratio:4/5`.
If there are fewer than 66 photos, just delete the extra `<figure>` blocks — the grid
reflows automatically.

I'll provide the photos and the caption text for each; match them up in order (or by the
description I give).

## Notes

- The design is **high fidelity** — keep the exact colors, fonts, spacing, and layout.
  Only swap in photos and caption text.
- Fonts are Google Fonts (Cormorant Garamond, Nunito Sans), already loaded in the file.
- Instagram link points to https://www.instagram.com/_sprinkle_kindness
- To host it: any static host works (Netlify, Vercel, GitHub Pages) — it's just one HTML
  file plus an `images/` folder.
