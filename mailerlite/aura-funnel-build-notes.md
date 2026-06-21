# Aura Freebie Funnel - MailerLite Build Notes

## API-created setup

MailerLite groups created on 2026-06-21:

- `190911925163394566` - Aura Freebie Subscribers
- `190911925688731169` - Soft Moon Community
- `190911926182610492` - Ebook Customers
- `190911926663906901` - Tag - Aura Interest
- `190911927182952115` - Tag - Downloaded Aura Freebie
- `190911927696754446` - Tag - Aura Funnel Completed

MailerLite does not expose a separate public tags resource in this API setup, so the tag requirements are represented as fallback groups with the `Tag -` prefix.

Automation draft created:

- `190911938543224016` - Aura Nurture Sequence — Why Do People Feel Different?

Automation structure created through the MailerLite API on 2026-06-21:

- Trigger: subscriber joins `Aura Freebie Subscribers`
- Email 1: `190918979047392265` - Your Workbook Is Ready
- Delay: `190918978596505553` - Wait for 2 days
- Email 2: `190918977974699807` - Why Some People Stay With Us
- Delay: `190918977547929328` - Wait for 2 days
- Email 3: `190918977029932741` - What If Aura Colors Aren't Fixed?
- Delay: `190918976590579347` - Wait for 2 days
- Email 4: `190918976069437020` - The Question Most Aura Articles Ignore
- Delay: `190918975627986316` - Wait for 2 days
- Email 5: `190918975158224119` - Inside The Aura Guide
- Delay: `190918974749280188` - Wait for 3 days
- Email 6: `190918974221845877` - A Small Reflection Before You Go
- Action: `190918973751035710` - Copy to Soft Moon Community
- Action: `190918973319021870` - Copy to Tag - Aura Funnel Completed

The automation is intentionally still disabled because MailerLite does not accept email body/design content through the tested API endpoints. The API accepts trigger, delays, action steps and email metadata, but the email content remains undesigned in MailerLite until edited in the dashboard.

Freebie download file on the website:

- `/downloads/why-do-people-feel-different-freebie.pdf`

Website opt-in:

- Landing page: `/aura-freebie/`
- Thank-you page: `/aura-freebie-thank-you/`
- Server-side submit endpoint: `/api/aura-freebie`

The submit endpoint is a Cloudflare Pages Function. It adds subscribers to the aura freebie groups through the MailerLite API without exposing the API token in the browser.

Cloudflare Pages must have this environment variable set in production:

- `MAILERLITE_API_TOKEN`

Wrangler could not set this automatically from this local environment because no `CLOUDFLARE_API_TOKEN` is configured for non-interactive Cloudflare access.

Important: MailerLite's public API and the tested hidden endpoints can create the automation trigger, delays, email blocks and group actions. The tested API endpoints do not write the email body/design content, so each email body still needs to be opened in the MailerLite dashboard before activation.

## Form / landing page

The website now has its own opt-in page. Creating a MailerLite-hosted landing page is optional, not required.

If a MailerLite-hosted form is created later, use this copy:

- Name: Aura Freebie Opt-In
- Headline: Why Do People Feel Different?
- Subheadline: Download the free reflection workbook on energy, presence and the people we never forget.
- Fields: email address, first name optional
- Success message: Your workbook is on its way. Please check your inbox.

Body copy:

Some people feel instantly calming.  
Some people seem magnetic.  
Some people stay with us long after they leave.

This free Soft Moon Studio workbook offers gentle reflection questions to help you explore the energy you notice in yourself and others.

CTA button:

Download The Free Workbook

After signup, add subscriber to:

- Aura Freebie Subscribers
- Tag - Aura Interest
- Tag - Downloaded Aura Freebie

Current blog CTA URL:

`/aura-freebie/?utm_source=blog&utm_medium=optin&utm_campaign=aura_freebie&utm_content=why_people_feel_different`

## Local test result

Tested locally with Cloudflare Pages dev on 2026-06-21:

- `POST /api/aura-freebie` returned `303` to `/aura-freebie-thank-you/`
- Test subscriber `softmoon.aura.test.20260621@example.com` was active in MailerLite
- Test subscriber groups:
  - Aura Freebie Subscribers
  - Tag - Aura Interest
  - Tag - Downloaded Aura Freebie
- Re-posting the same test email kept the same subscriber record, so duplicate form submits do not create duplicate subscribers.
- The dummy test subscriber was deleted after verification to avoid sending future automation emails to a fake address.

Recommended blog tracking:

`?utm_source=blog&utm_medium=optin&utm_campaign=aura_freebie&utm_content=why_people_feel_different`

## Automation

Name:

Aura Nurture Sequence — Why Do People Feel Different?

Trigger:

When subscriber joins group: Aura Freebie Subscribers

Recommended repeat setting:

Do not repeat the automation for subscribers who join the same group more than once.

Flow:

1. Email 1 - immediately
2. Wait 2 days
3. Email 2
4. Wait 2 days
5. Email 3
6. Wait 2 days
7. Email 4
8. Wait 2 days
9. Email 5
10. Wait 3 days
11. Email 6
12. Add to group: Soft Moon Community
13. Add to group: Tag - Aura Funnel Completed

Optional later buyer rule:

If Payhip or buyer tracking is connected later, exclude subscribers in `Ebook Customers` from sales emails or change the CTA copy to a customer-friendly message.

## Email 1

Timing: Immediately after signup

Subject: Your Workbook Is Ready ✨

Preview text: A gentle reflection workbook on energy and presence.

Goal: Deliver the freebie. No selling.

CTA:

- Button text: Download Workbook
- Link: `https://softmoonstudio.com/downloads/why-do-people-feel-different-freebie.pdf`

Body:

Hi,

Thank you for downloading **Why Do People Feel Different?**

I hope the questions inside help you notice something new about yourself and the people around you.

One thing I find fascinating is that many people begin exploring auras hoping to discover a color.

But often the deeper questions are:

Why do certain people feel magnetic?

Why do some people instantly feel familiar?

Why do some people seem to glow?

For now, simply enjoy the workbook slowly.

There are no right answers inside.

Only observations.

Only curiosity.

You can download your copy here:

[Download Workbook]

With love,  
Soft Moon Studio

## Email 2

Timing: 2 days after Email 1

Subject: Why Some People Stay With Us

Preview text: A soft reflection on presence, memory and energy.

Goal: Emotional connection. No ebook CTA.

Body:

Hi,

Have you ever met someone once and remembered them for years?

Not because they said something dramatic.

Not because they looked perfect.

But because something about their presence stayed with you.

Maybe they felt calming.

Maybe they felt warm.

Maybe they made you feel seen in a way you did not expect.

This is one of the ideas behind the first reflection in your workbook:

**Which people do you remember most?**

Sometimes the people we remember teach us something about the kind of energy we are drawn to.

And sometimes they show us the kind of presence we quietly hope to cultivate ourselves.

If you have a few quiet minutes today, return to Reflection 01 in the workbook.

Ask yourself:

Who tends to stay in my mind long after I have met them?

And what did their presence make me feel?

No need to overthink it.

Just notice.

If one person came to mind while reading this, you can simply write their name in your journal.

With love,  
Soft Moon Studio

## Email 3

Timing: 4 days after signup / 2 days after Email 2

Subject: What If Aura Colors Aren't Fixed?

Preview text: A gentler way to think about aura colors.

Goal: Create curiosity and send reader to the aura color blog.

CTA:

- Button text: Read: What Color Is My Aura?
- Link: `https://softmoonstudio.com/posts/what-color-is-my-aura/?utm_source=email&utm_medium=automation&utm_campaign=aura_freebie&utm_content=email_3`

Body:

Hi,

Many people first discover aura traditions by asking one question:

**What color is my aura?**

It is an understandable place to begin.

Colors give us language.

They make something invisible feel easier to explore.

But many aura traditions suggest that aura colors are not always fixed labels.

A person may carry one dominant energy for a long time.

But emotional seasons, personal growth, stress, healing and life transitions may also influence the energy they express.

That is why I like to think of aura colors less as a final answer and more as an invitation.

Not:

"What color am I forever?"

But:

"What kind of energy feels present in me right now?"

If you want to explore this idea more deeply, I wrote a full article here:

[Read: What Color Is My Aura?]

With love,  
Soft Moon Studio

## Email 4

Timing: 6 days after signup / 2 days after Email 3

Subject: The Question Most Aura Articles Ignore

Preview text: It may not be "what color am I?"

Goal: Softly introduce the paid ebook.

CTA:

- Button text: Explore Why Do Some People Seem To Glow?
- Link: `https://softmoonstudio.com/my-books/?utm_source=email&utm_medium=automation&utm_campaign=aura_ebook&utm_content=email_4`

Body:

Hi,

Most aura articles begin with one question:

**What color am I?**

And that can be a beautiful place to start.

But I think there is another question that feels even more interesting:

Why do some people seem magnetic?

Why do some people feel calming?

Why do some people seem to glow?

This is the deeper question behind the Soft Moon Studio aura guide.

Because aura traditions are not only about color.

They are also about presence.

The atmosphere someone creates.

The way people feel after spending time with them.

The energy they seem to carry into a room.

Your free workbook touches on this idea gently.

The full guide explores it more deeply.

If you feel curious, you can explore it here:

[Explore Why Do Some People Seem To Glow?]

With love,  
Soft Moon Studio

## Email 5

Timing: 8 days after signup / 2 days after Email 4

Subject: Inside The Aura Guide

Preview text: A closer look at what the full guide explores.

Goal: Sell the $4.99 ebook clearly but softly.

CTA:

- Button text: Get The Aura Guide
- Link: `https://softmoonstudio.com/my-books/?utm_source=email&utm_medium=automation&utm_campaign=aura_ebook&utm_content=email_5`

Body:

Hi,

If the reflection workbook made you curious about aura colors, energy and presence, the full guide may be the next step.

**Why Do Some People Seem To Glow?** is a soft, reflective introduction to aura traditions and the symbolic meanings behind human energy.

Inside the guide, you will discover:

- The seven main aura colors
- Traditional aura color meanings
- Why some people seem magnetic
- Whether aura colors can change
- A deeper exploration of energy and presence
- Reflection prompts to help you think about the energy you bring into the world

The guide is not designed to tell you who you are.

It is designed to help you notice yourself more deeply.

If you want to continue exploring, you can find the full guide here:

[Get The Aura Guide]

With love,  
Soft Moon Studio

## Email 6

Timing: 11 days after signup / 3 days after Email 5

Subject: A Small Reflection Before You Go

Preview text: What kind of presence are you creating?

Goal: Last soft sales email, then move to Soft Moon Community.

CTA:

- Button text: Explore The Guide
- Link: `https://softmoonstudio.com/my-books/?utm_source=email&utm_medium=automation&utm_campaign=aura_ebook&utm_content=email_6`

Body:

Hi,

Before this little aura sequence ends, I want to leave you with one final reflection.

Which question from the workbook stayed with you most?

Was it:

Which people do you remember most?

What energy do you bring into a room?

Which qualities do you admire most?

What feels most like you right now?

Sometimes one question opens a door.

And sometimes that door leads us toward a deeper understanding of ourselves.

Many people begin exploring auras because they want to know their color.

But the deeper question may be:

**What kind of presence am I creating?**

If you would like to continue exploring aura traditions, colors and the quiet mystery of why some people seem to glow, the full guide is here:

[Explore The Guide]

Thank you for being here.

With love,  
Soft Moon Studio
