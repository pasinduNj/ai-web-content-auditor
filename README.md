# AI Web Content Auditor

An intelligent, FastAPI-powered system designed to perform deep content audits, brand sentiment scoring, and gap analysis. It leverages Gemma 2 2B via Ollama to provide structured, actionable recommendations for website optimization.

---

## Tech Stack

- **Framework:** FastAPI (Python 3.13)
- **AI Engine:** Ollama (Gemma 2 2B)
- **Web Scraping:** BeautifulSoup4, aiohttp
- **Data Layer:** SQLite (Cache-first architecture)

---

# Setup & Installation (Step-by-Step)

## 1. Prerequisites

Make sure you have:

- Python 3.10+ (recommended 3.11/3.13)
- Git installed
- Ollama installed → https://ollama.com

---

## 2. Install and Prepare Ollama

Start Ollama:

```bash
ollama serve
```

Pull the model:

```bash
ollama pull gemma2:2b
```

Verify:

```bash
ollama list
```

---

## 3. Clone the Repository

```bash
git clone <your-repo-url>
cd web-analyzer
```

---

## 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Environment Configuration

Create a `.env` file in the root directory:

```env
OLLAMA_MODEL=gemma2:2b
BOILERPLATE_WORDS="Cookie Policy,Terms of Service,All rights reserved,Privacy Policy"
```

---

## 7. Run the Application

```bash
uvicorn app.main:app --reload
```

Open in browser:

```text
http://127.0.0.1:8000/docs
```

---

# API Usage

## Endpoint

```http
POST /analyze
```

---

## Request Body

```json
{
  "url": "https://example.com"
}
```

---

## Response (Example)

```json
{
  "status": "Processing started",
  "url": "https://example.com"
}
```

## Notes

Processing runs in the **background**
Results may take **20–60 seconds** depending on system performance
Cached results are returned instantly on repeat requests

---

# 🧠 System Workflow

```text
User Request
   ↓
FastAPI Endpoint
   ↓
Cache Check (SQLite)
   ↓
Async Web Crawler
   ↓
Content Processing
   ↓
LLM Analysis (Gemma via Ollama)
   ↓
Structured Output (Scores + Insights)
```

# Assumptions Made

- The target website is publicly accessible
- The website contains sufficient textual content for analysis
- Ollama is running locally and accessible
- The Gemma model is already downloaded

---

# Known Limitations

it is analyse only three pages

stuctured output i develop for the JSON format

Running Gemma 2B locally on CPU can be slow (20–60 seconds per page)

Pages with very little text may result in limited or fallback analysis

Results are processed asynchronously and not streamed live

Current implementation is suitable for local or small-scale usage (not optimized for high concurrency)

# Future Improvements

increase the structured output can enchance the user readablity
develop analys oll pages
Integrate GPU support for faster inference
Replace local LLM with API-based models (OpenAI / Groq)
Add frontend dashboard for visualization and customerize for camparism URL (campare two websites)
Implement Redis for distributed caching

# Author

Pasindu Jayasinghe
