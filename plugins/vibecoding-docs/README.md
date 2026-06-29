# vibecoding-docs

Skill de Claude Code que genera, de forma interactiva y en español, los **6 documentos de
planificación** que conviene tener **antes de programar (vibecoding)** una app — y los deja en
`docs/CLAUDE/` del proyecto, dejando una referencia en el `CLAUDE.md` raíz.

Los 6 documentos:

1. **PRD** — Requisitos de producto
2. **TRD** — Requisitos técnicos / stack
3. **Diseño UI/UX** — Sistema de diseño
4. **AppFlow** — Flujo de pantallas (diagrama Mermaid)
5. **Esquema del BackEnd** — Modelo de datos (diagrama ER Mermaid)
6. **Plan de Implementación** — Fases, hitos y plazos

## Instalación

```text
/plugin marketplace add SoftCollie/skills
/plugin install vibecoding-docs@softcollie
```

## Uso

En cualquier proyecto, escribe `/vibecoding-docs` o pídelo en lenguaje natural
("ayúdame a documentar esta app antes de programar", "genérame el PRD/TRD…").

- **Proyecto nuevo:** te hace preguntas cortas, documento a documento.
- **Proyecto existente:** primero **lee** `CLAUDE.md`, `README`, `docs/**`, manifiestos y la
  estructura del código para inferir el contexto; te muestra una *Ficha de contexto* y una tabla de
  decisión (Derivar / Enlazar / Crear) por cada documento, y solo te pide confirmar o corregir.

Salida: `docs/CLAUDE/01-prd.md … 06-plan-implementacion.md` + `README.md` índice, y una sección entre
marcadores `<!-- BEGIN/END vibecoding-docs -->` en el `CLAUDE.md` raíz (re-ejecutable sin duplicar).

## Roadmap

- [ ] Soporte explícito de **monorepos / multi-app** (AppFlow y UI/UX por superficie).
- [ ] **Spec-Driven Development**: constitución/guardrails, criterios de aceptación EARS, `tasks.md`
      y matriz de trazabilidad.
- [ ] Derivar el **design system** desde el código (tokens de Tailwind/Storybook) en vez de preguntar.
- [ ] Modo **estado** para proyectos vivos (hecho/wip/plan + discrepancias docs↔código).

## Licencia

MIT
