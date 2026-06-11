# More Guides cross-sell + multi-buy — locked spec (2026-06-12)

Roundtable verdict: Musk/Munger/Cialdini/Kahneman/Kennedy — see session notes.

## Strategy
- Hero = the reader completing the system for the goal they just declared (the book they're on).
- Mechanism: curated complements ("pairs best with"), NOT bestsellers. 4 cards, first card flagged "Pairs best".
- Offer ladder (always-on, auto-applied, max two tiers — Munger):
  - 2 single guides → 10% off all singles
  - 3+ single guides → 20% off all singles
  - All-7 bundle $129 stays best per-book ($18.43) and is EXCLUDED from % discounts.
- Framing (Kahneman): at 2 books show dollars saved; at 3+ show per-guide price. Bundle anchor $181.93 strikethrough stays.
- Cart nudge bar (Cialdini consistency + loss aversion): 1 single → "add 1 more, save 10% on both"; 2 → "add a 3rd, save 20% on all"; 3+ no bundle → upgrade line to $129 bundle; bundle present → "Best value unlocked".
- Discount must compute client-side in ONE function and flow into the mailto checkout body (Musk: single source of truth, no mispriced orders).

## Curation map (complements, first = pairs-best)
- fuel → mealprep, flexible, protein, inflammation
- muscle-code → protein, mealprep, fuel, flexible
- protein → muscle-code, mealprep, flexible, fuel
- mealprep → fuel, protein, flexible, femme-slimdown
- flexible → fuel, mealprep, protein, femme-slimdown
- inflammation → fuel, mealprep, protein, flexible
- femme-slimdown → mealprep, flexible, fuel, inflammation

## Section architecture (per ebook page)
1. Head: eyebrow "Complete your toolkit", h2 "Pairs well with this guide.", one bespoke line per book on why these four.
2. Deal ribbon: "Any 2 — save 10% · Any 3+ — save 20% · applied automatically"
3. 4 complement cards (existing .book system, "Pairs best" flag on card 1)
4. Bundle strip (dark): all 7 for $129 · $18.43/guide · best value + View bundle CTA.

## Verify gates
- Math: 2 singles = $46.78 (−$5.20); 3 = $62.38 ($20.79/guide); bundle untouched at $129.
- Mailto body contains discount line + correct total.
- Bundle-only cart → no % discount.
- Mobile 390px clean. Reads bespoke, not template.
