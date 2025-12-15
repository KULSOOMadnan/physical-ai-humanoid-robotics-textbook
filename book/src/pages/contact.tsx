import React from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';

function ContactPage() {
  return (
    <Layout title="Contact" description="Get in touch with the Physical AI & Humanoid Robotics Textbook team">
      <div className={clsx('container margin-vert--lg padding-vert--lg')}>
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h1 className="text--center">Contact & Feedback</h1>
            <div className="text--center margin-vert--lg">
              <p>
                We'd love to hear from you about the Physical AI & Humanoid Robotics Textbook.
              </p>

              <div className="margin-vert--lg">
                <h2>Provide Feedback</h2>
                <p>
                  Your feedback helps us improve the textbook for future learners.
                </p>
                <a
                  className="button button--primary button--lg margin-horiz--md"
                  href="https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Report Issues
                </a>
                <a
                  className="button button--secondary button--lg margin-horiz--md"
                  href="https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook/discussions"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Start Discussion
                </a>
              </div>

              <div className="margin-vert--lg">
                <h2>Contribute</h2>
                <p>
                  Interested in contributing to the textbook? We welcome contributions from the community.
                </p>
                <a
                  className="button button--info button--lg"
                  href="https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Contribute on GitHub
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default ContactPage;