import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Bridging the gap between the digital brain and the physical body.',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://KULSOOMadnan.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/physical-ai-humanoid-robotics-textbook/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'KULSOOMadnan', // Usually your GitHub org/user name.
  projectName: 'physical-ai-humanoid-robotics-textbook', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
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
          // Use the new textbook sidebar
          sidebarCollapsible: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics Textbook',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Textbook Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'textbookSidebar',
          position: 'left',
          label: '📚 Textbook',
        },
        {
          type: 'dropdown',
          label: 'Modules',
          position: 'left',
          items: [
            {
              label: 'Module 1: The Robotic Nervous System (ROS 2)',
              to: '/docs/module1-ros2/module1-intro',
            },
            {
              label: 'Module 2: The Digital Twin (Gazebo & Unity)',
              to: '/docs/module2-gazebounity/module2-intro',
            },
            {
              label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
              to: '/docs/module3-nvidiaisaac/module3-intro',
            },
            {
              label: 'Module 4: Vision-Language-Action (VLA)',
              to: '/docs/module4-vla/module4-intro',
            },
          ],
        },
        {
          type: 'dropdown',
          label: '🎯 Quizzes',
          position: 'left',
          items: [
            {
              label: 'All Module Quizzes',
              to: '/docs/quizzes',
            },
            {
              label: 'Module 1 Quiz',
              to: '/docs/module1-ros2/quiz/',
            },
            {
              label: 'Module 2 Quiz',
              to: '/docs/module2-gazebounity/quiz/',
            },
            {
              label: 'Module 3 Quiz',
              to: '/docs/module3-nvidiaisaac/quiz/',
            },
            {
              label: 'Module 4 Quiz',
              to: '/docs/module4-vla/quiz/',
            },
          ],
        },
        {
          href: 'https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '📚 Textbook',
          items: [
            {
              label: 'Home',
              to: '/',
            },
            {
              label: 'Textbook Overview',
              to: '/docs/intro',
            },
            {
              label: 'Getting Started',
              to: '/docs/getting-started',
            },
            {
              label: 'Textbook Overview',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: '🎯 Quizzes & Assessments',
          items: [
            {
              label: 'All Module Quizzes',
              to: '/docs/quizzes',
            },
            {
              label: 'Module 1 Quiz',
              to: '/docs/module1-ros2/quiz/',
            },
            {
              label: 'Module 2 Quiz',
              to: '/docs/module2-gazebounity/quiz/',
            },
            {
              label: 'Module 3 Quiz',
              to: '/docs/module3-nvidiaisaac/quiz/',
            },
            {
              label: 'Module 4 Quiz',
              to: '/docs/module4-vla/quiz/',
            },
          ],
        },
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1: ROS 2',
              to: '/docs/module1-ros2/module1-intro',
            },
            {
              label: 'Module 2: Simulation',
              to: '/docs/module2-gazebounity/module2-intro',
            },
            {
              label: 'Module 3: AI-Robot Brain',
              to: '/docs/module3-nvidiaisaac/module3-intro',
            },
            {
              label: 'Module 4: VLA',
              to: '/docs/module4-vla/module4-intro',
            },
          ],
        },
        {
          title: '🔗 Resources',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook',
            },
            {
              label: 'Docusaurus Documentation',
              href: 'https://docusaurus.io/docs',
            },
            {
              label: 'Community Support',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'Contact & Feedback',
              to: '/contact',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. All rights reserved.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
