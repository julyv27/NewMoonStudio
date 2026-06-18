---
name: soft-moon-studio-affiliate-blog
description: Create or update Soft Moon Studio blog articles that include Amazon affiliate products, Payhip ebooks, or other monetized offers. Use when writing, editing, reviewing, or publishing a commercial Soft Moon Studio article or article-assisted funnel. Enforce disclosure, shortcode use, visual style, image-sourcing rules, concise reader-first affiliate copy, and respectful conversion strategy for spiritual, astrology, wellness, home, and lifestyle content.
---

# Soft Moon Studio Affiliate Blog

Use this workflow whenever a Soft Moon Studio article contains an Amazon affiliate link, Payhip ebook CTA, or other monetized recommendation.

## Required Article Setup

1. Add `affiliate: true` to the article front matter.
2. Use `layouts/shortcodes/affiliate-product.html` for every Amazon product. Do not add bare Amazon text links.
3. Keep affiliate products relevant to the article. Do not turn reflective articles into dense product lists.
4. Confirm the live page after publishing.

The article template automatically shows this small disclosure above the body when `affiliate: true`:

```text
As an Amazon Associate, I earn from qualifying purchases.
```

The product shortcode automatically adds `rel="nofollow noopener sponsored"` and a visible `Affiliate link` note.

When an exact Amazon affiliate URL is not available yet, use the same shortcode with `affiliate="false"`, a descriptive `eyebrow`, and the CTA `Browse options on Amazon`. This renders a visible `Product link` note and omits `sponsored`. Replace the temporary URL with a specific SiteStripe affiliate URL before treating the card as a Soft Moon Studio pick.

## Product Card Pattern

Use:

```text
{{< affiliate-product title="Product Name" whyFits="One short reader-focused benefit." image="/img/blog/relevant-product-image.jpg" imageAlt="Accurate image description" imageLabel="Product image" url="AMAZON_AFFILIATE_URL" cta="View on Amazon" >}}
```

Rules:

- Keep `whyFits` to one short sentence.
- Describe fit and context, not unsupported results.
- Use the CTA `View on Amazon`.
- Let the shortcode show `Soft Moon Studio pick` and `Affiliate link`.
- For a temporary non-affiliate Amazon browse link, set `affiliate="false"` and use a neutral eyebrow such as `Cozy lighting idea`.
- Use a relevant owned or properly licensed lifestyle image.
- The visible subject of the image must match the recommended product type. For example, never use a salt-lamp image for a linen-lamp card.
- Omit the image parameter when no honest, relevant image is available. A text-only card is better than a misleading image.
- If an image is contextual rather than the exact product, make the alt text clear by adding `as lifestyle inspiration`.
- Set `imageLabel="Product image"` for an exact product image. Omit `imageLabel` for contextual imagery so the shortcode shows `Lifestyle inspiration`.
- Do not download and re-upload Amazon product images. Only use Amazon product imagery through an officially permitted method.
- Do not generate an image that could mislead readers into believing it shows the exact recommended product.

## Review Checklist

- Article has `affiliate: true`.
- Every Amazon link uses the shortcode.
- Product card has image, accurate alt text, one short `whyFits` sentence, CTA, and affiliate URL.
- Wellness copy avoids medical promises and unsupported claims.
- Disclosure appears on the live article.
- Buttons render correctly on desktop and mobile.

## Digital Product and Ebook CTAs

Use `layouts/shortcodes/ebook-cta.html` for Payhip ebooks and other Soft Moon Studio digital guides. Do not use bare Payhip links as the main conversion element.

For astrology and spiritual digital products:

- Keep the promise reflective and educational. Do not imply certainty, prediction, diagnosis, healing, wealth, love outcomes, or guaranteed transformation.
- Connect the offer to the reader's current question. For example, a Moon sign article should frame the guide around understanding the Sun, Moon, and Rising Sign together.
- Use the ebook cover or a truthful preview image whenever possible. Set accurate `imageAlt`.
- Place CTAs at natural decision points rather than only at the end.
- Use UTM parameters when the same ebook appears more than once in an article, so placement performance can be measured.
- Vary CTA titles and descriptions by placement. Repeating the same block three times reads like an ad, not guidance.

Recommended CTA placement for an informational astrology article:

1. Early contextual CTA after the opening problem or reader-recognition moment.
2. Middle CTA after the article has explained a meaningful concept and the reader wants the next layer.
3. Bottom CTA after the conclusion, before or near "Where to go next."

Use:

```text
{{< ebook-cta label="Astrology ebook" title="Reader-facing benefit" description="One concise sentence connecting the guide to this article's question." image="/img/books/your-zodiac-sign-was-never-meant-to-explain-you.png" imageAlt="Cover of the Soft Moon Studio astrology guide Your Zodiac Sign Was Never Meant To Explain You" url="https://payhip.com/b/od2Ol?utm_source=softmoonstudio&utm_medium=blog&utm_campaign=astrology_ebook&utm_content=PLACEMENT" cta="Explore the Guide" >}}
```

Review checklist for ebook CTAs:

- The article contains enough value before asking for a click.
- CTA placement matches reader intent and does not interrupt a fragile or sensitive section.
- The cover renders on desktop and mobile.
- Payhip URL works and includes UTM parameters when useful.
- Copy avoids unsupported spiritual or wellness claims.
