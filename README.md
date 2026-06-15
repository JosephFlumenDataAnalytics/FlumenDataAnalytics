# Flumen Data Analytics Platform

**Live site: [flumendataanalytics.com](https://flumendataanalytics.com)**

A production-deployed analytics consulting platform that delivers live, embedded Metabase dashboards to business clients. Built and deployed end to end from a minimal Flask scaffold, with no prior web development experience.

## Stack

- **Backend:** Python, Flask, Jinja2 templating
- **Frontend:** HTML, CSS, Bootstrap 5
- **Embedding:** Metabase SDK (self-hosted), JWT signed embedding
- **Server:** Ubuntu 24, DigitalOcean Droplet
- **Web server:** nginx (reverse proxy)
- **SSL:** Let's Encrypt via Certbot (auto-renewing)
- **Process management:** systemd service

## Features

- Fully deployed production site served over HTTPS at a custom domain
- Live interactive Metabase dashboard embedded via signed JWT tokens, including tooltips and filters
- Automated onboarding pipeline where client contract acceptance triggers server-side database provisioning and dashboard generation
- Pricing section with four service tiers
- Data privacy section with Colorado Privacy Act compliance language
- SEO meta tags, canonical URL configuration, and Google Search Console sitemap integration
- www to non-www redirect via nginx
- Responsive layout with scroll-reveal animations and a sticky navbar

## Architecture

```
flumendataanalytics.com (Namecheap DNS)
        |
        v
nginx (reverse proxy, SSL termination)
        |
        v
Flask app (port 5000, systemd service)
        |
        |-- /                      renders analytics/index.html
        |-- /analytics             renders analytics/index.html
        |-- /analytics/token/<n>   generates signed JWT for Metabase embed
        |-- /sitemap.xml           serves XML sitemap for Google indexing
                |
                v
        dashboard.flumendataanalytics.com
        (self-hosted Metabase, Docker, port 3000)
```

## Project Structure

```
run.py                          Flask entry point
app/
  __init__.py                   App factory, blueprint registration
  routes/
    flumen_site.py              Main site routes including sitemap
    analytics.py                Dashboard token endpoint, JWT signing
templates/
  flumen_site/
    base.html                   Master layout, navbar, SEO meta tags
    index.html                  Scaffold homepage
  analytics/
    index.html                  Main page: hero, dashboard, pricing, privacy
```

## Metabase Embedding

Dashboards are embedded using Metabase's signed embedding SDK. Rather than hardcoding a JWT token (which expires in ten minutes), Flask generates a fresh signed token on every page load via the `/analytics/token/<slot>` endpoint. The page fetches the token in JavaScript and passes it to the `<metabase-dashboard>` web component at runtime.

```python
payload = {
    "resource": {"dashboard": dashboard_id},
    "params": {},
    "iat": now,
    "exp": now + 600,
    "_embedding_params": embedding_params
}
token = jwt.encode(payload, METABASE_EMBED_SECRET, algorithm="HS256")
```

## Deployment

The app runs as a systemd service on a DigitalOcean Ubuntu droplet behind nginx as a reverse proxy. SSL is handled by Let's Encrypt with automatic renewal via Certbot. DNS is managed through Namecheap with records for the main domain, the www redirect, the Metabase subdomain, and ProtonMail.

## Summary

Starting from a basic Flask scaffold with two placeholder routes and no front end, and with no prior web development experience, I built and deployed:

- The full front end, including layout, typography, color scheme, animations, and responsive behavior
- The Metabase JWT embedding system
- All server infrastructure, including nginx configuration, SSL, DNS management, and the systemd service
- SEO configuration, including meta tags, canonical URLs, sitemap, and Google Search Console integration
- Google Business Profile setup for organic search visibility
