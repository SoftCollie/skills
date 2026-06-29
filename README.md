# SoftCollie Skills · marketplace para Claude Code

Stack público de skills de **SoftCollie / ShephERP** para [Claude Code](https://claude.com/claude-code).
Instálalas como plugins y mantenlas actualizadas con los comandos `/plugin`.

## Instalación

```text
/plugin marketplace add SoftCollie/skills
/plugin install vibecoding-docs@softcollie
```

> El primer comando registra este marketplace (una sola vez). El segundo instala una skill concreta.

## Skills disponibles

| Skill | Qué hace |
|-------|----------|
| [`vibecoding-docs`](plugins/vibecoding-docs) | Genera los 6 documentos de planificación previos al *vibecoding* (PRD, TRD, UI/UX, AppFlow, esquema del backend y plan de implementación) en `docs/CLAUDE/` y los referencia desde el `CLAUDE.md` raíz. En proyectos existentes analiza el contexto en vez de preguntar desde cero. |
| [`watch-for-me`](plugins/watch-for-me) | Mira un vídeo por ti sin reproducirlo: desde una ruta o una URL (Instagram, YouTube, TikTok…) extrae los fotogramas clave, contact sheets y opcional transcripción, sintetiza el contenido y deja al agente listo para responder preguntas sobre el vídeo. Multiplataforma; gestiona sus dependencias. |

## Actualizar

Cuando se publique una versión nueva:

```text
/plugin marketplace update softcollie
/plugin update vibecoding-docs
```

## Para mantenedores

- Cada skill es un **plugin** bajo `plugins/<nombre>/` con su `.claude-plugin/plugin.json`.
- El catálogo se declara en [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).
- Versionado **semver** en el campo `version` de cada `plugin.json`. Sube la versión al publicar cambios.
- Publicar una actualización = editar la skill, subir `version`, `git commit` y `git push` a `main`.

## Licencia

MIT — ver [LICENSE](LICENSE).
