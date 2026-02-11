# Sudoku Solver

Upload a photo of a Sudoku puzzle—get the solution.

## Features

- **Photo → Solution**: Upload an image; the app extracts the puzzle via vision AI and solves it.
- **Backtracking solver**: Fast constraint-propagation algorithm.
- **Clear board view**: Given cells in bold, solved cells in blue.

## Quick Start

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/), and an OpenAI API key.

```bash
# Clone and enter the repo
cd sudoku-solver

# Install dependencies
uv sync

# Run the app (set your API key first)
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
