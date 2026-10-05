import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    index: '01',
    title: 'Hosted web app',
    label: 'NO INSTALL',
    description: (
      <>
        Open the browser workspace at the project site. Encoding and decoding happen in your browser.
      </>
    ),
    link: 'https://annex-studio.github.io/VEIL/Veil.html',
    linkText: 'Launch Veil',
  },
  {
    index: '02',
    title: 'Python CLI',
    label: 'LOCAL TERMINAL',
    description: (
      <>
        Run the interactive terminal app for text disguise, decoding, image hiding, and image reveal.
      </>
    ),
    link: '/cli',
    linkText: 'CLI setup',
  },
  {
    index: '03',
    title: 'Self-host',
    label: 'YOUR DEPLOYMENT',
    description: (
      <>
        Build the static site and publish it on a host you control, including its direct Veil app URL.
      </>
    ),
    link: '/self-hosting',
    linkText: 'Build and deploy',
  },
];

function Feature({index, label, title, description, link, linkText}) {
  return (
    <article className={clsx('col col--4', styles.column)}>
      <div className={styles.accessItem}>
        <div className={styles.meta}><span>{index}</span><span>{label}</span></div>
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
        <Link className={styles.accessLink} to={link}>{linkText}<span aria-hidden="true">↗</span></Link>
      </div>
    </article>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.access} aria-label="Ways to use Veil">
      <div className="container">
        <div className={styles.grid}>
          {FeatureList.map((props, idx) => (
            <Feature key={props.index} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
