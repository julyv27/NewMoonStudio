---
name: soft-moon-studio-affiliate-blog
description: Create or update Soft Moon Studio blog articles that include Amazon affiliate products. Use when writing, editing, reviewing, or publishing an article with Amazon links in the Soft Moon Studio workspace. Enforce the site's disclosure, product-card shortcode, visual style, image-sourcing rules, and concise reader-first affiliate copy.
---

# Soft Moon Studio Affiliate Blog

Use this workflow whenever a Soft Moon Studio article contains an Amazon affiliate link.

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

## Product Card Pattern

Use:

```text
{{< affiliate-product title="Product Name" whyFits="One short reader-focused benefit." image="/img/blog/relevant-lifestyle-image.jpg" imageAlt="Accurate description as lifestyle inspiration" url="AMAZON_AFFILIATE_URL" cta="View on Amazon" >}}
```

Rules:

- Keep `whyFits` to one short sentence.
- Describe fit and context, not unsupported results.
- Use the CTA `View on Amazon`.
- Let the shortcode show `Soft Moon Studio pick` and `Affiliate link`.
- Use a relevant owned or properly licensed lifestyle image.
- If an image is contextual rather than the exact product, make the alt text clear by adding `as lifestyle inspiration`.
- The shortcode visibly labels card images as `Lifestyle inspiration`.
- Do not download and re-upload Amazon product images. Only use Amazon product imagery through an officially permitted method.
- Do not generate an image that could mislead readers into believing it shows the exact recommended product.

## Review Checklist

- Article has `affiliate: true`.
- Every Amazon link uses the shortcode.
- Product card has image, accurate alt text, one short `whyFits` sentence, CTA, and affiliate URL.
- Wellness copy avoids medical promises and unsupported claims.
- Disclosure appears on the live article.
- Buttons render correctly on desktop and mobile.
