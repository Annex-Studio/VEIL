import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import styles from './index.module.css';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Veil is a privacy-first browser app for encrypted messages and image steganography.">
      <main>
        <header className={styles.hero}>
          <div className={styles.heroInner}>
            <div className={styles.heroCopy}>
              <p className={styles.eyebrow}>Local privacy workspace</p>
              <Heading as="h1">Veil</Heading>
              <p className={styles.lede}>
                Encrypt a message or image, then carry it as ordinary-looking text or inside a picture.
                The secret stays on your device while Veil transforms it.
              </p>
              <div className={styles.actions}>
                <a className={styles.primaryAction} href="https://annex-studio.github.io/VEIL/Veil.html">
                  Open Veil in your browser
                </a>
                <Link className={styles.secondaryAction} to="/intro">
                  Read the overview
                </Link>
              </div>
              <p className={styles.releaseNote}>No account. No upload. Keep the password separate.</p>
            </div>
            <aside className={styles.signal} aria-label="Veil's three browser workflows">
              <div className={styles.signalHeader}><span>WORKFLOWS</span><span>01—03</span></div>
              <div className={styles.signalRow}><b>01</b><span>Text <i>to</i> chatter</span><strong>WRITE</strong></div>
              <div className={styles.signalRow}><b>02</b><span>Image <i>to</i> chatter</span><strong>IMAGE</strong></div>
              <div className={styles.signalRow}><b>03</b><span>Secret <i>inside</i> image</span><strong>STEGO</strong></div>
              <div className={styles.signalFoot}>AES-GCM ENCRYPTION UNDERNEATH</div>
            </aside>
          </div>
        </header>
        <section className={styles.accessSection}>
          <div className={styles.sectionHeading}>
            <p className={styles.eyebrow}>Choose your route</p>
            <Heading as="h2">Three ways to use Veil</Heading>
          </div>
        </section>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
