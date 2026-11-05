---
this_file: AGENTS.md
---

# vfjLib: agent guide

A low-level reader and writer for FontLab JSON (VFJ) files.

`Lib/vfjLib/` contains the package, `Tools/` contains utilities and `Doc/` is reserved for reference material and currently contains only an empty placeholder.

## Checks

The observed source base is `bf87275fba54bc2959b112391b2bca43d7ded621`.
`setup.py` packages `Lib/vfjLib/`. `Tools/` contains utilities and `Doc/` is reserved
for reference material and currently contains only an empty placeholder.
No tracked suite or test wrapper is established.
The pytest metadata in `setup.py` does not supply tests.
Before a writer change, define an owned VFJ fixture and a complete-data
preservation contract. Verify saved and reopened output. Keep unsupported fields
and native compatibility limits explicit. Never use an owner font as a fixture.

## Review and delivery

Read README, PLAN, TODO, WORK and CHANGELOG before work. Use an isolated checkout.
Preserve the owner's branches, index, edits, archives and licences.
Choose one small complete MVP. Name its callers, tests, fixtures, configuration
and exports. Use graph context and impact before source symbol changes.
Confirm stale, empty or unknown graph results against the actual source.

Run the exact repository checks. Keep the unchanged 80% coverage gate for each
complete changed production module where the milestone gate applies.
Documentation checks cover headers, fences, links, privacy and the exact diff.
Keep ordinary installed hooks active. Do not bypass a failed gate.
Obtain independent specification and quality review before a milestone commit.
Stage only the approved paths after checking their preimage hashes.
Run graph change analysis before committing.

Issue 230 authorizes reviewed, passing documentation milestone commits and pushes.
Verify the actual remote branch SHA after a push. Refresh remote refs before
integration. Reconcile concurrent work and consumers before primary-branch
integration. Run the applicable combined-source and CI checks.
Do not infer publication, installation or native acceptance from a branch push.
Do not create release tags, dispatch release workflows or publish packages for
this documentation milestone.

Before obsolete branch or file removal, verify recovery and integration.
Check fresh owner/worktree attachments and unique work. Preserve sealed evidence
and protected tags. Do not force-push or rewrite history by implication.
Keep PLAN future-facing and TODO flat with unchecked open tasks.
Record only verified scope in CHANGELOG and current checks in WORK.

Issue 123 remains paused. Issue 207 candidates require reconciliation with newer
source. Keep source tests, complete archives, installed origins/RECORD, native
workflows, canonical promotion, remote delivery and publication separate.
Do not read or mutate owner fonts, preferences, Output or global update queues.
Do not install or uninstall in the owner's FontLab user folder.
Preserve private configuration and source boundaries. Native work requires a
separate safe owned-fixture session under the workspace D30 checks and fences.
The D31 zone/master lane remains reserved. D29 generation/publication gates apply.

This repository integrates qualified work into `master`.

Preserve Vassil Kateliev’s authorship and BSD 3-Clause terms in LICENSE.
