import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'AI-Native Interactive Textbook',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // ✅ YOUR VERCEL URL
  url: 'https://hackathon-1.vercel.app',

  // ✅ IMPORTANT FOR VERCEL
  baseUrl: '/',

  organizationName: 'RabiaFS18',
  projectName: 'Hackathon-1',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
        },

        blog: {
          showReadingTime: true,
        },

        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    navbar: {
      title: 'AI Robotics Book',

      logo: {
        alt: 'AI Logo',
        src: 'img/logo.svg',
      },

      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },

        {
          to: '/docs/ai',
          label: 'AI Tutor',
          position: 'left',
        },

        {
          href: 'https://github.com/RabiaFS18/Hackathon-1',
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
              label: 'AI Tutor',
              to: '/docs/ai',
            },
          ],
        },

        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/RabiaFS18/Hackathon-1',
            },
          ],
        },
      ],

      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;