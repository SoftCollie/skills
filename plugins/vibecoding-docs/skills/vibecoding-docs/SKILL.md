---
name: vibecoding-docs
description: Genera de forma interactiva los 6 documentos de planificación que conviene tener ANTES de programar (vibecoding) una app — PRD, TRD, Diseño UI/UX, AppFlow, Esquema del BackEnd y Plan de Implementación — haciendo preguntas al usuario y escribiéndolos en `docs/CLAUDE/` del proyecto, y deja una referencia en el CLAUDE.md raíz. Úsala cuando el usuario quiera planificar/documentar un proyecto o app antes de codificar, o pida crear/actualizar el PRD, TRD, design system, flujo de la app, esquema de base de datos o plan de implementación. Funciona en cualquier proyecto.
---

# Vibecoding Docs — 6 documentos antes de programar

Esta skill conduce una conversación guiada para producir **6 documentos de planificación**
en español y los deja en `docs/CLAUDE/` del proyecto actual. Cada documento sienta las
bases del siguiente, de modo que al terminar el agente (Claude Code u otro) tenga todo el
contexto para implementar la app sin "adivinar".

Los 6 documentos:

1. **PRD** — Documento de Requisitos de Producto (`01-prd.md`)
2. **TRD** — Documento de Requisitos Técnicos / stack (`02-trd.md`)
3. **Diseño UI/UX** — Sistema de diseño (`03-ui-ux.md`)
4. **AppFlow** — Flujo de pantallas y recorrido del usuario (`04-appflow.md`)
5. **Esquema del BackEnd** — Modelo de datos (`05-backend-schema.md`)
6. **Plan de Implementación** — Fases, hitos y plazos (`06-plan-implementacion.md`)

## Reglas fijas

- **Idioma:** redacta TODO el contenido en **español**. Excepción razonable: nombres de
  campos/tablas, identificadores de código y nombres propios de tecnologías (React, PostgreSQL,
  AWS…) van en su forma original.
- **Ruta de salida:** SIEMPRE `docs/CLAUDE/` en la raíz del proyecto. Crea la carpeta si no existe.
- **Modo progresivo:** trabaja **un documento a la vez**. Pregunta lo justo, genera ese documento,
  enséñalo y confirma antes de pasar al siguiente. No abrumes con cuestionarios largos: agrupa las
  preguntas en tandas pequeñas (idealmente con la herramienta de preguntas para opciones cerradas y
  preguntas abiertas para descripciones).
- **No inventes silenciosamente:** si el usuario no sabe o no responde algo, propón un valor por
  defecto sensato y márcalo con `> TODO:` para que lo revise.
- **Reanudable:** si `docs/CLAUDE/` ya tiene documentos, ofrece continuar/actualizar en lugar de
  empezar de cero.

## Flujo de trabajo

### Paso 0 — Preparar y contextualizar (una sola vez)

1. Localiza la raíz del proyecto (donde está `.git`, `package.json`, etc.; si no hay, usa el
   directorio de trabajo actual). Crea `docs/CLAUDE/` si falta.
2. Comprueba si ya existen documentos en `docs/CLAUDE/`. Si los hay, pregunta si quiere
   **continuar**, **actualizar uno concreto** o **regenerar**.
3. **Determina si es proyecto NUEVO o EXISTENTE.** Es "existente" si hay código, `.git` con
   historial, `CLAUDE.md`, `README`, `docs/`, etc. En ese caso ejecuta el **reconocimiento** del
   Paso 0-bis ANTES de preguntar nada. La regla de oro: en proyectos existentes **no se pregunta lo
   que se puede leer** — se infiere, se presenta y solo se pide confirmar o corregir.
4. Pregunta el **contexto base** (solo lo que no hayas podido inferir). En proyectos nuevos, una
   tanda corta: nombre del proyecto/app · qué hace y para quién (una frase) · plataforma objetivo
   (Web · Móvil iOS/Android · Ambas · Escritorio) · ¿idea nueva o en marcha?

### Paso 0-bis — Reconocimiento de proyecto existente

Objetivo: reconstruir el contexto a partir de lo que YA hay, para que las preguntas se conviertan en
"confirmar/corregir" en vez de "responder desde cero".

1. **Lee las fuentes de contexto** que existan (de mayor a menor señal):
   - `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md` — instrucciones y
     descripción del proyecto.
   - `README*`, `MVP.md`, `ROADMAP*`, `CHANGELOG*`, `docs/**` (incluye `.es.md`), wikis.
   - Manifiestos: `package.json`, `composer.json`, `pyproject.toml`, `requirements.txt`, `go.mod`,
     `pom.xml`, `Gemfile`, `*.csproj` → stack, scripts, dependencias.
   - Infra: `Dockerfile`, `docker-compose*.yml`, `*-ci.yml`, `.env.template`/`.env.example`,
     `angular.json`/`vite.config`/`next.config`, `capacitor.config`, `ionic.config` → despliegue y plataforma.
   - Estructura de carpetas (árbol de 2-3 niveles, `apps/`, `src/`, `packages/`) y, si hay BD,
     migraciones/esquemas (`migrations/`, `schema.prisma`, `*.sql`, entidades/modelos).
2. **Sintetiza una "Ficha de contexto"** y muéstrala al usuario para validar (no la copies a los
   documentos finales): nombre, propósito, usuarios, plataforma, stack detectado, integraciones,
   modelo de datos entrevisto, estado/madurez y fase actual.
3. **Mapea lo existente contra los 6 documentos.** Para cada uno decide y propón:
   - **Derivar** — ya hay material suficiente (p. ej. un `docs/ARCHITECTURE.md` alimenta el TRD); se
     genera resumiendo/estructurando lo que existe.
   - **Enlazar / no duplicar** — ya existe un documento equivalente y bueno; en `docs/CLAUDE/` se crea
     una ficha breve que **referencia** al original en vez de copiarlo.
   - **Crear** — no hay nada; se genera con las preguntas habituales (que serán pocas).
   Presenta esta tabla de decisión y deja que el usuario la ajuste antes de generar.
4. **Concilia con `docs/` y `CLAUDE.md` existentes:** respeta su estilo e idioma, no contradigas lo ya
   documentado y, si detectas discrepancias entre el código y los docs, **señálalas** en vez de
   sobrescribir. Nunca borres documentación previa.

### Pasos 1–6 — Generar cada documento

Para CADA documento, en orden:

1. **Lee la plantilla** correspondiente en `templates/` (ver tabla abajo) para conocer su estructura.
2. **Haz las preguntas** propias de ese documento (las que indica la plantilla), en tandas cortas.
   Reutiliza lo ya respondido en pasos previos; no repreguntes.
3. **Redacta el documento** en `docs/CLAUDE/NN-<slug>.md` rellenando la plantilla con las respuestas.
   Usa diagramas **Mermaid** donde la plantilla lo indique (flujos y esquema ER), que es el
   equivalente en texto a las diapositivas del concepto original.
4. **Resume** lo generado (2–3 líneas) y pregunta si quiere ajustar algo o **continuar** con el siguiente.
5. Cada documento empieza con un encabezado que incluye el proyecto y una línea
   `> Última actualización: <fecha de hoy>`.

| # | Documento | Fichero salida | Plantilla |
|---|-----------|----------------|-----------|
| 1 | PRD | `docs/CLAUDE/01-prd.md` | `templates/01-prd.md` |
| 2 | TRD | `docs/CLAUDE/02-trd.md` | `templates/02-trd.md` |
| 3 | Diseño UI/UX | `docs/CLAUDE/03-ui-ux.md` | `templates/03-ui-ux.md` |
| 4 | AppFlow | `docs/CLAUDE/04-appflow.md` | `templates/04-appflow.md` |
| 5 | Esquema del BackEnd | `docs/CLAUDE/05-backend-schema.md` | `templates/05-backend-schema.md` |
| 6 | Plan de Implementación | `docs/CLAUDE/06-plan-implementacion.md` | `templates/06-plan-implementacion.md` |

> El usuario puede pedir generar solo algunos documentos; respétalo. El orden recomendado es 1→6
> porque cada uno aporta contexto al siguiente (p. ej. las entidades del PRD alimentan el esquema
> del BackEnd).

### Paso 7 — Índice y referencia en CLAUDE.md

1. Crea/actualiza `docs/CLAUDE/README.md` como índice con enlaces a los 6 documentos y una línea
   de estado (generado / pendiente) por cada uno.
2. Crea o actualiza el **`CLAUDE.md` de la raíz** del proyecto añadiendo (o refrescando) una sección
   delimitada por marcadores para no duplicar en futuras ejecuciones:

```markdown
<!-- BEGIN vibecoding-docs -->
## 📐 Documentación de planificación (docs/CLAUDE/)

Antes de implementar cualquier funcionalidad, consulta y respeta estos documentos:

- [`docs/CLAUDE/01-prd.md`](docs/CLAUDE/01-prd.md) — Requisitos de producto (qué se construye y por qué)
- [`docs/CLAUDE/02-trd.md`](docs/CLAUDE/02-trd.md) — Requisitos técnicos y stack
- [`docs/CLAUDE/03-ui-ux.md`](docs/CLAUDE/03-ui-ux.md) — Sistema de diseño UI/UX
- [`docs/CLAUDE/04-appflow.md`](docs/CLAUDE/04-appflow.md) — Flujo de pantallas / recorrido del usuario
- [`docs/CLAUDE/05-backend-schema.md`](docs/CLAUDE/05-backend-schema.md) — Esquema del backend / modelo de datos
- [`docs/CLAUDE/06-plan-implementacion.md`](docs/CLAUDE/06-plan-implementacion.md) — Plan de implementación

Estos documentos son la fuente de verdad del proyecto. Si una petición los contradice, avísalo.
<!-- END vibecoding-docs -->
```

   - Si `CLAUDE.md` no existe, créalo con un encabezado mínimo (`# <Proyecto>`) y esta sección.
   - Si ya existe la sección entre marcadores, reemplaza solo ese bloque.
   - No toques el resto del `CLAUDE.md`.

3. Cierra resumiendo qué documentos quedaron creados y cuáles pendientes/TODO.

## Buenas prácticas al preguntar

- Una tanda = 2–4 preguntas como máximo. Avanza, no interrogues.
- Para elecciones cerradas (plataforma, framework, base de datos, estilo visual) ofrece opciones
  concretas — usa como repertorio el stack de referencia de `templates/02-trd.md`.
- Para descripciones (problema, usuarios, funcionalidades) deja respuesta abierta.
- Si el usuario dice "tú decide" / "lo que recomiendes", elige por él, justifícalo en una línea y
  sigue; márcalo con `> TODO:` si conviene que lo valide.
- Mantén el foco: el objetivo es dejar documentos accionables, no exhaustivos.
