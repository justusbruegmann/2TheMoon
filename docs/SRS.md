# [Project Name] — Software Requirements Specification

<!--
HOW TO USE THIS TEMPLATE
- Copy the whole docs/ folder into your repository.
- Replace every [placeholder] in square brackets. Comments like this one are guidance: they
  are invisible on GitHub, and you may delete them once a section is done.
- Keep every heading and its number. If a section does not apply, write
  "Not applicable" and one sentence why.
- Every section you write names its author: in the "Author" line below its heading, or in
  the Author column of a table. Prefilled sections need no author.
- Structure after the RUP template "Software Requirements Specification":
  https://cin.ufpe.br/~if682/RUP/webtmpl/templates/req/rup_srs.htm
-->

| Team | Version | Last change |
| ---- | ------- | ----------- |
| [Team name] | [0.1] | [dd.mm.yyyy] |

The Git history of this file is the revision history.

## Table of contents

1. [Introduction](#1-introduction)
2. [Overall description](#2-overall-description)
3. [Specific requirements](#3-specific-requirements)
4. [Supporting information](#4-supporting-information)

## 1 Introduction

### 1.1 Purpose

*Author: [first name]*

<!-- One paragraph: what this document describes and who reads it
     (your team, the lecturer as investor, the developer who takes over). -->

This document specifies the requirements of [project name]. […]

### 1.2 Scope

*Author: [first name]*

<!-- What the software does and for whom, in two or three sentences.
     Then split explicitly into in scope and out of scope, each with a reason.
     Out of scope = your MoSCoW "won't have this time". Document later changes here. -->

[Two or three sentences.]

| In scope | Reason |
| -------- | ------ |
| [feature] | [why] |

| Out of scope | Reason |
| ------------ | ------ |
| [feature] | [why not, or not now] |

### 1.3 Definitions, acronyms and abbreviations

*Author: [first name]*

| Term | Meaning |
| ---- | ------- |
| SRS | Software Requirements Specification |
| UC | Use case |
| NFR | Non-functional requirement (quality requirement or constraint) |
| [term] | [meaning] |

### 1.4 References

*Author: [first name]*

| Title | Link |
| ----- | ---- |
| Blog | [link to your GitHub Discussions] |
| Board | [link to your GitHub Projects board] |
| [other document] | [link] |

### 1.5 Overview

Section 2 describes the product as a whole: vision and use case diagram. Section 3 lists the
specific requirements: the use cases (3.1) and the quality requirements and constraints
(3.2 to 3.12).

## 2 Overall description

### 2.1 Vision

*Author: [first name]*

<!-- Your vision from Task 1, updated: the problem, the target group and the stakeholders,
     the value, and how you differ from alternatives. The investor should get it in two minutes. -->

[…]

### 2.2 Use case diagram

*Author: [first name]*

<!-- One UML use case diagram for the whole application, at least five high-level use cases;
     login and registration do not count. Commit the source file next to the image. -->

![Use case diagram](diagrams/use-case-diagram.png)

### 2.3 Assumptions and dependencies

*Author: [first name]*

<!-- Optional: what you assume (e.g., users have a DHBW account) and what you depend on
     (e.g., an external API). Delete the comment and write "None" if there are none. -->

[…]

## 3 Specific requirements

### 3.1 Functionality

<!-- One subsection per use case. The specification lives in its own file in use_cases/,
     created from UC-00_template.md. Here: name, author, one sentence, link.
     Task 3: at least one specified use case per team member (four entries with a link below).
     List every use case of your diagram; mark the ones not specified yet as "planned". -->

#### 3.1.1 UC-01 [Verb object]

*Author: [first name]* · [One sentence.] · [Specification](use_cases/UC-01_[name].md)

#### 3.1.2 UC-02 [Verb object]

*Author: [first name]* · [One sentence.] · [Specification](use_cases/UC-02_[name].md)

#### 3.1.3 UC-03 [Verb object]

*Author: [first name]* · [One sentence.] · [Specification](use_cases/UC-03_[name].md)

#### 3.1.4 UC-04 [Verb object]

*Author: [first name]* · [One sentence.] · [Specification](use_cases/UC-04_[name].md)

#### 3.1.5 UC-05 [Verb object]

*Author: [first name]* · [One sentence.] · planned

<!-- QUALITY REQUIREMENTS (3.2 to 3.5)
     At least one per section. Each one: an ID, one sentence with "shall", a number you can
     test, and if possible stimulus, response and measure. IDs are unique in the whole SRS,
     including the special requirements of your use cases.
     Example: NFR-P-01 — When 50 users search at the same time, the app lists free slots
     within 1 s for 95 % of the requests. -->

### 3.2 Usability

| ID | Requirement | Author |
| -- | ----------- | ------ |
| NFR-U-01 | [measurable requirement] | [first name] |

### 3.3 Reliability

| ID | Requirement | Author |
| -- | ----------- | ------ |
| NFR-R-01 | [measurable requirement] | [first name] |

### 3.4 Performance

| ID | Requirement | Author |
| -- | ----------- | ------ |
| NFR-P-01 | [measurable requirement] | [first name] |

### 3.5 Supportability

| ID | Requirement | Author |
| -- | ----------- | ------ |
| NFR-S-01 | [measurable requirement] | [first name] |

### 3.6 Design constraints

*Author: [first name]*

<!-- Decisions that are fixed, not chosen per feature: your stack. -->

| ID | Constraint |
| -- | ---------- |
| DC-01 | Frontend: [JavaScript/TypeScript, framework] |
| DC-02 | Backend: [Java, JavaScript/TypeScript or Python, framework] |
| DC-03 | Database: […] |

### 3.7 Online user documentation and help system requirements

Not applicable. [Reason, or replace with requirements.]

### 3.8 Purchased components

Not applicable. [Reason, or list them.]

### 3.9 Interfaces

*Author: [first name]*

#### 3.9.1 User interfaces

<!-- Link the mockups of your use cases, or describe the main screens in one line each. -->

[…]

#### 3.9.2 Hardware interfaces

Not applicable. [Reason.]

#### 3.9.3 Software interfaces

<!-- External services and APIs you use, e.g., an e-mail service. -->

[…]

#### 3.9.4 Communications interfaces

<!-- E.g., HTTPS between frontend and backend. -->

[…]

### 3.10 Licensing requirements

*Author: [first name]*

<!-- The license of your project, and of libraries that impose conditions. -->

[…]

### 3.11 Legal, copyright and other notices

*Author: [first name]*

<!-- E.g., data protection (GDPR) if you store personal data. -->

[…]

### 3.12 Applicable standards

*Author: [first name]*

<!-- E.g., WCAG 2.2 level AA, a coding standard. -->

[…]

## 4 Supporting information

<!-- Optional: appendices, glossary extensions, interview notes. -->

None.
