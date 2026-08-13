---
name: vibecoding-docs
description: Interactively generate the 6 planning documents worth having BEFORE you start coding (vibecoding) an app — PRD, TRD, UI/UX Design, AppFlow, BackEnd Schema and Implementation Plan — by asking the user questions and writing them into the project's `docs/CLAUDE/`, leaving a reference in the root CLAUDE.md. Use it when the user wants to plan/document a project or app before coding, or asks to create/update the PRD, TRD, design system, app flow, database schema or implementation plan. Works in any project.
---

# Vibecoding Docs — 6 documents before you code

This skill runs a guided conversation to produce **6 planning documents** and leaves them in
the current project's `docs/CLAUDE/`. Each document lays the groundwork for the next, so that
by the end the agent (Claude Code or another) has all the context it needs to implement the
app without guessing.

The 6 documents:

1. **PRD** — Product Requirements Document (`01-prd.md`)
2. **TRD** — Technical Requirements Document / stack (`02-trd.md`)
3. **UI/UX Design** — Design system (`03-ui-ux.md`)
4. **AppFlow** — Screen flow and user journey (`04-appflow.md`)
5. **BackEnd Schema** — Data model (`05-backend-schema.md`)
6. **Implementation Plan** — Phases, milestones and timeline (`06-implementation-plan.md`)

## Fixed rules

- **Language:** write the documents in **the language the user is speaking**; default to
  English when it is unclear. Reasonable exception: field/table names, code identifiers and
  proper technology names (React, PostgreSQL, AWS…) stay in their original form. Keep the
  file names as listed above regardless of language.
- **Output path:** ALWAYS `docs/CLAUDE/` at the project root. Create the folder if missing.
- **Progressive mode:** work **one document at a time**. Ask just enough, generate that
  document, show it and confirm before moving to the next. Do not overwhelm with long
  questionnaires: group questions into small batches (ideally using the question tool for
  closed options, and open questions for descriptions).
- **Never invent silently:** if the user does not know or does not answer something, propose
  a sensible default and mark it with `> TODO:` so they can review it.
- **Resumable:** if `docs/CLAUDE/` already holds documents, offer to continue/update instead
  of starting from scratch.

## Workflow

### Step 0 — Set up and gather context (once)

1. Locate the project root (where `.git`, `package.json`, etc. live; if there is none, use the
   current working directory). Create `docs/CLAUDE/` if missing.
2. Check whether documents already exist in `docs/CLAUDE/`. If they do, ask whether the user
   wants to **continue**, **update a specific one** or **regenerate**.
3. **Determine whether this is a NEW or an EXISTING project.** It is "existing" if there is
   code, a `.git` with history, a `CLAUDE.md`, a `README`, a `docs/` folder, etc. In that case
   run the **reconnaissance** of Step 0-bis BEFORE asking anything. The golden rule: in
   existing projects **you do not ask what you can read** — infer it, present it, and only ask
   for confirmation or corrections.
4. Ask for the **base context** (only what you could not infer). In new projects, one short
   batch: project/app name · what it does and for whom (one sentence) · target platform
   (Web · Mobile iOS/Android · Both · Desktop) · new idea or already in progress?

### Step 0-bis — Reconnaissance of an existing project

Goal: rebuild the context from what is ALREADY there, so the questions become
"confirm/correct" instead of "answer from scratch".

1. **Read the context sources** that exist (strongest signal first):
   - `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md` — project
     instructions and description.
   - `README*`, `MVP.md`, `ROADMAP*`, `CHANGELOG*`, `docs/**` (including localized `.xx.md`),
     wikis.
   - Manifests: `package.json`, `composer.json`, `pyproject.toml`, `requirements.txt`,
     `go.mod`, `pom.xml`, `Gemfile`, `*.csproj` → stack, scripts, dependencies.
   - Infra: `Dockerfile`, `docker-compose*.yml`, `*-ci.yml`, `.env.template`/`.env.example`,
     `angular.json`/`vite.config`/`next.config`, `capacitor.config`, `ionic.config` →
     deployment and platform.
   - Folder structure (2-3 level tree, `apps/`, `src/`, `packages/`) and, if there is a
     database, migrations/schemas (`migrations/`, `schema.prisma`, `*.sql`, entities/models).
2. **Synthesize a "context sheet"** and show it to the user for validation (do not copy it
   into the final documents): name, purpose, users, platform, detected stack, integrations,
   glimpsed data model, maturity and current phase.
3. **Map what exists against the 6 documents.** For each one decide and propose:
   - **Derive** — there is already enough material (e.g. a `docs/ARCHITECTURE.md` feeds the
     TRD); generate it by summarizing/structuring what exists.
   - **Link / do not duplicate** — an equivalent, good document already exists; in
     `docs/CLAUDE/` create a short stub that **references** the original instead of copying it.
   - **Create** — there is nothing; generate it with the usual questions (there will be few).
   Present this decision table and let the user adjust it before generating.
4. **Reconcile with the existing `docs/` and `CLAUDE.md`:** respect their style and language,
   do not contradict what is already documented and, if you spot discrepancies between the
   code and the docs, **flag them** instead of overwriting. Never delete previous documentation.

### Steps 1–6 — Generate each document

For EACH document, in order:

1. **Read the matching template** in `templates/` (see the table below) to learn its structure.
2. **Ask that document's questions** (the ones the template lists), in short batches. Reuse
   what was already answered in previous steps; do not ask twice.
3. **Write the document** to `docs/CLAUDE/NN-<slug>.md`, filling the template with the answers.
   Use **Mermaid** diagrams where the template says so (flows and ER schema) — the text
   equivalent of the slides in the original concept.
4. **Summarize** what you generated (2–3 lines) and ask whether they want to adjust anything
   or **continue** with the next one.
5. Each document starts with a header that includes the project and a
   `> Last updated: <today's date>` line.

| # | Document | Output file | Template |
|---|----------|-------------|----------|
| 1 | PRD | `docs/CLAUDE/01-prd.md` | `templates/01-prd.md` |
| 2 | TRD | `docs/CLAUDE/02-trd.md` | `templates/02-trd.md` |
| 3 | UI/UX Design | `docs/CLAUDE/03-ui-ux.md` | `templates/03-ui-ux.md` |
| 4 | AppFlow | `docs/CLAUDE/04-appflow.md` | `templates/04-appflow.md` |
| 5 | BackEnd Schema | `docs/CLAUDE/05-backend-schema.md` | `templates/05-backend-schema.md` |
| 6 | Implementation Plan | `docs/CLAUDE/06-implementation-plan.md` | `templates/06-implementation-plan.md` |

> The user may ask for only some of the documents; respect that. The recommended order is 1→6
> because each one feeds context to the next (e.g. the PRD entities feed the BackEnd schema).

### Step 7 — Index and reference in CLAUDE.md

1. Create/update `docs/CLAUDE/README.md` as an index linking to the 6 documents, with a status
   line (generated / pending) for each.
2. Create or update the project's **root `CLAUDE.md`**, adding (or refreshing) a section
   delimited by markers so future runs do not duplicate it:

```markdown
<!-- BEGIN vibecoding-docs -->
## 📐 Planning documentation (docs/CLAUDE/)

Before implementing any feature, read and respect these documents:

- [`docs/CLAUDE/01-prd.md`](docs/CLAUDE/01-prd.md) — Product requirements (what is being built and why)
- [`docs/CLAUDE/02-trd.md`](docs/CLAUDE/02-trd.md) — Technical requirements and stack
- [`docs/CLAUDE/03-ui-ux.md`](docs/CLAUDE/03-ui-ux.md) — UI/UX design system
- [`docs/CLAUDE/04-appflow.md`](docs/CLAUDE/04-appflow.md) — Screen flow / user journey
- [`docs/CLAUDE/05-backend-schema.md`](docs/CLAUDE/05-backend-schema.md) — Backend schema / data model
- [`docs/CLAUDE/06-implementation-plan.md`](docs/CLAUDE/06-implementation-plan.md) — Implementation plan

These documents are the project's source of truth. If a request contradicts them, say so.
<!-- END vibecoding-docs -->
```

   - Write that section in the same language as the documents.
   - If `CLAUDE.md` does not exist, create it with a minimal header (`# <Project>`) and this
     section.
   - If the marker section already exists, replace only that block.
   - Do not touch the rest of `CLAUDE.md`.

3. Close by summarizing which documents were created and which are pending/TODO.

## Good practice when asking

- One batch = 2–4 questions max. Keep moving, do not interrogate.
- For closed choices (platform, framework, database, visual style) offer concrete options —
  use the reference stack in `templates/02-trd.md` as your repertoire.
- For descriptions (problem, users, features) leave the answer open.
- If the user says "you decide" / "whatever you recommend", choose for them, justify it in one
  line and move on; mark it with `> TODO:` if it is worth validating.
- Stay focused: the goal is actionable documents, not exhaustive ones.
