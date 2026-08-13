---
name: watch-for-me
description: Watch a video for the user WITHOUT playing it — from a local path or a URL (Instagram, YouTube, TikTok, X/Twitter, etc.) extract the key frames (interval sampling + scene-cut detection), contact sheets and, optionally, the audio transcript; then summarize everything into SUMMARY.md and stay available to answer questions about the video, reopening specific frames when needed. Use it when the user wants to "analyze/summarize a video", asks "what happens in this reel/short/clip", wants to understand a video without watching it end to end, or asks about a specific moment in a video. Cross-platform (Windows/Linux/macOS); manages its own dependencies.
---

# watch-for-me — let Claude watch the video for you

This skill prepares the visual and textual material of a video, and then **you (the agent)
analyze it by reading the frames** (your file-reading tool renders images), producing a
summary the user can keep talking to you about.

The source can be a **local file** or a **URL** (Instagram, YouTube, TikTok, X/Twitter,
etc.): URLs are downloaded with `yt-dlp`.

## Dependencies (automatic)

The bundled script **manages its own dependencies**: it uses the system `ffmpeg` or, if
missing, installs a portable binary via `pip install imageio-ffmpeg` (no admin rights);
installs `yt-dlp` for regular URLs; installs **Playwright + Chromium** only when the URL is
an Instagram one (automatic resolution, see below); and installs `faster-whisper` only when
audio is requested. If something cannot be installed automatically (e.g. system ffmpeg on a
machine without pip), the script prints the exact command for the user's OS — **relay that
message to the user**.

## Instagram (automatic, no login)

`yt-dlp` downloads YouTube, TikTok, X/Twitter and friends directly. **Instagram blocks
anonymous access**, so for Instagram URLs the script resolves it **on its own**: it launches
an **internal headless browser** (Playwright/Chromium) that fetches the video through a web
downloader — **no login, no cookies, nothing for the user to do**. The first run downloads
~120 MB of Chromium (installed automatically).

Notes:
- This is the **most fragile** part of the flow (it depends on a downloader site's HTML). If
  it fails (site down or changed), tell the user: they can hand you the already downloaded
  **.mp4 file**, or use `--cookies-from-browser firefox|chrome`.
- On very minimal servers, headless Chromium may need system libraries
  (`python -m playwright install-deps chromium`). Not needed on a normal desktop.

## Workflow

1. **Identify the source** in the user's request: a file path or a URL. If it is unclear,
   ask for it. Instagram downloads itself (headless browser); only if the script reports
   that the IG resolution failed, offer the alternatives from the section above.

2. **Locate the Python interpreter** (`python3` on Linux/macOS, `python` on Windows) and
   this skill's script: `scripts/analizar_video.py` (next to this SKILL.md).

3. **Run the script** to prepare the material. Template:

   ```bash
   python3 "<this-skill-dir>/scripts/analizar_video.py" "<PATH-OR-URL>" --outdir "<working-folder>"
   ```

   Useful options you can add depending on what the user asks for:
   - `--audio` → transcribe the audio (faster-whisper, CPU). Add it when the user cares
     about what is being said / there is meaningful dialogue. Off by default (faster).
   - `--interval N` → seconds between frames (default: automatic, based on duration).
   - `--scene-threshold T` → cut sensitivity 0..1 (default 0.4; lower = more cuts).
   - `--max-frames M` → frame cap (default 240).
   - `--cookies-from-browser firefox|chrome|brave` → for URLs behind a login (private
     Instagram accounts).

   If the script exits with a dependency error, **show the user the install command it
   printed** and stop until they resolve it.

4. **Read the material** in the `<base>_analisis/` folder reported by the `RESULT` line:
   - Start with the **contact sheets** (`sheets/contact_NN.jpg`) for the global picture.
   - Then the **transcript** (`transcripcion.txt`) if present.
   - Open **individual frames** (`frames/fNNN__<timestamp>.jpg`) wherever you need detail.
     The filename carries the timestamp; the `_CORTE` suffix marks a scene change. Use
     `frames_index.csv` to locate moments.

   (The script writes those Spanish file and folder names; they are the literal names on
   disk.)

5. **Write `SUMMARY.md`** in that folder with at least:
   - **Executive summary** (2-4 sentences).
   - **Timeline** with timestamps (what happens and when).
   - **Topics / sections**.
   - **Key visual elements**: on-screen text, slides, people, places, objects, charts.
   - **Relevant facts/quotes** from the audio (when a transcript exists).

6. **Summarize on screen** briefly and **stay available** for questions. When the user asks
   about a specific moment, **reopen the corresponding frame(s)** before answering, so you
   are precise (never make up what you have not looked at).

## Rules

- Write in **the user's language** — match the language they are using; default to English.
- Never assert visual details you have not confirmed by looking at the actual frame.
- Always cite **timestamps** when describing moments of the video.
- If the video is long and there are a lot of frames, lean on the contact sheets and open
  only the relevant frames, to avoid burning context.
- Rights: the skill does not vet where the video comes from; assume the user is entitled to
  analyze the content they hand you.
