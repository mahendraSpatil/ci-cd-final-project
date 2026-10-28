# ci-cd-final-project
#cicd-final-project
[![CI Build](https://github.com/mahendraSpatil/ci-cd-pipeline-final-project/actions/workflows/workflow.yml/badge.svg)](https://github.com/mahendraSpatil/ci-cd-pipeline-final-project/actions/workflows/workflow.yml)
[![OpenShift Pipelines](https://img.shields.io/badge/OpenShift-Tekton_CI%2FCD-red?logo=redhatopenshift)](https://www.redhat.com/en/technologies/cloud-computing/openshift/pipelines)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A production-grade Python/Flask RESTful microservice for managing user accounts. This project demonstrates modern Cloud Native and CI/CD practices using **GitHub Actions**, **Tekton Pipelines**, and **Red Hat OpenShift**.

---

## 📋 Table of Contents
- [Architecture & Overview](#-architecture--overview)
- [REST API Endpoints](#-rest-api-endpoints)
- [Local Development Setup](#-local-development-setup)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [CI/CD Automation](#-cicd-automation)
  - [1. GitHub Actions Workflow](#1-github-actions-workflow)
  - [2. Tekton Pipelines on OpenShift](#2-tekton-pipelines-on-openshift)
- [Verification & Project Deliverables](#-verification--project-deliverables)

---

## 🏛 Architecture & Overview

The Accounts microservice is structured following modern 12-factor application patterns:
- **Web Framework**: Flask with SQLAlchemy ORM.
- **Database**: PostgreSQL (production) / SQLite in-memory (local development/testing).
- **WSGI Runner**: Gunicorn running on port `8080`.
- **Packaging**: Containerized deployment on Kubernetes / OpenShift.

```
                    ┌─────────────────────────┐
                    │     HTTP Client / UI    │
                    └────────────┬────────────┘
                                 │ :8080
                                 ▼
                    ┌─────────────────────────┐
                    │    Accounts Service     │
                    │   (Flask + Gunicorn)    │
                    └────────────┬────────────┘
                                 │ SQLAlchemy
                                 ▼
                    ┌─────────────────────────┐
                    │       PostgreSQL        │
                    │       Database          │
                    └─────────────────────────┘
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Healthcheck and readiness probe |
| `GET` | `/` | Service root and API info |
| `POST` | `/accounts` | Create a new user account |
| `GET` | `/accounts` | List all existing accounts |
| `GET` | `/accounts/<id>` | Read a specific account by ID |
| `PUT` | `/accounts/<id>` | Update an existing account |
| `DELETE` | `/accounts/<id>` | Delete an account |

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.9+
- `pip` and `virtualenv`
- Git

### 1. Clone the repository
```bash
git clone https://github.com/mahendraSpatil/cd-pipeline-final-project.git
cd cd-pipeline-final-project
```

### 2. Create and activate a Virtual Environment
```bash
# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Application Locally
```bash
gunicorn --bind 0.0.0.0:8080 service:app
```
Test the health endpoint:
```bash
curl -i http://localhost:8080/health
```

---

## 🧪 Testing & Quality Assurance

### Code Linting
Run `flake8` to enforce PEP8 standards and catch syntax errors:
```bash
flake8 service --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 service --count --max-complexity=10 --max-line-length=127 --statistics
```

### Unit Tests & Code Coverage
Execute automated unit tests with `nosetests` or `pytest` including coverage reporting:
```bash
pytest --cov=service --cov-report=term-missing
# or with nosetests
nosetests -v --with-spec --spec-color --with-coverage --cover-package=service
```

---

## 🚀 CI/CD Automation

### 1. GitHub Actions Workflow
On every push or pull request to the `main` branch, the workflow located at [`.github/workflows/workflow.yml`](.github/workflows/workflow.yml) executes:
1. Clones the code via `actions/checkout@v3`.
2. Sets up Python 3.9 via `actions/setup-python@v4`.
3. Installs dependencies from `requirements.txt`.
4. Runs strict linting with `flake8`.
5. Executes all unit test suites with coverage reporting.

### 2. Tekton Pipelines on OpenShift
Cloud-native delivery is managed by Tekton Pipelines inside Red Hat OpenShift:
- **`cleanup` Task**: Wipes stale artifacts from the shared PersistentVolumeClaim (`pipelinerun-pvc`).
- **`git-clone` Task**: Fetches source code from GitHub into the pipeline workspace.
- **`lint` Task**: Validates PEP8 styling.
- **`nose` Task**: Executes unit tests in an isolated `python:3.9-slim` container.

---

## 📂 Verification & Project Deliverables

All course-required manifests and scripts are located in their respective directories:
- `.github/workflows/workflow.yml`: Continuous Integration workflow.
- `.tekton/tasks.yml`: Reusable Tekton tasks (`cleanup` and `nose`).
- `.tekton/pipeline.yml`: Complete Tekton CI/CD pipeline definition.
- `.tekton/pvc.yml`: PersistentVolumeClaim definition for OpenShift.
- `.tekton/pipelinerun.yml`: Pipeline execution manifest.
