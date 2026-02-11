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
├── app.py                      # Streamlit UI: upload, solve, display
├── algo.py                     # Backtracking solver
├── ocr.py                      # Extract grid via API call to AI model
├── Dockerfile                  # Cloud Run container config
├── .github/workflows/          # CI/CD pipeline
└── pyproject.toml              # uv dependencies
```

## Deployment

The app runs on **Google Cloud Run** via a GitHub Actions workflow.

### Pipeline

Triggered manually via `workflow_dispatch`:

1. Export `requirements.txt` from `pyproject.toml` using `uv export`
2. Build Docker image from `Dockerfile`
3. Push image to Google Artifact Registry
4. Deploy to Cloud Run

### Configuration

**Required GitHub secrets:**
- `GCP_SA_KEY` - Service account credentials for GCP authentication
- `OPENAI_API_KEY_SUDOKU` - Passed as environment variable to the app

**Required GitHub variables:**
- `GAR_LOCATION` - Artifact Registry location (e.g., `us-central1`)
- `GCP_PROJECT_ID` - Google Cloud project ID
- `GAR_REPOSITORY` - Artifact Registry repository name
- `IMAGE_NAME` - Docker image name
- `CLOUD_RUN_SERVICE` - Cloud Run service name
