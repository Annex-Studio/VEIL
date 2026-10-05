# Veil Documentation Site

The Veil docs and hosted application are built with [Docusaurus](https://docusaurus.io/). The browser app source remains `../Veil.html`; the prestart and prebuild scripts copy it and its logo into `static/`. The postbuild script publishes Docusaurus output to `docs/manual/`, served at `https://annex-studio.github.io/VEIL/manual/`.

## Installation

```bash
npm install
```

## Local Development

```bash
npm run start
```

This command copies the app and starts the docs server with a local root base URL, so page styles and scripts load correctly. Open `http://localhost:3000/intro` for the guide or `http://localhost:3000/Veil.html` for the app. Do not open generated HTML files directly with `file://`; their production assets use the GitHub Pages path.

## Build

```bash
npm run build
```

This command generates static content into `build/`, including the app page and logo, then copies the site into `docs/manual/`. The overview is available at `https://annex-studio.github.io/VEIL/manual/intro.html` once GitHub Pages updates.

## Deployment

GitHub Pages serves the repository's `docs/` folder. After building, commit the generated `docs/manual/` directory along with your changes and push to the Pages source branch. Do not use `npm run deploy` for this setup, because it publishes a separate site to the `gh-pages` branch and replaces the landing-page layout.
