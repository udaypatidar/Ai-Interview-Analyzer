# Ai Interview Analyzer

## Overview

Ai Interview Analyzer is a lightweight web-backed tool that transcribes and analyzes interview or practice audio to provide scoring, feedback, and visual results to help candidates improve their speaking and content.

## Purpose

Helps candidates practice technical and behavioral interviews by providing automated transcription, scoring, and actionable feedback on responses.

## Key Features

- Automatic audio upload and processing (uses bundled `ffmpeg`).
- Transcription and question/answer scoring.
- Result summary pages with feedback and metrics.
- Simple HTML/CSS frontend with upload/result views in `Templates/`.

## Tech Stack

- Python backend (entry: `demo.py`)
- HTML/CSS frontend (templates under `Templates/`)
- Local `ffmpeg` bundle included under `ffmpeg-8.1.1-essentials_build/` for audio handling

## Quick Start

1. (Optional) create and activate a Python virtual environment.
2. Install dependencies (if any) listed in `requirements.txt`.
3. Run the app:

```bash
python Ai_interview_analyzer/demo.py
```

## Files of interest

- `Ai_interview_analyzer/demo.py` — application entry point
- `Ai_interview_analyzer/Templates/` — HTML templates (`index.html`, `practice.html`, `result.html`)
- `uploads/` — user uploads (recommended to keep out of Git)

## Notes

- Add a `requirements.txt` if your project depends on external packages.
- This repository should exclude large media in `uploads/` from Git; see `.gitignore`.

If you want, I can also create `requirements.txt`, a license file, and set up GitHub Actions for CI.
