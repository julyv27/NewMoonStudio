This app is used by Soft Moon Studio to publish owned organic Pinterest content
to the authenticated Soft Moon Studio business account.

The app authenticates the user through Pinterest OAuth using the redirect URI
`http://localhost:8080/callback`. It requests only the scopes needed for this
workflow: `boards:read`, `pins:read`, `pins:write` and `user_accounts:read`.

After authentication, the app verifies the connected Pinterest business account,
retrieves the user's boards, and prepares an organic Pin with a selected board,
title, description, destination URL and public image URL. The app is intended
only for publishing Soft Moon Studio's own content to the Soft Moon Studio
Pinterest account.

The demo video shows:

1. OAuth authentication and requested scopes.
2. The connected Soft Moon Studio business account.
3. Pinterest boards returned by the API.
4. A Pin payload with board, title, description, link and image URL.
