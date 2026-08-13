# SoftCollie Skills · a marketplace for Claude Code

The public skill stack of **SoftCollie / ShephERP** for [Claude Code](https://claude.com/claude-code).
Install them as plugins and keep them updated with the `/plugin` commands.

## Install

```text
/plugin marketplace add SoftCollie/skills
/plugin install vibecoding-docs@softcollie
```

> The first command registers this marketplace (once). The second installs a specific skill.

## Available skills

| Skill | What it does |
|-------|--------------|
| [`vibecoding-docs`](plugins/vibecoding-docs) | Generates the 6 planning documents you want before *vibecoding* (PRD, TRD, UI/UX, AppFlow, backend schema and implementation plan) into `docs/CLAUDE/`, and references them from the root `CLAUDE.md`. In existing projects it reads the context instead of asking from scratch. |
| [`watch-for-me`](plugins/watch-for-me) | Watches a video for you without playing it: from a local path or a URL (Instagram, YouTube, TikTok…) it extracts the key frames, contact sheets and an optional transcript, summarizes the content and leaves the agent ready to answer questions about the video. Cross-platform; manages its own dependencies. |

## Update

When a new version ships:

```text
/plugin marketplace update softcollie
/plugin update vibecoding-docs
```

## For maintainers

- Each skill is a **plugin** under `plugins/<name>/` with its own `.claude-plugin/plugin.json`.
- The catalog is declared in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).
- **Semver** versioning in each `plugin.json`'s `version` field. Bump it when publishing changes.
- Publishing an update = edit the skill, bump `version`, `git commit` and `git push` to `main`.
- Everything user-facing (skill descriptions, READMEs, generated docs) is written in **English**
  so the skills are discoverable; the skills themselves answer in the user's language.

## License

MIT — see [LICENSE](LICENSE).
