# vibecoding-docs

A Claude Code skill that interactively generates the **6 planning documents** worth having
**before you start coding (vibecoding)** an app — and drops them into the project's
`docs/CLAUDE/`, leaving a reference in the root `CLAUDE.md`.

The 6 documents:

1. **PRD** — Product requirements
2. **TRD** — Technical requirements / stack
3. **UI/UX Design** — Design system
4. **AppFlow** — Screen flow (Mermaid diagram)
5. **BackEnd Schema** — Data model (Mermaid ER diagram)
6. **Implementation Plan** — Phases, milestones and timeline

## Install

```text
/plugin marketplace add SoftCollie/skills
/plugin install vibecoding-docs@softcollie
```

### Alternative via npm

If you would rather install it without the marketplace, this package copies the skill into
`~/.claude/skills/`:

```bash
npx @softcollie/vibecoding-docs-skill
```

> The recommended channel in Claude Code is the marketplace (`/plugin`); npm is an
> alternative for anyone who prefers `npx`.

## Usage

In any project, type `/vibecoding-docs` or just ask in plain language ("help me document this
app before I start coding", "generate the PRD/TRD for me…").

- **New project:** it asks short questions, one document at a time.
- **Existing project:** it first **reads** `CLAUDE.md`, `README`, `docs/**`, the manifests and
  the code structure to infer the context; it shows you a *context sheet* and a decision table
  (Derive / Link / Create) per document, and only asks you to confirm or correct.

The documents are written in **your language** — whichever one you are talking in (English by
default).

Output: `docs/CLAUDE/01-prd.md … 06-implementation-plan.md` + a `README.md` index, and a
section between `<!-- BEGIN/END vibecoding-docs -->` markers in the root `CLAUDE.md`
(re-runnable without duplicating).

## Roadmap

- [ ] Explicit **monorepo / multi-app** support (AppFlow and UI/UX per surface).
- [ ] **Spec-Driven Development**: constitution/guardrails, EARS acceptance criteria,
      `tasks.md` and a traceability matrix.
- [ ] Derive the **design system** from the code (Tailwind/Storybook tokens) instead of asking.
- [ ] **Status mode** for live projects (done/wip/planned + docs↔code discrepancies).

## License

MIT
