# AI381 MLOps Lab 2 - Churn Prediction API

[![CI](https://github.com/JawadAbu-alshar/ai381-mlops-lab2/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/JawadAbu-alshar/ai381-mlops-lab2/actions/workflows/ci.yml)
[![Docker Build and Security Scan](https://github.com/JawadAbu-alshar/ai381-mlops-lab2/actions/workflows/docker.yml/badge.svg?branch=main)](https://github.com/JawadAbu-alshar/ai381-mlops-lab2/actions/workflows/docker.yml)

**Course:** AI381 - Machine Learning Operations  
**University:** Jordan University of Science and Technology (JUST)  
**Instructor:** Dr. Tariq Al-Omari  
**Assignment:** Lab 2 - Bring Your Own Model: Container + CI

## Overview

This project demonstrates an end-to-end MLOps workflow for customer churn prediction. It combines model training, FastAPI inference, automated testing, containerization, CI, security scanning, and container registry publishing.

## Machine Learning Model

- Algorithm: Logistic Regression
- Dataset: `churn_v2.csv`
- Training script: `src/train/train.py`
- Model artifact: `model.joblib`
- F1 score: approximately 0.587
- ROC-AUC: approximately 0.792

## Run the Service with One Command

From the repository root:

```bash
docker build -f Docker/Dockerfile -t ai381-churn:latest . && docker run --rm -p 8000:8000 ai381-churn:latest
```

The service is available at `http://localhost:8000`.

### API Endpoints

Health check:

```bash
curl -i http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

The API returns a `churn_probability` between 0 and 1.

Interactive documentation: http://localhost:8000/docs

## Training

```bash
pip install -r requirements.txt
python src/train/train.py
```

## Automated Testing

```bash
python -m pytest tests/ -v
```

Five tests cover:

1. API contract
2. Model loading
3. Input schema validation
4. Edge cases
5. Deterministic predictions

## Linting

Install Ruff if necessary:

```bash
pip install ruff
```

Run lint checks:

```bash
ruff check src/app/main.py src/train/train.py tests/
```

## Docker Design

The `Docker/Dockerfile` uses:

- A multi-stage build
- A pinned Python base image version (`python:3.14.4-slim`)
- A dedicated non-root runtime user
- A Docker HEALTHCHECK
- A virtual environment copied from the builder stage
- Debian package updates in the runtime image

## GitHub Actions CI/CD

### CI Workflow

`.github/workflows/ci.yml`

Runs on pull requests and pushes to `main`:

- Installs Python dependencies
- Runs Ruff linting
- Executes five pytest tests

### Docker Workflow

`.github/workflows/docker.yml`

- Builds the Docker image
- Runs a Trivy scan for HIGH and CRITICAL vulnerabilities
- Fails when matching vulnerabilities are found
- Logs in to GHCR using `GITHUB_TOKEN`
- Publishes the Docker image on pushes to `main`
- Uses the Git commit SHA as the image tag

GitHub Actions references are pinned to full commit SHAs.

## Security Scanning

Trivy initially detected HIGH and CRITICAL vulnerabilities in Debian packages.

After updating the runtime image packages, the local scan reported zero HIGH/CRITICAL findings with `--ignore-unfixed`.

The Docker security workflow subsequently passed on the pull request and on `main`.

## Published GHCR Image

The image was successfully published, pulled, and tested:

```text
ghcr.io/jawadabu-alshar/ai381-mlops-lab2:2cd4508d84ab690a6cfabba1275c834a9c77b14b
```

Pull the published image:

```bash
docker pull ghcr.io/jawadabu-alshar/ai381-mlops-lab2:2cd4508d84ab690a6cfabba1275c834a9c77b14b
```

Run the published image:

```bash
docker run --rm -p 8001:8000 ghcr.io/jawadabu-alshar/ai381-mlops-lab2:2cd4508d84ab690a6cfabba1275c834a9c77b14b
```

Verified results:

- Docker container status: `healthy`
- `GET /health`: HTTP 200, `{"status":"ok"}`
- `POST /predict`: `{"churn_probability":0.895}` for the tested sample

## Branch Protection and Pull Requests

The `main` branch is protected by an active GitHub ruleset named `Protect main`.

The ruleset requires:

- A pull request before merging
- Successful `lint-and-test` and `docker-build` checks
- An up-to-date branch before merging

Pull Request #1 was merged into `main` after the required checks passed.

## Project Structure

```text
.github/workflows/
    ci.yml
    docker.yml
Docker/
    Dockerfile
    Dockerfile.dockerignore
src/
    app/
        main.py
    train/
        train.py
tests/
    test_api.py
churn_v1.csv
churn_v2.csv
model.joblib
requirements.txt
sample_request.json
README.md
```

## Challenges and Lessons Learned

The project required resolving Docker Desktop integration with WSL2, correcting a GitHub Actions configuration issue, and addressing Debian vulnerabilities reported by Trivy.

Automated testing, pull request checks, container health checks, and GHCR publishing helped establish a repeatable and verifiable deployment process.
