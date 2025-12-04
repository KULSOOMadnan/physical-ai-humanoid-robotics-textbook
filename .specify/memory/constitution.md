<!--
Sync Impact Report:
Version change:  → 1.0.0
List of modified principles:
  - Structured Knowledge Transfer: New
  - Practical Application: New
  - Reader-Centric Design: New
  - Maintainability: New
  - Deployment Excellence: New
Added sections:
  - Key Standards & Constraints
  - Development Workflow & Quality Checklist
Removed sections:
  - (None explicitly, but the template's generic principles 6 and their descriptions are replaced)
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Original adoption date unknown.
-->
# Technical Book Creation using Docusaurus and Spec-Kit Plus Constitution

## Core Principles

### Structured Knowledge Transfer
Content must be organized logically with clear progression from fundamentals to advanced concepts.

### Practical Application
Every theoretical concept should include real-world examples, code snippets, or practical demonstrations.

### Reader-Centric Design
Write for the target audience with appropriate technical depth and clear explanations.

### Maintainability
Documentation and code must be easy to update, extend, and version-control.

### Deployment Excellence
Book must be accessible, fast-loading, and properly configured for GitHub Pages.

## Key Standards & Constraints

### Content Quality
-   **Clarity:** Technical explanations must be clear, concise, and jargon-free where possible.
-   **Accuracy:** All technical information, code examples, and commands must be tested and verified.
-   **Consistency:** Maintain uniform terminology, formatting, and style throughout the book.
-   **Completeness:** Each chapter should be self-contained while building on previous chapters.

### Documentation Structure
-   **Docusaurus Framework:** Use Docusaurus v3.x+ for documentation site generation.
-   **Markdown Standard:** Write content in MDX (Markdown + JSX) format.
-   **Navigation:** Clear sidebar navigation with logical hierarchy (max 3 levels deep).
-   **Code Blocks:** Use syntax highlighting with language specification for all code examples.
-   **Metadata:** Include frontmatter (title, description, tags) in every document.

### Technical Requirements
-   **Spec-Kit Plus Integration:** Follow Spec-Kit Plus conventions for project structure and specifications.
-   **Claude Code Usage:** Leverage Claude Code for code generation, refactoring, and documentation assistance.
-   **Version Control:** Use Git with meaningful commit messages following conventional commits format.
-   **GitHub Pages:** Configure proper build and deployment workflow.

### Code Standards
-   **Executable Examples:** All code snippets must be tested and runnable.
-   **Best Practices:** Follow language-specific best practices and style guides.
-   **Comments:** Include inline comments for complex logic.
-   **Error Handling:** Demonstrate proper error handling in examples.

## Constraints

### Technical Constraints
-   **Platform:** Docusaurus with Node.js v18+.
-   **Deployment:** GitHub Pages with automated CI/CD.
-   **Repository:** Public GitHub repository with clear README.
-   **Build Time:** Site must build successfully in under 5 minutes.
-   **File Size:** Individual markdown files should not exceed 500 lines (split if necessary).

### Content Constraints
-   **Chapter Length:** 1,500-4,000 words per chapter (excluding code blocks).
-   **Minimum Chapters:** At least 8 substantive chapters.
-   **Code Examples:** Minimum 3-5 working code examples per technical chapter.
-   **Images/Diagrams:** Use lightweight formats (SVG preferred, PNG/JPG optimized).
-   **External Dependencies:** Minimize external CDN dependencies for faster loading.

### Style Constraints
-   **Voice:** Second person ("you") for instructional content.
-   **Tense:** Present tense for current state, future for outcomes.
-   **Headings:** Title case for chapter titles, sentence case for section headings.
-   **Lists:** Parallel structure in all bulleted and numbered lists.
-   **Links:** All external links must be valid and include descriptive text.

## Development Workflow & Quality Checklist

### Spec-Kit Plus Workflow
1.  **Specification Phase**
    *   Define book outline and chapter structure in `/specs` directory.
    *   Create specification documents for each major section.
    *   Document technical requirements and dependencies.
2.  **Development Phase**
    *   Use Claude Code to generate initial content drafts.
    *   Iterate on content with Claude Code for refinement.
    *   Build code examples and test thoroughly.
    *   Configure Docusaurus with custom theme and plugins.
3.  **Review Phase**
    *   Technical review of all code examples.
    *   Content review for clarity and accuracy.
    *   Cross-reference links and navigation.
    *   Test deployment in staging environment.
4.  **Deployment Phase**
    *   Configure GitHub Actions for CI/CD.
    *   Deploy to GitHub Pages.
    *   Verify production build.
    *   Set up custom domain (if applicable).
5.  **Maintenance Phase**
    *   Monitor for broken links or outdated content.
    *   Update dependencies regularly.
    *   Address reader feedback and issues.
    *   Version control major updates.

## Quality Checklist
Before marking the project complete, verify:

*   ✅ All chapters written and reviewed.
*   ✅ All code examples tested and documented.
*   ✅ Docusaurus configuration optimized.
*   ✅ GitHub repository properly structured.
*   ✅ GitHub Pages deployment successful.
*   ✅ Mobile responsiveness verified.
*   ✅ Accessibility standards met.
*   ✅ Search functionality working.
*   ✅ Social sharing metadata configured.
*   ✅ Analytics configured (optional).
*   ✅ README and documentation complete.
*   ✅ License file included.
*   ✅ Final proofreading completed.

## Governance
This Constitution defines the foundational principles, standards, and processes for the "Technical Book Creation using Docusaurus and Spec-Kit Plus" project. It supersedes all other informal practices.

### Amendment Procedure
Any amendments to this Constitution must follow a formal process:
1.  **Proposal:** Submit a clear proposal outlining the suggested changes and their rationale.
2.  **Review:** The proposal must undergo review by the project maintainers and key stakeholders.
3.  **Approval:** Changes require explicit approval from the project lead.
4.  **Documentation:** Approved amendments must be documented with a new version increment, an updated `LAST_AMENDED_DATE`, and a Sync Impact Report (as per this constitution's guidelines).

### Versioning Policy
The Constitution version adheres to semantic versioning:
-   **MAJOR:** Backward incompatible governance/principle removals or redefinitions.
-   **MINOR:** New principle/section added or materially expanded guidance.
-   **PATCH:** Clarifications, wording, typo fixes, non-semantic refinements.

### Compliance Review
All significant project activities, including design, development, and deployment, must demonstrate compliance with the principles and standards outlined herein. Regular compliance reviews will be conducted as part of the project's quality gates.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown. | **Last Amended**: 2025-12-03
