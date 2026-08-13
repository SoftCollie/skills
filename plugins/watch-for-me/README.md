# watch-for-me · a Claude Code skill

Let Claude **watch the video for you**, **without playing it**. From a **local path** or a
**URL** (Instagram, YouTube, TikTok, X/Twitter…) it extracts the key frames (interval
sampling + scene-cut detection), builds *contact sheets* and, optionally, transcribes the
audio. Claude then **reads the frames** and the transcript, writes a `SUMMARY.md` and stays
available to answer questions about the video (reopening specific frames to be accurate).

It works because Claude Code's file-reading tool **renders images**: no separate vision
model and no API keys required.

## Install

### As a marketplace plugin (recommended)

```text
/plugin marketplace add SoftCollie/skills
/plugin install watch-for-me@softcollie
```

### As an npm package

```bash
npx @softcollie/watch-for-me-skill
```

This copies the skill into `~/.claude/skills/watch-for-me`. Restart Claude Code and use it
with `/watch-for-me`.

## Usage

Inside Claude Code:

```text
/watch-for-me https://www.instagram.com/reel/XXXX/
/watch-for-me /path/to/talk.mp4
/watch-for-me https://youtu.be/XXXX  (and ask it to transcribe the audio)
```

Or just ask in plain language: *"watch this video for me: <url>"*.

> **Instagram**: works **automatically — no login, no cookies, nothing on your side**. IG
> blocks anonymous access, so for Instagram URLs the skill launches an **internal headless
> browser** (Playwright/Chromium) that resolves the video for you. The first run downloads
> ~120 MB of Chromium. This is the most fragile part (it depends on a downloader site); if
> it ever breaks, hand it the already downloaded `.mp4`.

## Dependencies (automatic, cross-platform)

The skill **manages its own dependencies**:

| Dependency | What for | How it is resolved |
|------------|----------|--------------------|
| `ffmpeg` | extract frames and contact sheets | uses the system one; if missing, installs `imageio-ffmpeg` (portable binary via pip, no admin rights) |
| `yt-dlp` | download URLs (YouTube/TikTok/X…) | installed via pip when the source is a URL |
| `playwright` + Chromium | resolve **Instagram** without login | installs itself (pip + `playwright install chromium`, ~120 MB) the first time you pass an IG URL |
| `faster-whisper` | transcribe audio (optional) | installed via pip only when you pass `--audio` |

Anything it cannot install on its own (e.g. system `ffmpeg` in an environment without pip)
is reported with the exact command for your OS (Windows / Linux / macOS).

## What it produces

Next to the video, a `<name>_analisis/` folder:

- `sheets/contact_NN.jpg` — thumbnail grids in chronological order (the global picture).
- `frames/fNNN__<timestamp>.jpg` — full-resolution frames; the filename carries the
  timestamp and `_CORTE` marks a scene change.
- `frames_index.csv` — frame index (idx, seconds, hms, type, file).
- `transcripcion.txt` — transcript with timestamps (when `--audio` was requested).
- `SUMMARY.md` — the summary Claude writes.

> The engine script (`analizar_video.py`) and the file names it produces are still in
> Spanish; only its console output is affected. Everything the agent writes is in your
> language.

## License

MIT
