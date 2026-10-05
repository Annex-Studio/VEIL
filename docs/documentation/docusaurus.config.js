// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

import {themes as prismThemes} from 'prism-react-renderer';

const isDevServer = process.env.npm_lifecycle_event === 'start' ||
  process.argv.some((arg) => arg === 'start');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Veil',
  tagline: 'Encrypted communication with cover',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://annex-studio.github.io',
  
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: process.env.VEIL_DOCS_BASE_URL || (isDevServer ? '/' : '/VEIL/manual/'),

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'annex-studio', // Usually your GitHub org/username.
  projectName: 'VEIL', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
          editUrl: 'https://github.com/annex-studio/VEIL/tree/main/docs/documentation/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Veil',
        logo: {
          alt: 'Veil Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://annex-studio.github.io/VEIL/Veil.html',
            label: 'Open Veil',
            position: 'right',
          },
          {
            href: 'https://github.com/annex-studio/VEIL',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Getting Started',
                to: '/',
              },
            ],
          },
          {
            title: 'Project',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/annex-studio/VEIL',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Veil by Annex Studio. Documentation built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;