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

`www.softmoonstudio.com` moet als alternatieve ingang bereikbaar zijn. Voeg het
eerst als custom domain toe aan hetzelfde Pages-project en maak daarna een
proxied DNS-record aan:

| Type | Naam | IPv4-adres | Proxy status |
| --- | --- | --- | --- |
| `CNAME` | `www` | `softmoonstudio.pages.dev` | Proxied |

Maak vervolgens een Bulk Redirect van `www.softmoonstudio.com` naar
`https://softmoonstudio.com` met status `301`, subpath matching en behoud van
querystrings. Controleer daarna beide ingangen met:

```sh
curl -I https://softmoonstudio.com/
curl -I https://www.softmoonstudio.com/
```

De eerste hoort `200` te geven en de tweede één `301` naar het hoofddomein.

## Beschikbaarheid en 502-controle

- Production branch: `main`
- Build command: `hugo --gc --minify`
- Output directory: `public`
- Koppel geen extra Worker of reverse proxy vóór het Pages-project.
- Laat de laatste geslaagde Pages-deployment actief wanneer een nieuwe build faalt.
- Stel een externe uptimecheck in op `/` en op een representatief artikel, elke
  vijf minuten vanuit minstens twee regio's.
- Waarschuw bij twee opeenvolgende `5xx`-responses; één losse Cloudflare-fout kan
  een tijdelijk netwerkincident zijn.
- Controleer bij een 502 eerst de Cloudflare Ray ID, Pages deployment status en
  eventuele redirect- of Worker-rules voordat DNS wordt gewijzigd.
