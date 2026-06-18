---
name: Premium InsurTech System
colors:
  surface: '#faf8ff'
  surface-dim: '#d9d9e5'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f2fe'
  surface-container: '#ededf9'
  surface-container-high: '#e8e7f3'
  surface-container-highest: '#e2e1ed'
  on-surface: '#1a1b23'
  on-surface-variant: '#434655'
  inverse-surface: '#2e3039'
  inverse-on-surface: '#f0f0fb'
  outline: '#747686'
  outline-variant: '#c4c5d7'
  surface-tint: '#2151da'
  primary: '#0037b0'
  on-primary: '#ffffff'
  primary-container: '#1d4ed8'
  on-primary-container: '#cad3ff'
  inverse-primary: '#b7c4ff'
  secondary: '#565d79'
  on-secondary: '#ffffff'
  secondary-container: '#d8deff'
  on-secondary-container: '#5a627e'
  tertiary: '#424546'
  on-tertiary: '#ffffff'
  tertiary-container: '#5a5c5d'
  on-tertiary-container: '#d3d5d6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b7c4ff'
  on-primary-fixed: '#001551'
  on-primary-fixed-variant: '#0039b5'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#bec5e5'
  on-secondary-fixed: '#131a33'
  on-secondary-fixed-variant: '#3e4660'
  tertiary-fixed: '#e1e3e4'
  tertiary-fixed-dim: '#c5c7c8'
  on-tertiary-fixed: '#191c1d'
  on-tertiary-fixed-variant: '#454748'
  background: '#faf8ff'
  on-background: '#1a1b23'
  surface-variant: '#e2e1ed'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-padding: 2rem
  gutter: 1.5rem
  panel-gap: 1rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style

This design system is engineered for the high-stakes world of B2B InsurTech, where clarity, precision, and institutional trust are paramount. The aesthetic follows a **Modern Minimalism** philosophy, blending the functional rigor of Stripe with the refined finish of Apple. 

The personality is authoritative yet accessible, using expansive whitespace and a structured information hierarchy to make complex risk data feel manageable. Visual weight is used strategically to guide users through underwriting workflows, ensuring that critical data points—like risk scores and premium totals—receive immediate focus without overwhelming the interface.

## Colors

The palette is anchored by **Deep Navy Blue**, providing a stable, professional foundation for structural elements like sidebars and navigation headers. **Crisp White** serves as the primary canvas, ensuring maximum legibility and a sense of "openness" in data-heavy views.

**Electric Blue** is reserved exclusively for primary calls-to-action and active states, creating a clear interactive path for the user. Semantic colors are high-chroma for instant recognition: **Emerald Green** denotes low risk or successful validation, while **Crimson Red** highlights high-risk outliers and critical errors. Neutral grays are used for secondary text and borders to maintain a soft, low-friction environment.

## Typography

**Inter** is the sole typeface, chosen for its exceptional legibility in technical contexts. The system utilizes a tight typographic scale to maximize information density without sacrificing clarity. 

For financial figures and policy numbers, use the `data-mono` role, which leverages tabular num features to ensure columns of numbers align perfectly for easy comparison. Headlines use slight negative letter-spacing to appear more cohesive at larger sizes, while uppercase labels provide clear categorization for form fields and table headers.

## Layout & Spacing

The layout utilizes a **Fixed Dashboard Container** model. On desktop, a persistent sidebar (Deep Navy) anchors the left, while a fixed header provides global context. The main content area consists of scrollable panels that use a 12-column grid.

- **Margins:** 32px (2rem) for main containers to provide "breathing room."
- **Gutters:** 24px (1.5rem) between grid columns.
- **Panel Logic:** Content is grouped into white "cards" or "panels" with 16px gaps between them to create a modular, organized feel.
- **Responsiveness:** On tablet, the sidebar collapses into a hamburger menu. On mobile, all panels stack vertically, and container padding reduces to 16px.

## Elevation & Depth

This design system uses **Tonal Layering** and **Soft Ambient Shadows** to define hierarchy rather than heavy lines. 

- **Level 0 (Background):** Off-white (#F8F9FA) creates a soft base.
- **Level 1 (Cards/Panels):** Pure white (#FFFFFF) with a very subtle shadow (4px blur, 10% opacity) to suggest lift.
- **Level 2 (Dropdowns/Modals):** High-elevation shadows (12px blur, 15% opacity) to pull the element significantly forward.

Outlines are used sparingly—only for input fields and ghost buttons—using a low-contrast gray (#E2E8F0) to keep the UI feeling "light."

## Shapes

The shape language is consistent and approachable, utilizing a **Rounded** (8px) radius for all standard UI components including cards, buttons, and input fields. 

- **Standard Elements:** 8px (0.5rem) corner radius.
- **Small Elements (Chips/Badges):** 4px (0.25rem) or fully pill-shaped depending on the status type.
- **Interactive States:** Hovering over a card may subtly increase the shadow spread, but the corner radius remains constant to maintain grid alignment.

## Components

### Buttons & Controls
- **Primary Button:** Electric Blue background, white text, 8px radius. Heavy emphasis on the `Generate Quote` or `Save` actions.
- **Secondary Button:** Clear background with a subtle gray border; uses Electric Blue for text.
- **Toggle Switches:** "iOS-style" modern toggles. High-contrast green for 'On' states, neutral gray for 'Off'.

### Data Inputs
- **Input Fields:** White background, 1px light gray border. On focus, the border transitions to Electric Blue with a soft blue outer glow (ring).
- **Checkboxes:** Square with 4px radius; Electric Blue fill with a white checkmark when active.

### Dashboard Specifics
- **Risk Cards:** White panels containing the composite risk score. The score is displayed in a circular gauge with a stroke thickness of 4px.
- **Data Tables:** Row-based layouts with no vertical dividers. Use subtle zebra-striping (#F8F9FA) on hover to help the eye track across long rows of data.
- **Status Badges:** Soft-colored backgrounds with high-contrast text (e.g., Light Green background with Dark Green text) for "Auto Approved" or "Flagged" states.