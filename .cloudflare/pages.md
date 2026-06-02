# Cloudflare Pages instellingen

Gebruik deze instellingen bij het aanmaken van het Cloudflare Pages-project:

- Framework preset: Hugo
- Build command: `hugo --gc --minify`
- Build output directory: `public`
- Root directory: leeg laten
- Environment variable: `HUGO_VERSION=0.162.0`

## Eigen domein koppelen

Koppel het hoofddomein via het bestaande Pages-project:

1. Open in Cloudflare `Workers & Pages`.
2. Selecteer het Pages-project voor Soft Moon Studio.
3. Open `Custom domains` en kies `Set up a custom domain`.
4. Voeg `softmoonstudio.com` toe.
5. Wacht tot het domein de status `Active` heeft.

## Oud Pages-domein doorsturen

Maak daarna in Cloudflare een account-level Bulk Redirect aan zodat bestaande
links naar `softmoonstudio.pages.dev` hun pad en trackingparameters behouden:

| Instelling | Waarde |
| --- | --- |
| Source URL | `softmoonstudio.pages.dev` |
| Target URL | `https://softmoonstudio.com` |
| Status | `301` |
| Preserve query string | aan |
| Subpath matching | aan |
| Preserve path suffix | aan |
| Include subdomains | aan |

Maak een Bulk Redirect Rule aan die deze lijst gebruikt.

Voorbeeld:

`https://softmoonstudio.pages.dev/posts/example/?utm_source=pinterest`

wordt:

`https://softmoonstudio.com/posts/example/?utm_source=pinterest`

## Optioneel: www doorsturen

Als `www.softmoonstudio.com` ook gebruikt moet kunnen worden, maak een tweede
Bulk Redirect aan van `www.softmoonstudio.com` naar `https://softmoonstudio.com`
met dezelfde opties en status `301`. Voeg in DNS ook een proxied `A`-record toe:

| Type | Naam | IPv4-adres | Proxy status |
| --- | --- | --- | --- |
| `A` | `www` | `192.0.2.1` | Proxied |
