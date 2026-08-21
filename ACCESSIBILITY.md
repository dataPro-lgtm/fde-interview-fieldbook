# Accessibility

This fieldbook aims to remain usable as plain, versioned Markdown. Accessibility is a continuous authoring constraint, not a claim of certification.

## Current reader support

- Core pages use one H1 and ordered heading levels.
- Chinese and English entry paths are separated and clearly labeled.
- Reading maps route by goal and time instead of requiring a cover-to-cover read.
- Diagrams are Mermaid source, accompanied by prose that explains the operational conclusion.
- Tables are used for bounded comparisons rather than as page-layout containers.
- Meaning is not intentionally encoded by color alone.
- The core content remains readable without custom JavaScript or a generated site.

## Authoring requirements

When contributing:

1. use descriptive link text instead of “click here”;
2. keep heading order stable and do not skip levels for visual size;
3. explain every diagram in adjacent prose so the diagram is not the only carrier of meaning;
4. avoid paragraph-sized table cells and provide prose when a table becomes difficult on narrow screens;
5. do not use emoji, color, capitalization, or position as the only status signal;
6. label code blocks and explain their expected result;
7. preserve the certainty, scope, and warnings of the source when translating;
8. prefer plain language, concrete examples, and short navigation labels.

## Known limits

The project has not completed a formal WCAG audit or assistive-technology test matrix. GitHub rendering is partly outside the repository's control, and wide technical tables can still require horizontal scrolling. A future generated site must pass the acceptance criteria in the [site evaluation](docs/research/documentation-site-evaluation.md) before it replaces the GitHub-native path.

Report a barrier through the [content issue form](https://github.com/dataPro-lgtm/fde-interview-fieldbook/issues/new?template=content-gap.yml). Describe the page, assistive context if you are comfortable sharing it, and the task you could not complete; no medical or personal information is required.
