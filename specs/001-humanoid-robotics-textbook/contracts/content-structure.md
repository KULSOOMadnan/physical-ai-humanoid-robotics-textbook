# Content Structure Contracts: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-04
**Feature**: 001-humanoid-robotics-textbook
**Plan**: specs/001-humanoid-robotics-textbook/plan.md
**Data Model**: specs/001-humanoid-robotics-textbook/data-model.md

## Overview

This document outlines the structured contracts for the textbook's content, detailing how chapters, content modules, and other elements are organized and interlinked to ensure a cohesive and effective learning experience. These contracts act as "APIs" for content creation, ensuring consistency and adherence to the pedagogical goals.

## 1. Textbook Structure Contract

*   **Description**: Defines the top-level organization of the entire textbook.
*   **Structure**:
    *   `Front Matter`: (e.g., Title Page, Copyright, Dedication, Table of Contents, Preface)
    *   `Core Chapters`: A sequence of 12-15 `Chapter` entities, logically ordered from fundamentals to advanced topics.
        *   **Validation**: Must have at least 12 chapters as per `SC-007`.
    *   `Glossary`: A comprehensive list of defined terms.
    *   `Appendices`: Supplementary materials such as mathematical foundations, setup guides.
    *   `Back Matter`: (e.g., Index, References)
*   **Integrity Rules**:
    *   All `Chapter` entities must be uniquely numbered and titled.
    *   All internal links within the textbook content must be functional (`SC-014`).
    *   `Glossary` terms must be consistently used and defined on first use in chapters.

## 2. Chapter Structure Contract

*   **Description**: Defines the internal organization of each `Chapter`.
*   **Structure**:
    *   `Introduction`: Overview of chapter goals and prerequisites.
    *   `Learning Objectives`: Explicitly stated learning outcomes.
    *   `Core Content Modules`: An ordered sequence of `Content Module` entities.
        *   **Validation**: Each chapter must contain at least 2-3 technical diagrams (`SC-019`).
        *   **Flow**: Follows Theory → Simulation → Practice → Real-world transfer pedagogical constraint.
    *   `Summary/Conclusion`: Recap of key concepts.
    *   `End-of-Chapter Quizzes`: Assessment questions (`FR-019`).
    *   `Projects/Exercises`: Hands-on practical tasks (`FR-019`, `SC-010`).
*   **Integrity Rules**:
    *   `Chapter` content (excluding code) between 4,000-7,000 words (`SC-017`).
    *   `Code-to-Text Ratio` must be a minimum of 30% for core content.
    *   All `Code Example` modules must be runnable and tested (`SC-008`).

## 3. Content Module Contracts (Examples)

*   **Description**: Defines the expected format and content of various types of learning modules.

### 3.1. Text Module

*   **Type**: `Text`
*   **Content**: Markdown text, explanations, theoretical concepts.
*   **Integrity**: Clear, concise, accurate, and jargon-free (`Constitution: Content Quality - Clarity`).

### 3.2. Code Example Module

*   **Type**: `Code Example`
*   **Content**: Python code snippet, often with accompanying explanation.
*   **Integrity**: Must be runnable, tested, follow PEP 8, include type hints and docstrings (`Constitution: Code Standards`).
*   **Placement**: Referenced from `code-examples/` directory.

### 3.3. Diagram/Figure Module

*   **Type**: `Diagram/Figure`
*   **Content**: Path to image file (SVG, optimized PNG/JPG).
*   **Integrity**: Must enhance understanding (`SC-009`), include alt text for accessibility, and be lightweight.

### 3.4. Exercise/Lab Module

*   **Type**: `Exercise/Lab`
*   **Content**: Problem description, steps, expected output, solution link.
*   **Integrity**: Hands-on, practical application, clear instructions (`SC-010`).

### 3.5. Case Study Module

*   **Type**: `Case Study`
*   **Content**: Description of real-world robotics project, lessons learned.
*   **Integrity**: Industry-relevant, concise.

## 4. Inter-Module Communication (Conceptual)

*   **Description**: How different content modules implicitly "interact" or depend on each other.
*   **Dependencies**:
    *   `Code Example` modules often depend on concepts introduced in `Text Module`s.
    *   `Exercise/Lab` modules rely on `Code Example`s and `Text Module`s.
    *   `Diagram/Figure` modules support `Text Module`s.
    *   `Glossary` terms can be linked from any `Text Module`.
*   **Flow**: Pedagogical progression ensures foundational concepts are covered before advanced topics are introduced (`Constitution: Difficulty Curve`).

## 5. Metadata Contract (Docusaurus Frontmatter)

*   **Description**: Standardized metadata for all MDX content files.
*   **Fields**:
    *   `title`: (String, required)
    *   `description`: (String, optional, for SEO)
    *   `sidebar_label`: (String, required for navigation)
    *   `keywords`: (List of Strings, optional, for SEO)
    *   `slug`: (String, optional, for custom URL paths)
    *   `authors`: (List of Strings, optional)
    *   `tags`: (List of Strings, optional)
*   **Integrity**: Must include frontmatter in every document (`Constitution: Documentation Structure - Metadata`).
