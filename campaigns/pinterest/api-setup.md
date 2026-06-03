# Pinterest API Setup

Trial access is active for `softmoonstagingapp`.

## Current Trial Access Limitation

Pinterest documents that Pins created with Trial access are visible only to the
creator. Use this phase for API testing, board lookup and the first controlled
test Pin. Public automated publishing requires Standard access.

## Required Scopes

Use the minimum scopes needed for organic content testing:

- `boards:read`
- `pins:read`
- `pins:write`

Add `boards:write` only if the tool needs to create boards.

## Local Secret Setup

Do not paste tokens into chat and do not commit them.

Create a local `.env` file from `.env.example`, then fill in:

```text
PINTEREST_ACCESS_TOKEN=...
PINTEREST_API_BASE=https://api.pinterest.com/v5
```

Load it in the terminal:

```bash
set -a
source .env
set +a
```

## Smoke Tests

Check the connected account:

```bash
python3 scripts/pinterest_api.py me
```

List boards and IDs:

```bash
python3 scripts/pinterest_api.py boards
```

Dry-run the emotional-safety context Pin:

```bash
python3 scripts/pinterest_api.py create-pin \
  --board "Calm Home Aesthetic" \
  --title "How to Make Your Home Feel Emotionally Safer" \
  --description "Small changes in lighting, evening rituals and atmosphere can help your home feel calmer, softer and easier to rest in. Explore simple cozy home ideas for creating a more emotionally safe space. This post contains affiliate links. #CalmHome #SoftLiving #CozyHome" \
  --link "https://softmoonstudio.com/posts/how-i-made-my-home-feel-emotionally-safe/?utm_source=pinterest&utm_medium=organic&utm_campaign=emotional_safety_home&utm_content=context_pin_01" \
  --image-url "https://softmoonstudio.com/img/pinterest/emotional-safety-home/context-pin-01.png" \
  --dry-run
```

Remove `--dry-run` only when the payload looks correct.

## Standard Access Prep

Pinterest requires a recording of the OAuth flow even if the app is for one
owner account. After Trial testing works, record:

1. App opens OAuth authorization.
2. Account grants scopes.
3. Tool lists boards.
4. Tool creates one test Pin.
