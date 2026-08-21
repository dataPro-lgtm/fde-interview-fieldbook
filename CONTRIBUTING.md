# Contributing

Thank you for helping make FDE interview preparation more accurate and useful.

## What we welcome

- corrections supported by a current source;
- original cases that teach discovery, engineering, rollout, or productization;
- clearer explanations and counterexamples;
- translations that preserve meaning rather than translating word for word;
- new scorecard dimensions with observable evidence;
- role updates from official job postings or employer documentation.

## Evidence rules

Classify external claims as one of:

1. **Official** — an employer posting, protocol specification, standards body, or first-party technical documentation.
2. **Corroborated** — at least two credible, independent sources agree.
3. **Community** — practitioner experience that is useful but not authoritative.

For time-sensitive claims, add or update an entry in `data/sources.json` with `last_checked`. Do not turn a single community interview report into a company-wide statement.

## Content rules

- Write in your own words.
- Explain reasoning, trade-offs, failure boundaries, and what evidence would change the answer.
- Prefer a realistic scenario over a long vocabulary list.
- Do not promise that a single framework is universally correct.
- Do not submit confidential, leaked, paid, or copyrighted material without permission.
- Do not add raw PDF, DOCX, XLSX, or ZIP files.

## Pull-request checklist

- [ ] The change has a clear learner outcome.
- [ ] Time-sensitive claims have a source and checked date.
- [ ] Official facts and personal experience are labeled separately.
- [ ] Internal links work.
- [ ] Case-pack files and staged artifacts are registered in `data/case-packs.json`.
- [ ] The change adds no proprietary material or personal data.
- [ ] `python3 scripts/validate_repo.py` passes.
- [ ] `python3 scripts/validate_case_packs.py` passes when cases change.
- [ ] `npx --yes markdownlint-cli2@0.18.1 "**/*.md" "#node_modules"` passes.
- [ ] `python3 scripts/validate_mermaid.py --files <changed-markdown>` passes when diagrams change.

## Visual language

Use a diagram or table only when it makes a relationship faster to understand than a short paragraph.

- Prefer Mermaid so diagrams remain reviewable, searchable, theme-aware, and editable in Git.
- Use top-to-bottom flows by default; wide left-to-right diagrams are difficult to read on phones.
- Keep one diagram focused on one question, typically with five to nine primary steps; split larger diagrams by phase.
- Use tables for comparisons, scoring anchors, ownership, and decision boundaries; avoid paragraph-sized cells.
- Introduce every visual with the question it answers, and explain the operational takeaway after it.
- Do not rely on color alone. Labels and arrow direction must preserve the meaning in dark mode, print, and assistive reading.
- A visual should not invent precision, replace necessary caveats, or repeat nearby prose without reducing cognitive load.

Changed Mermaid blocks are rendered in CI with a pinned CLI. Public links are checked separately on a weekly schedule so transient network failures do not block ordinary pull requests. Only public HTTPS links are accepted; localhost, private-network targets, and non-standard ports are rejected before a request is sent.

## Good first contributions

See [ROADMAP.md](ROADMAP.md) for open translation, case, and source-refresh tasks. New case packs must follow the [facilitation standard](interview-kits/cases/facilitation-standard.md); a good pull request does not need to add a whole chapter.

## Practice feedback

You do not need to write code or a chapter to contribute. After using a case, scorecard, or calibration exercise, open the structured [practice feedback form](https://github.com/dataPro-lgtm/fde-interview-fieldbook/issues/new?template=practice-feedback.yml). Describe what changed between your first and second attempt, and where the material still failed to help.

Remove employer-confidential details, personal data, leaked questions, and paid material. A useful report can describe the skill and failure pattern without naming the company or interview process.
