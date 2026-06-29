---
name: watch-for-me
description: Mira un vídeo por ti SIN reproducirlo — a partir de una ruta local o una URL (Instagram, YouTube, TikTok, etc.) extrae los fotogramas clave (muestreo + detección de cortes), contact sheets y, opcionalmente, la transcripción del audio; luego sintetiza el contenido en SINTESIS.md y queda disponible para responder preguntas sobre el vídeo, reabriendo fotogramas concretos cuando hace falta. Úsala cuando el usuario quiera "analizar/resumir un vídeo", "saber qué pasa en este reel/short/clip", entender un vídeo sin verlo entero, o preguntar por momentos concretos de un vídeo. Multiplataforma (Windows/Linux/macOS); gestiona sus propias dependencias.
---

# watch-for-me — que Claude mire el vídeo por ti

Esta skill prepara material visual y textual de un vídeo y luego **tú (el agente) lo
analizas leyendo los fotogramas** (tu herramienta de lectura de archivos renderiza
imágenes), produciendo una síntesis con la que el usuario puede seguir conversando.

La fuente puede ser un **archivo local** o una **URL** (Instagram, YouTube, TikTok,
Twitter/X, etc.): si es una URL, se descarga con `yt-dlp`.

## Dependencias (automáticas)

El script incluido **gestiona sus dependencias**: usa el `ffmpeg` del sistema o, si no
está, instala un binario portable vía `pip install imageio-ffmpeg` (sin permisos de
admin); instala `yt-dlp` para URLs normales; instala **Playwright + Chromium** sólo si la
URL es de Instagram (resolución automática, ver abajo); e instala `faster-whisper` sólo si
se pide audio. Si algo no se puede instalar solo (p.ej. ffmpeg del sistema sin pip), el
script imprime el comando exacto para el SO del usuario — **relata ese mensaje al usuario**.

## Instagram (automático, sin login)

`yt-dlp` descarga directamente YouTube, TikTok, Twitter/X, etc. **Instagram bloquea el
acceso anónimo**, así que para URLs de Instagram el script lo resuelve **solo**: lanza un
**navegador headless interno** (Playwright/Chromium) que obtiene el vídeo a través de un
descargador web — **sin login, sin cookies y sin que el usuario haga nada**. La primera vez
descarga ~120 MB de Chromium (se instala automáticamente).

Notas:
- Es la parte **más frágil** del flujo (depende del HTML de un sitio descargador). Si falla
  (sitio caído o cambiado), avisa al usuario: puede pasarte el **archivo .mp4** ya
  descargado, o usar `--cookies-from-browser firefox|chrome`.
- En servidores muy mínimos, Chromium headless puede necesitar librerías del sistema
  (`python -m playwright install-deps chromium`). En un escritorio normal no hace falta.

## Flujo de trabajo

1. **Identifica la fuente** en la petición del usuario: una ruta de archivo o una URL.
   Si no está clara, pídela. Instagram se descarga solo (navegador headless); sólo si el
   script informa de que la resolución de IG falló, ofrece las alternativas de esa sección.

2. **Localiza el intérprete de Python** (`python3` en Linux/macOS, `python` en Windows) y
   el script de esta skill: `scripts/analizar_video.py` (está junto a este SKILL.md).

3. **Ejecuta el script** para preparar el material. Plantilla:

   ```bash
   python3 "<dir-de-esta-skill>/scripts/analizar_video.py" "<RUTA-O-URL>" --outdir "<carpeta-de-trabajo>"
   ```

   Opciones útiles que puedes añadir según lo que pida el usuario:
   - `--audio` → transcribe el audio (faster-whisper, CPU). Añádelo si el usuario quiere
     lo que se dice / hay diálogo importante. Por defecto NO transcribe (más rápido).
   - `--interval N` → segundos entre fotogramas (def: automático por duración).
   - `--scene-threshold T` → sensibilidad de cortes 0..1 (def 0.4; menor = más cortes).
   - `--max-frames M` → tope de fotogramas (def 240).
   - `--cookies-from-browser firefox|chrome|brave` → para URLs con login (Instagram privado).

   Si el script termina con un error de dependencia, **muéstrale al usuario el comando de
   instalación que ha impreso** y detente hasta que lo resuelva.

4. **Lee el material** de la carpeta `<base>_analisis/` que indica la línea `RESULT`:
   - Primero las **contact sheets** (`sheets/contact_NN.jpg`) para la visión global.
   - La **transcripción** (`transcripcion.txt`) si existe.
   - Abre **fotogramas individuales** (`frames/fNNN__<timestamp>.jpg`) donde necesites
     detalle. El nombre lleva el timestamp; `_CORTE` marca un cambio de escena. Usa
     `frames_index.csv` para localizar momentos.

5. **Escribe `SINTESIS.md`** en esa carpeta con, como mínimo:
   - **Resumen ejecutivo** (2-4 frases).
   - **Cronología** con timestamps (qué ocurre y cuándo).
   - **Temas / secciones**.
   - **Elementos visuales clave**: texto en pantalla, diapositivas, personas, lugares,
     objetos, gráficos.
   - **Datos/citas** relevantes del audio (si hay transcripción).

6. **Resume por pantalla** brevemente y **quédate disponible** para preguntas. Cuando el
   usuario pregunte por un momento concreto, **reabre el/los fotograma(s)** correspondiente(s)
   antes de responder, para ser preciso (no inventes lo que no has mirado).

## Reglas

- Trabaja en **español** salvo que el usuario pida otro idioma.
- No afirmes detalles visuales que no hayas confirmado mirando el fotograma concreto.
- Cita siempre **timestamps** cuando describas momentos del vídeo.
- Si el vídeo es largo y hay muchísimos fotogramas, apóyate en las contact sheets y abre
  sólo los fotogramas relevantes para no malgastar contexto.
- Derechos: la skill no controla la procedencia del vídeo; asume que el usuario tiene
  derecho a analizar el contenido que te pasa.
