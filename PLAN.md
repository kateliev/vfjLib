---
this_file: PLAN.md
---

# vfjLib: remaining plan

1. Define an owned-fixture VFJ read/write preservation contract.
2. Verify complete expected VFJ data and saved/reopened output before qualifying writer changes.
3. Qualify the reviewed documentation milestone, verify its remote SHA and integrate into `master` under the applicable gates.
4. After integration and recovery checks, remove only proven obsolete items without unique or attached owner work.

## Checks

The observed source base is `bf87275fba54bc2959b112391b2bca43d7ded621`.
`setup.py` packages `Lib/vfjLib/`. `Tools/` contains utilities and `Doc/` is reserved
for reference material and currently contains only an empty placeholder.
No tracked suite or test wrapper is established.
The pytest metadata in `setup.py` does not supply tests.
Before a writer change, define an owned VFJ fixture and a complete-data
preservation contract. Verify saved and reopened output. Keep unsupported fields
and native compatibility limits explicit. Never use an owner font as a fixture.

Preserve Vassil Kateliev’s authorship and BSD 3-Clause terms in LICENSE.

Follow [AGENTS.md](AGENTS.md) for independent review and qualified milestone delivery.
Keep Issue 123 paused and native/installation/publication gates separate.
