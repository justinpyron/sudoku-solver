# Sudoku Solver

A Streamlit web app that solves Sudoku puzzles from uploaded photos.

**How it works:**
1. Upload an image of a sudoku board
2. OpenAI's vision API extracts the grid
3. Backtracking solver computes the solution
4. Solved board displayed in the app

## Quick Start

**Prerequisites:** Python 3.12+ and an OpenAI API key.

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Dependencies

```bash
cd sudoku-solver
uv sync
```

### Run the App

```bash
export OPENAI_API_KEY_SUDOKU=your-api-key
uv run streamlit run app.py
```

## Project Structure

```
├── app.py                      # Streamlit UI: upload, display, solve
├── algo.py                     # Backtracking solver
├── ocr.py                      # Vision API extraction from image
├── Dockerfile                  # Cloud Run container config
├── .github/workflows/          # CI/CD pipeline
└── pyproject.toml              # uv dependencies
```

## Deployment

Docker image builds from `Dockerfile` and runs on **Cloud Run** (port 8080). CI/CD via GitHub Actions:

- **Trigger:** Manual (`workflow_dispatch`)
- **Flow:** `uv export` → build image → push to Artifact Registry → deploy to Cloud Run
- **Secrets:** `OPENAI_API_KEY_SUDOKU` must be set in GitHub and passed as an env var
