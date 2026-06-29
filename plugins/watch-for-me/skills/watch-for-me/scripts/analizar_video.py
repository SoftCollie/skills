#!/usr/bin/env python3
"""
analizar_video.py — Prepara el material para analizar un vídeo sin reproducirlo.

Es el motor de la skill «analizar-video» de Claude Code. Es PORTABLE
(Windows / Linux / macOS) y **gestiona sus propias dependencias**:

  * ffmpeg/ffprobe → usa el del sistema; si no está, instala `imageio-ffmpeg`
    (binario estático vía pip, sin permisos de administrador).
  * yt-dlp        → sólo si la fuente es una URL; se instala vía pip si falta.
  * faster-whisper → sólo con --audio; se instala vía pip si falta.

Lo que NO puede instalar solo (p.ej. ffmpeg del sistema en algún SO sin pip
disponible) lo informa con el comando exacto para ese SO.

Salida: en  <outdir>/<base>_analisis/  →  frames/  sheets/  frames_index.csv
        transcripcion.txt (si --audio)  README_ANALISIS.md
Imprime una última línea  RESULT ...  legible por la skill.

Uso:
  python analizar_video.py <ruta-o-URL> [opciones]
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import platform

IS_WIN = platform.system() == "Windows"


def log(msg):
    print(msg, flush=True)


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


# --------------------------------------------------------------------------- #
#  Gestión de dependencias
# --------------------------------------------------------------------------- #
def pip_install(pkgs, allow_install):
    if not allow_install:
        return False
    log(f"  📦 Instalando dependencias: {', '.join(pkgs)} (pip)…")
    base = [sys.executable, "-m", "pip", "install", "-q", "--upgrade"]
    # 1º intento normal; 2º intento con --user (entornos sin venv)
    for extra in ([], ["--user"]):
        r = subprocess.run(base + extra + list(pkgs))
        if r.returncode == 0:
            return True
    return False


def manual_ffmpeg_hint():
    sysname = platform.system()
    if sysname == "Windows":
        return ("Instala ffmpeg:  winget install Gyan.FFmpeg   (o:  choco install ffmpeg  /  "
                "scoop install ffmpeg)")
    if sysname == "Darwin":
        return "Instala ffmpeg:  brew install ffmpeg"
    # Linux: detectar gestor
    for mgr, cmd in (("apt", "sudo apt install -y ffmpeg"),
                     ("dnf", "sudo dnf install -y ffmpeg"),
                     ("pacman", "sudo pacman -S ffmpeg"),
                     ("zypper", "sudo zypper install ffmpeg")):
        if shutil.which(mgr):
            return f"Instala ffmpeg:  {cmd}"
    return "Instala ffmpeg con el gestor de paquetes de tu sistema."


def ensure_ffmpeg(allow_install):
    """Devuelve (ffmpeg, ffprobe_o_None) o aborta con instrucciones."""
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if ffmpeg:
        return ffmpeg, ffprobe
    # Fallback portable: binario estático vía pip (no necesita admin)
    try:
        import imageio_ffmpeg  # noqa
    except ImportError:
        if not pip_install(["imageio-ffmpeg"], allow_install):
            log("❌ No encuentro ffmpeg y no pude instalarlo automáticamente.")
            log("   " + manual_ffmpeg_hint())
            sys.exit(2)
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        log(f"  ✓ ffmpeg portable (imageio-ffmpeg): {ffmpeg}")
        return ffmpeg, None  # imageio-ffmpeg no trae ffprobe → duración vía ffmpeg
    except Exception:
        log("❌ No encuentro ffmpeg.  " + manual_ffmpeg_hint())
        sys.exit(2)


def ensure_ytdlp(allow_install):
    """Devuelve el comando base para yt-dlp (lista)."""
    exe = shutil.which("yt-dlp")
    if exe:
        return [exe]
    try:
        import yt_dlp  # noqa
        return [sys.executable, "-m", "yt_dlp"]
    except ImportError:
        if pip_install(["yt-dlp"], allow_install):
            return [sys.executable, "-m", "yt_dlp"]
    log("❌ Necesito yt-dlp para descargar URLs y no pude instalarlo.")
    log("   Instálalo con:  pip install -U yt-dlp")
    sys.exit(3)


def ensure_whisper(allow_install):
    try:
        import faster_whisper  # noqa
        return True
    except ImportError:
        if pip_install(["faster-whisper"], allow_install):
            return True
    return False


# --------------------------------------------------------------------------- #
#  Sondas / utilidades
# --------------------------------------------------------------------------- #
def probe_duration(ffmpeg, ffprobe, video):
    if ffprobe:
        r = run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", video])
        try:
            return float(r.stdout.strip())
        except ValueError:
            pass
    # Fallback: parsear la salida de ffmpeg
    r = run([ffmpeg, "-i", video])
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", r.stderr)
    if m:
        h, mi, s = m.groups()
        return int(h) * 3600 + int(mi) * 60 + float(s)
    return 0.0


def auto_interval(duration):
    if duration <= 120:
        return 3
    if duration <= 600:
        return 6
    if duration <= 1800:
        return 12
    if duration <= 3600:
        return 20
    return 30


def hms(seconds):
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m{sec:02d}s"
    return f"{m}m{sec:02d}s"


# --------------------------------------------------------------------------- #
#  Descarga (URLs)
# --------------------------------------------------------------------------- #
def is_url(s):
    return s.startswith("http://") or s.startswith("https://")


def download_url(ytdlp, url, outdir, cookies_browser, cookies_file):
    os.makedirs(outdir, exist_ok=True)
    stage = os.path.join(outdir, ".descarga_tmp")
    if os.path.isdir(stage):
        shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage, exist_ok=True)
    log("⬇️   Descargando vídeo de la URL con yt-dlp…")
    args = ytdlp + ["--no-playlist", "--restrict-filenames",
                    "--merge-output-format", "mp4",
                    "-o", os.path.join(stage, "%(title).80s-%(id)s.%(ext)s")]
    if cookies_browser:
        args += ["--cookies-from-browser", cookies_browser]
    if cookies_file:
        args += ["--cookies", cookies_file]
    args.append(url)
    if subprocess.run(args).returncode != 0:
        log("❌ La descarga falló. Si requiere login (p.ej. Instagram privado), usa")
        log("   --cookies-from-browser firefox  (o chrome/brave).")
        shutil.rmtree(stage, ignore_errors=True)
        sys.exit(4)
    # localizar el fichero de vídeo (el más grande; excluye sidecars)
    cands = []
    for f in os.listdir(stage):
        p = os.path.join(stage, f)
        if os.path.isfile(p) and not f.endswith((".part", ".json", ".jpg",
                                                  ".png", ".webp", ".vtt", ".srt")):
            cands.append((os.path.getsize(p), p))
    if not cands:
        log("❌ No encuentro el vídeo descargado.")
        shutil.rmtree(stage, ignore_errors=True)
        sys.exit(4)
    src = max(cands)[1]
    final = os.path.join(outdir, os.path.basename(src))
    shutil.move(src, final)
    shutil.rmtree(stage, ignore_errors=True)
    log(f"✅  Descargado: {final}")
    return final


# --------------------------------------------------------------------------- #
#  Extracción de fotogramas
# --------------------------------------------------------------------------- #
def extract_periodic(ffmpeg, video, tmpdir, interval, width):
    out = os.path.join(tmpdir, "p_%04d.jpg")
    run([ffmpeg, "-y", "-loglevel", "error", "-i", video,
         "-vf", f"fps=1/{interval},scale={width}:-1", "-qscale:v", "3", out])
    frames = []
    for f in sorted(os.listdir(tmpdir)):
        m = re.match(r"p_(\d+)\.jpg$", f)
        if m:
            t = (int(m.group(1)) - 1) * interval
            frames.append((t, "periodico", os.path.join(tmpdir, f)))
    return frames


def extract_scenes(ffmpeg, video, tmpdir, threshold, width):
    # La ruta de metadata=print:file= va DENTRO del filtergraph (donde [ ] : y los
    # espacios son especiales). Por eso se ejecuta con cwd=tmpdir y nombre relativo
    # limpio; el -i input sí admite ruta absoluta con corchetes/espacios.
    run([ffmpeg, "-y", "-loglevel", "error", "-i", os.path.abspath(video),
         "-vf", (f"select='gt(scene,{threshold})',scale={width}:-1,"
                 f"metadata=print:file=scenes_meta.txt"),
         "-vsync", "vfr", "-qscale:v", "3", "s_%04d.jpg"], cwd=tmpdir)
    times = []
    meta = os.path.join(tmpdir, "scenes_meta.txt")
    if os.path.exists(meta):
        with open(meta) as fh:
            for line in fh:
                m = re.search(r"pts_time:([0-9.]+)", line)
                if m:
                    times.append(float(m.group(1)))
    frames = []
    scene_files = sorted(f for f in os.listdir(tmpdir) if re.match(r"s_\d+\.jpg$", f))
    for i, f in enumerate(scene_files):
        t = times[i] if i < len(times) else 0.0
        frames.append((t, "escena", os.path.join(tmpdir, f)))
    return frames


def dedup_and_cap(frames, min_gap, max_frames):
    frames.sort(key=lambda x: (x[0], 0 if x[1] == "escena" else 1))
    kept = []
    for t, typ, path in frames:
        if kept and (t - kept[-1][0]) < min_gap:
            if typ == "escena" and kept[-1][1] != "escena":
                kept[-1] = (t, typ, path)
            continue
        kept.append((t, typ, path))
    if len(kept) > max_frames:
        scenes = [f for f in kept if f[1] == "escena"]
        periodic = [f for f in kept if f[1] != "escena"]
        budget = max(0, max_frames - len(scenes))
        if budget and periodic:
            step = len(periodic) / budget
            periodic = [periodic[int(i * step)] for i in range(budget)]
        kept = sorted(scenes + periodic, key=lambda x: x[0])
    return kept


def build_contact_sheets(ffmpeg, video, sheets_dir, interval, thumb_w, cols, rows):
    # Receta canónica: tile DIRECTAMENTE sobre el vídeo. Hacer tile sobre imágenes
    # pre-extraídas falla (el demuxer image2 sólo entrega 2 frames al filtro tile).
    os.makedirs(sheets_dir, exist_ok=True)
    out = os.path.join(sheets_dir, "contact_%02d.jpg")
    r = run([ffmpeg, "-y", "-loglevel", "error", "-i", video,
             "-vf", (f"fps=1/{interval},scale={thumb_w}:-1,"
                     f"tile={cols}x{rows}:padding=6:margin=6:color=white"),
             "-qscale:v", "3", out])
    return r.returncode == 0


# --------------------------------------------------------------------------- #
#  Transcripción (opcional)
# --------------------------------------------------------------------------- #
def transcribe(ffmpeg, video, outdir, model_name):
    from faster_whisper import WhisperModel
    wav = os.path.join(outdir, ".audio_16k.wav")
    run([ffmpeg, "-y", "-loglevel", "error", "-i", video,
         "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav])
    if not os.path.exists(wav):
        return None
    log(f"  🎙  Transcribiendo con faster-whisper ({model_name}, CPU int8)…")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(wav, vad_filter=True)
    txt = os.path.join(outdir, "transcripcion.txt")
    with open(txt, "w", encoding="utf-8") as fh:
        for seg in segments:
            fh.write(f"[{hms(seg.start)} → {hms(seg.end)}] {seg.text.strip()}\n")
    os.remove(wav)
    return txt


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="ruta local o URL (IG/YouTube/TikTok/…)")
    ap.add_argument("--outdir", default=".", help="dónde guardar (def: actual)")
    ap.add_argument("--interval", type=int, default=0)
    ap.add_argument("--max-frames", type=int, default=240)
    ap.add_argument("--scene-threshold", type=float, default=0.4)
    ap.add_argument("--no-scene", action="store_true")
    ap.add_argument("--thumb", type=int, default=768)
    ap.add_argument("--sheet-thumb", type=int, default=384)
    ap.add_argument("--sheet-cols", type=int, default=5)
    ap.add_argument("--sheet-rows", type=int, default=4)
    ap.add_argument("--audio", action="store_true", help="transcribe el audio")
    ap.add_argument("--whisper-model", default="small")
    ap.add_argument("--cookies-from-browser", default="")
    ap.add_argument("--cookies", default="")
    ap.add_argument("--no-install", action="store_true",
                    help="no instalar dependencias automáticamente; sólo informar")
    args = ap.parse_args()
    allow = not args.no_install

    log("🔧 Comprobando dependencias…")
    ffmpeg, ffprobe = ensure_ffmpeg(allow)

    # Fuente: URL → descargar
    source = args.source
    if is_url(source):
        ytdlp = ensure_ytdlp(allow)
        source = download_url(ytdlp, source, os.path.abspath(args.outdir),
                              args.cookies_from_browser, args.cookies)

    video = os.path.abspath(source)
    if not os.path.isfile(video):
        log(f"❌ No existe: {video}")
        sys.exit(1)

    base = os.path.splitext(os.path.basename(video))[0]
    outdir = os.path.join(os.path.dirname(video), f"{base}_analisis")
    frames_dir = os.path.join(outdir, "frames")
    sheets_dir = os.path.join(outdir, "sheets")
    tmpdir = os.path.join(outdir, ".tmp_frames")
    for d in (frames_dir, sheets_dir, tmpdir):
        os.makedirs(d, exist_ok=True)

    duration = probe_duration(ffmpeg, ffprobe, video)
    interval = args.interval or auto_interval(duration)
    if duration and duration / interval > args.max_frames:
        interval = int(duration / args.max_frames) + 1

    log(f"🎬 {os.path.basename(video)}  ·  {hms(duration)}  ·  intervalo {interval}s")
    log("🖼  Extrayendo fotogramas…")
    frames = extract_periodic(ffmpeg, video, tmpdir, interval, args.thumb)
    n_periodic = len(frames)
    n_scene = 0
    if not args.no_scene:
        scenes = extract_scenes(ffmpeg, video, tmpdir, args.scene_threshold, args.thumb)
        n_scene = len(scenes)
        frames += scenes

    frames = dedup_and_cap(frames, max(1.0, interval * 0.4), args.max_frames)

    with open(os.path.join(outdir, "frames_index.csv"), "w", encoding="utf-8") as csv:
        csv.write("idx,segundos,hms,tipo,fichero\n")
        for idx, (t, typ, src) in enumerate(frames):
            tag = "_CORTE" if typ == "escena" else ""
            name = f"f{idx:03d}__{hms(t)}{tag}.jpg"
            shutil.move(src, os.path.join(frames_dir, name))
            csv.write(f"{idx},{int(round(t))},{hms(t)},{typ},frames/{name}\n")
    shutil.rmtree(tmpdir, ignore_errors=True)

    ok = build_contact_sheets(ffmpeg, video, sheets_dir, interval,
                              args.sheet_thumb, args.sheet_cols, args.sheet_rows)
    n_sheets = len([f for f in os.listdir(sheets_dir)
                    if f.startswith("contact_")]) if ok else 0

    # Audio (opcional)
    transcript_note = "(sin transcripción)"
    if args.audio:
        if ensure_whisper(allow):
            try:
                txt = transcribe(ffmpeg, video, outdir, args.whisper_model)
                transcript_note = "transcripcion.txt" if txt else "(la transcripción falló)"
            except Exception as e:
                transcript_note = f"(la transcripción falló: {e})"
        else:
            transcript_note = ("(faster-whisper no disponible; instala con "
                               "`pip install faster-whisper` o usa sin --audio)")

    # README
    with open(os.path.join(outdir, "README_ANALISIS.md"), "w", encoding="utf-8") as fh:
        fh.write(f"""# Material de análisis: {os.path.basename(video)}

- `sheets/contact_NN.jpg` — rejillas de miniaturas en orden cronológico (izq→der,
  arriba→abajo). Una miniatura cada **{interval}s**; la miniatura nº k (desde 0) ≈ k×{interval}s.
  Empieza por aquí para la visión global.
- `frames/fNNN__<timestamp>.jpg` — fotogramas a resolución completa; el nombre lleva el
  **timestamp** (p.ej. `f042__12m30s.jpg` = 12:30). Sufijo `_CORTE` = cambio de escena.
- `frames_index.csv` — idx, segundos, hms, tipo, fichero.
- `transcripcion.txt` — transcripción del audio si se generó. Estado: {transcript_note}

Origen: {video}
""")

    log(f"✅ Material listo en: {outdir}")
    log(f"   {len(frames)} fotogramas (periódicos≈{n_periodic}, cortes={n_scene}), "
        f"{n_sheets} contact sheets · audio: {transcript_note}")
    log(f"RESULT outdir={outdir} frames={len(frames)} cortes={n_scene} "
        f"sheets={n_sheets} interval={interval} duration={int(round(duration))}")


if __name__ == "__main__":
    main()
