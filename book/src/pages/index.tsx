import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import book_cover from '@site/static/img/book-cover.png'; 
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={styles.heroContent}>
        {/* Left: Text */}
        <div className={styles.heroText}>
          <Heading as="h1" className="hero__title">{siteConfig.title}</Heading>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link className="button button--secondary button--lg" to="/docs/intro">
              Start Reading  
            </Link>
          </div>
        </div>

        {/* Right: Hero Image */}
        <div className={styles.heroImage}>
          <img src={book_cover} alt="Book Cover" />
        </div>
      </div>
    </header>
  );
}

type ModuleItem = {
  id: string;
  title: string;
  description: ReactNode;
  color: string;
  icon: string;
};

const ModuleList: ModuleItem[] = [
  {
    id: '1',
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description: (
      <>Explore ROS 2 fundamentals: architecture, nodes, topics, services, actions, and communication setup.</>
    ),
    color: 'primary',
    icon: '🧠',
  },
  {
    id: '2',
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description: (
      <>Learn to simulate robots with Gazebo & Unity, including physics, sensors, and sim-to-real transfer.</>
    ),
    color: 'secondary',
    icon: '🔄',
  },
  {
    id: '3',
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
    description: (
      <>Dive into AI for robotics: computer vision, sensor fusion, motion planning, manipulation, and reinforcement learning.</>
    ),
    color: 'success',
    icon: '🤖',
  },
  {
    id: '4',
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: (
      <>Integrate vision, language, and action; learn natural language commands, perception, HRI, and capstone project.</>
    ),
    color: 'info',
    icon: '💬',
  },
];

function Module({id, title, description, color, icon}: ModuleItem) {
  let modulePath = '';
  switch(id) {
    case '1':
      modulePath = '/docs/module1-ros2/chapter01/';
      break;
    case '2':
      modulePath = '/docs/module2-gazebounity/chapter04/';
      break;
    case '3':
      modulePath = '/docs/module3-nvidiaisaac/chapter10/';
      break;
    case '4':
      modulePath = '/docs/module4-vla/chapter12/';
      break;
    default:
      modulePath = '/docs/intro';
  }

  return (
    <div className={clsx('col col--6 margin-bottom--lg')}>
      <div className={clsx('card', `card--${color}`)}>
        <div className="card__header">
          <h3>
            <span style={{ fontSize: '1.5em', marginRight: '0.5em' }}>{icon}</span>
            {title}
          </h3>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
        <div className="card__footer">
          <Link className={clsx('button', `button--${color}`)} to={modulePath}>
            Explore Module
          </Link>
        </div>
      </div>
    </div>
  );
}

function BookIntroduction() {
  return (
    <section className={clsx(styles.bookIntro, 'margin-vert--lg')}>
      <div className="container">
        <div className="row" style={{ gap: '2rem', textAlign: 'center' }}>
          <div className="col col--12">
            <Heading as="h2">Welcome to Physical AI & Humanoid Robotics</Heading>
            <p className="text--large">
              This comprehensive textbook bridges the gap between artificial intelligence
              and physical embodiment, exploring how humanoid robots can perceive, reason,
              and act in the real world. Through four carefully structured modules,
              you'll journey from foundational concepts to cutting-edge applications
              in embodied intelligence.
            </p>
          </div>
        </div>

        <div className="row margin-vert--lg">
          <div className="col col--4">
            <div className="feature-card">
              <span className="feature-icon">🔬</span>
              <h3>The Science of Embodied AI</h3>
              <p>Understand how intelligence emerges through interaction with the physical world</p>
            </div>
          </div>
          <div className="col col--4">
            <div className="feature-card">
              <span className="feature-icon">🦾</span>
              <h3>Humanoid Design Principles</h3>
              <p>Learn the engineering behind robots designed for human environments</p>
            </div>
          </div>
          <div className="col col--4">
            <div className="feature-card">
              <span className="feature-icon">🚀</span>
              <h3>Real-World Applications</h3>
              <p>Explore practical implementations and future possibilities</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}


export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics Textbook`}
      description="A comprehensive textbook on Physical AI and Humanoid Robotics - bridging the gap between AI and embodied systems">
      <HomepageHeader />
      <main>
        <BookIntroduction />
        <section className="container padding-vert--lg">
          <div className="row">
            <div className="col col--12 text--center margin-bottom--lg">
              <Heading as="h2">Learning Modules</Heading>
              <p>Progress through our structured curriculum covering all aspects of humanoid robotics</p>
            </div>
          </div>
          <div className="row">
            {ModuleList.map((props, idx) => (
              <Module key={idx} {...props} />
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}
