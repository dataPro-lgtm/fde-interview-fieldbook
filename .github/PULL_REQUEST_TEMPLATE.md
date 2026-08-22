# Pull request

## Learner outcome

What can a reader do or understand better after this change?

## Evidence

- Source level: Official / Corroborated / Community / Not time-sensitive
- Direct links and checked dates:

## Quality checklist

- [ ] Claims are scoped to the evidence.
- [ ] Reasoning, trade-offs, and failure boundaries are explained.
- [ ] No confidential, leaked, paid, personal, or copied material is included.
- [ ] Internal links pass `python3 scripts/validate_repo.py`.
- [ ] Case changes pass `python3 scripts/validate_case_packs.py`.
- [ ] Role-radar or baseline changes pass `python3 scripts/validate_research_data.py`.
- [ ] Role-playbook changes pass `python3 scripts/validate_role_playbooks.py`.
- [ ] Guided-practice changes pass `python3 scripts/validate_learning_paths.py`.
- [ ] Calibration changes pass `python3 scripts/validate_calibration.py`.
- [ ] Core translation or source-ledger changes pass `python3 scripts/validate_parity_archive.py`.
- [ ] Release-bound changes refresh and pass `python3 scripts/validate_release_manifest.py --check`.
- [ ] Changed Mermaid diagrams render with `python3 scripts/validate_mermaid.py --files <paths>`.
- [ ] Diagrams, tables, links, and translations preserve an accessible text path.
- [ ] Material changes are noted in `CHANGELOG.md`.
