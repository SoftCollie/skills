# watch-for-me · skill de Claude Code

Que Claude **mire el vídeo por ti**, **sin reproducirlo**. A partir de una **ruta local** o una **URL**
(Instagram, YouTube, TikTok, Twitter/X…) extrae los fotogramas clave (muestreo periódico
+ detección de cortes de escena), genera *contact sheets* y, opcionalmente, transcribe el
audio. Después Claude **lee los fotogramas** y la transcripción, escribe una `SINTESIS.md`
y queda disponible para responder preguntas sobre el vídeo (reabriendo fotogramas
concretos para ser preciso).

Funciona porque la herramienta de lectura de archivos de Claude Code **renderiza
imágenes**: no hace falta un modelo de visión aparte ni claves de API.

## Instalación

### Como plugin del marketplace (recomendado)

```text
/plugin marketplace add SoftCollie/skills
/plugin install watch-for-me@softcollie
```

### Como paquete npm

```bash
npx @softcollie/watch-for-me-skill
```

Copia la skill en `~/.claude/skills/watch-for-me`. Reinicia Claude Code y úsala con
`/watch-for-me`.

## Uso

Dentro de Claude Code:

```text
/watch-for-me https://www.instagram.com/reel/XXXX/
/watch-for-me /ruta/a/charla.mp4
/watch-for-me https://youtu.be/XXXX  (y pídele que transcriba el audio)
```

O simplemente pídeselo en lenguaje natural: *"mírame este vídeo: <url>"*.

> **Instagram**: IG suele exigir login y bloquea la descarga anónima. Usa
> `--cookies-from-browser firefox|chrome`, **o** descarga el reel con un downloader web y
> pásale el **archivo** o el **enlace directo del .mp4**. La skill acepta ruta o URL.

## Dependencias (automáticas, multiplataforma)

La skill **gestiona sus dependencias**:

| Dependencia | Para qué | Cómo se resuelve |
|-------------|----------|------------------|
| `ffmpeg` | extraer fotogramas y contact sheets | usa el del sistema; si falta, instala `imageio-ffmpeg` (binario portable vía pip, sin admin) |
| `yt-dlp` | descargar URLs | se instala vía pip si la fuente es una URL |
| `faster-whisper` | transcribir audio (opcional) | se instala vía pip sólo al pedir `--audio` |

Lo que no pueda instalar solo (p.ej. `ffmpeg` del sistema en un entorno sin pip), lo
informa con el comando exacto para tu SO (Windows / Linux / macOS).

## Qué genera

Junto al vídeo, una carpeta `<nombre>_analisis/`:

- `sheets/contact_NN.jpg` — rejillas de miniaturas en orden cronológico (visión global).
- `frames/fNNN__<timestamp>.jpg` — fotogramas a resolución completa; el nombre lleva el
  timestamp y `_CORTE` marca un cambio de escena.
- `frames_index.csv` — índice de fotogramas (idx, segundos, hms, tipo, fichero).
- `transcripcion.txt` — transcripción con timestamps (si se pidió `--audio`).
- `SINTESIS.md` — la síntesis que escribe Claude.

## Licencia

MIT
