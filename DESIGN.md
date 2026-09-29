---
title: "Yasin & Tahlil Memorial Design Tokens"
version: "1.0"
status: "verified"
---

# Design Tokens

## Colors

| Token            | Value      | Usage                        |
|------------------|------------|------------------------------|
| primary          | #12211A    | Deep pine ink, backgrounds   |
| secondary        | #5C6B63    | Sage, muted elements         |
| tertiary         | #A8863F    | Antique gold, accents        |
| neutral          | #F7F3EA    | Paper, light backgrounds     |
| on-primary       | #F7F3EA    | Text on primary              |
| on-tertiary      | #12211A    | Text on tertiary             |
| muted            | #9FB3A8    | Secondary text               |
| surface-deep     | #0C1712    | Deepest background           |

## Typography

| Role      | Font              | Weights       |
|-----------|-------------------|---------------|
| Display   | Cormorant Garamond| 400, 600      |
| Arabic    | Amiri             | 400           |
| Body      | Inter             | 400, 500      |

## Radii

| Token | Value |
|-------|-------|
| sm    | 2px   |
| md    | 4px   |
| lg    | 8px   |

## Spacing

| Token | Value |
|-------|-------|
| xs    | 4px   |
| sm    | 8px   |
| md    | 16px  |
| lg    | 24px  |
| xl    | 48px  |
| xxl   | 96px  |

## Constraints

- No emoji, no PNG icons, no gradient, no glass, no glow, no drop shadow
- SVG inline icons only
- One primary button only: "Mulai"
- Arabic text always above transliteration
- Custom modal, no browser confirm()
- Manual refresh, not auto-reload
- Single page, two views (cover / booklet), JS-driven
- Booklet lazy-loads on Mulai click
- Prefers-reduced-motion respected
- WCAG AA contrast ratios
