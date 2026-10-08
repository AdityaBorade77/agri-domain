---
name: Kisan Earth
colors:
  surface: '#eefdf3'
  surface-dim: '#cfded4'
  surface-bright: '#eefdf3'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#e8f7ed'
  surface-container: '#e2f2e7'
  surface-container-high: '#ddece2'
  surface-container-highest: '#d7e6dc'
  on-surface: '#111e18'
  on-surface-variant: '#504440'
  inverse-surface: '#26332d'
  inverse-on-surface: '#e5f4ea'
  outline: '#82746f'
  outline-variant: '#d4c3bd'
  surface-tint: '#7a5649'
  primary: '#5f3e32'
  on-primary: '#ffffff'
  primary-container: '#795548'
  on-primary-container: '#fdcdbc'
  inverse-primary: '#ebbcac'
  secondary: '#2c694e'
  on-secondary: '#ffffff'
  secondary-container: '#aeeecb'
  on-secondary-container: '#316e52'
  tertiary: '#2c4c3b'
  on-tertiary: '#ffffff'
  tertiary-container: '#446452'
  on-tertiary-container: '#bbdfc8'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbcf'
  primary-fixed-dim: '#ebbcac'
  on-primary-fixed: '#2e150b'
  on-primary-fixed-variant: '#603f33'
  secondary-fixed: '#b1f0ce'
  secondary-fixed-dim: '#95d4b3'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#0e5138'
  tertiary-fixed: '#c7ebd4'
  tertiary-fixed-dim: '#abcfb8'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#2d4d3c'
  background: '#eefdf3'
  on-background: '#111e18'
  surface-variant: '#d7e6dc'
typography:
  display:
    fontFamily: Bricolage Grotesque
    fontSize: 2.75rem
    fontWeight: '800'
    lineHeight: 3.25rem
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Bricolage Grotesque
    fontSize: 2.125rem
    fontWeight: '800'
    lineHeight: 2.5rem
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Bricolage Grotesque
    fontSize: 2rem
    fontWeight: '700'
    lineHeight: 2.5rem
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Bricolage Grotesque
    fontSize: 1.625rem
    fontWeight: '700'
    lineHeight: 2.125rem
    letterSpacing: 0em
  headline-md:
    fontFamily: Bricolage Grotesque
    fontSize: 1.375rem
    fontWeight: '700'
    lineHeight: 1.875rem
  headline-sm:
    fontFamily: Bricolage Grotesque
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.625rem
  body-lg:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: 1.75rem
  body-md:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-sm:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.375rem
  label-lg:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 1.0625rem
    fontWeight: '700'
    lineHeight: 1.5rem
    letterSpacing: 0.01em
  label-md:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 0.9375rem
    fontWeight: '600'
    lineHeight: 1.375rem
  label-sm:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 0.8125rem
    fontWeight: '600'
    lineHeight: 1.125rem
    letterSpacing: 0.02em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.375rem
  space-sm: 0.75rem
  space-md: 1.25rem
  space-lg: 1.75rem
  space-xl: 2.5rem
---

## Brand & Style

This design system is crafted specifically for agricultural communities navigating digital tools directly in the field, under direct, blinding sunlight and amidst practical physical work. The brand persona bridges grounded pastoral intuition with crisp, modern utility: deeply respectful of agrarian tradition, unpretentious, resilient, and utterly trustworthy.

The design movement mixes **High-Contrast Utilitarianism** with **Earthy Tactile Modernism**:
- **Sunlight Resilience:** High-clarity contrast rules over low-contrast subtleties. Surfaces rely on earthy warmth rather than sterile whites to reduce eye strain under bright skies.
- **Dignified Functionality:** Avoid delicate ornamentation, artificial glassmorphism, or synthetic neon. Instead, visual weight is carried by sturdy loam tones, deep forest greens, and solid, confidence-inspiring tap areas.
- **Approachability:** The typography pairs the expressive humanist warmth of Bricolage Grotesque in headlines with the hyper-differentiated optical clarity of Atkinson Hyperlegible Next for critical data, pricing, weather telemetry, and multilingual rendering.

## Colors

The palette directly reflects the working soil, crop foliage, and bright open environment of rural operations:

- **Primary (`#795548`):** Deep, fertile loam earth. Used for foundational anchors, authoritative buttons, structural badges, and primary grounding accents.
- **Secondary (`#2D6A4F`):** Vigorous, natural leaf green. Dedicated to affirmative primary action flows (buy inputs, confirm harvest dates, submit advisory requests, call Kisan support).
- **Tertiary (`#1B3B2B`):** Deep shadowed forest evergreen. Reserved for high-priority headlines, key metrics, and primary text content, ensuring an unbroken contrast ratio above 7:1 against light canvas backings.
- **Neutral (`#5A6860`):** Muted sage silt. Used for secondary labels, metadata, inactive indicators, and unselected component outlines.
- **Base Canvas & Card Surfaces:**
  - Screen Background: `#FBF9F5` (warm sun-bleached chalk).
  - Elevated Card Base: `#F4EFE6` (sun-dried grain tier 1).
  - Nested Surface / Field Container: `#EFE9DC` (parchment tier 2).

### Outdoor High-Contrast Rules
- Never use text lighter than `#5A6860` on any light background.
- Primary buttons prioritize deep leaf green `#2D6A4F` or loam earth `#795548` with crisp `#FFFFFF` text to maintain legible clarity when screens are dimmed or covered in glare.
- Error states utilize a rich rust red (`#9E2A2B`), avoiding neon reds that wash out under sunlight.

## Typography

The type system prioritizes unambiguous glyph recognition for users who may have mild visual impairments or are operating phones one-handed on tractors and uneven fields:

- **Headlines (Bricolage Grotesque):** Expressive, earthy, slightly idiosyncratic curvature that feels approachable, handcrafted, yet structurally sound. Headline weights are kept bold (`600`–`800`) to punch through glare.
- **Body & Labels (Atkinson Hyperlegible Next):** Hyper-distinct character forms (such as differentiated zero vs. capital O, distinct 1, l, and I) prevent dangerous misunderstandings of fertilizer doses, market mandi rates, and crop acreages.
- **Language Equivalence:** When rendering Devanagari script, sizes must remain strictly proportional to Atkinson Hyperlegible Next body metrics, ensuring baseline stability and unobstructed matra accents.

## Layout & Spacing

Field use demands an architecture centered on single-column hand thumb zones, forgiving touch targets, and generous vertical clearance:

- **Grid Architecture:** 
  - Mobile (≤640px): 4-column fluid layout with `1rem` margins and `1rem` gutters. All primary action flows remain full-width.
  - Tablet (641px–1024px): 8-column layout with `1.5rem` margins and `1rem` gutters.
  - Desktop (>1024px): 12-column layout capped at `1200px` max-width with `2rem` margins and `1.5rem` gutters.
- **Field Ergonomics:** Minimum interactive hit targets are set to **52px × 52px** (exceeding standard 48px guidelines) to allow effortless interaction with soil-dusted fingers or work gloves.
- **Rhythm:** Spacing expands linearly using the token scale. Tight internal padding (`space-xs`, `space-sm`) binds paired indicators (e.g., unit label + rate), while wide breathing room (`space-md`, `space-lg`) demarcates independent agricultural operations.

## Elevation & Depth

To avoid optical clutter under harsh natural light, elevation is created via **warm tonal layering** supplemented by **soft organic ambient diffusion**:

- **No Artificial Glows or Glass:** Blurs, translucent backdrops, and artificial cyan/violet drop shadows are prohibited; they wash out instantly outdoors.
- **Ground Tier (Canvas):** `#FBF9F5` serves as the baseline earth level.
- **Level 1 (Card & Content Tier):** Solid `#F4EFE6` backed by a gentle, warm loam-tinted shadow: `0 3px 12px -2px rgba(121, 85, 72, 0.08)`. This creates subtle depth without dirty borders.
- **Level 2 (Interactive Floating / Active Sheets):** `#FFFFFF` or `#EFE9DC` backed by `0 8px 24px -4px rgba(27, 59, 43, 0.12)`.
- **Structural Separation:** Where low-light conditions require definition without shadows, use a 1.5px solid border in `#E4DCD0` to cleanly separate modules.

## Shapes

The shape system embraces organic, comfortable pill curvature (`roundedness: 3`), echoing smooth river pebbles, seeds, and natural landscape contours:

- **Standard Elements (Pills):** Base interactive elements (chips, inputs, primary buttons) use full `1rem` (16px) to full-pill radii.
- **Cards & Surfaces (`rounded-lg`):** Content containers feature generous `2rem` (32px) radii, giving the UI a welcoming, non-intimidating posture that invites physical interaction.
- **Modal Sheets (`rounded-xl`):** Bottom action sheets and hero status modules employ `3rem` (48px) top radiuses to visually cradle content.

## Components

### Buttons
- **Primary Action (Foliage Green):** Background `#2D6A4F`, text `#FFFFFF`, minimum height `56px`, pill-shaped (`roundedness: 3`). Active state darkens to `#1B3B2B`.
- **Secondary Action (Loam Earth):** Background `#795548`, text `#FFFFFF`, minimum height `56px`.
- **Tertiary / Utility (Parchment Outlined):** Background `#F4EFE6`, border `1.5px solid #8D6E63`, text `#1B3B2B`.
- **Micro-haptics:** All buttons must contain an icon paired with bold text to assist rapid non-textual comprehension.

### Chips & Tags
- **Filter Chips:** Height `44px`, radius `9999px` (pill). Inactive: `#EFE9DC` background with `#5A6860` text. Selected: `#1B3B2B` background with `#FFFFFF` text.
- **Agronomic Status Tags:** 
  - *Healthy / Ready:* `#E8F3ED` background with `#2D6A4F` text.
  - *Advisory / Alert:* `#FDF3E7` background with `#B45309` text.
  - *Hazard / Soil Pest:* `#FBEBEB` background with `#9E2A2B` text.

### Form Inputs
- **Text & Numeric Inputs:** Minimum height `56px`, background `#F4EFE6`, radius `1rem`, border `2px solid transparent`. On focus: background `#FFFFFF`, border `2px solid #2D6A4F`. 
- **Large Typography:** Numeric fields for crop pricing, acreages, and quantities use `1.25rem` font weight `600` to prevent transcription errors.
- **Persistent Helper Icons:** Always pair inputs with a relevant trailing voice-input or numeric stepper icon.

### Checkboxes & Radio Buttons
- **Dimensions:** Sized generously at `28px × 28px` with an expanded tap target of `52px`.
- **Visuals:** Radio circles and checkboxes use a `2.5px` border in `#5A6860`. When active, fill with `#2D6A4F` featuring a solid `#FFFFFF` checkmark or inner pip.

### Lists & Activity Rows
- **Layout:** Divided by `1.5px` solid `#EFE9DC` instead of hairline grays.
- **Structure:** Left-aligned iconography in a circular container (`44px`, `#EFE9DC`), high-contrast title (`#1B3B2B`), and large status pill on the trailing side.

### Cards
- **Base Card:** Built with `#F4EFE6` background, `2rem` rounded corners, and `1.25rem` internal padding. 
- **Field Metric Cards:** Highlighting weather, irrigation windows, or mandi prices. The top section presents large key figures (`display-mobile` in `#1B3B2B`), followed by a supporting label in `#5A6860` and an illustrative pictorial badge.

### Specialized Agricultural Components
- **Voice-First Floating Action Bar:** Fixed pill dock at bottom center of the mobile screen featuring an omni-present microphone trigger in `#2D6A4F` to accommodate dialect-driven voice search across regional farming queries.
- **Offline Sync Banner:** A persistent, high-contrast banner in `#795548` with `#FFFFFF` text indicating cached regional advisory data when network drops in rural blindspots.