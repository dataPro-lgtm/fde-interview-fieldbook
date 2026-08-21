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
- [ ] The change adds no proprietary material or personal data.
- [ ] `python3 scripts/validate_repo.py` passes.

## Good first contributions

See [ROADMAP.md](ROADMAP.md) for open translation, case, and source-refresh tasks. Small corrections are valuable; a good pull request does not need to add a whole chapter.
