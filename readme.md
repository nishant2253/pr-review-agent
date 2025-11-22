# 🚀 Automated GitHub Pull Request Review Agent

An AI-powered backend system that automatically analyzes GitHub Pull Requests and generates structured, actionable review comments—just like an experienced software engineer.

This project uses multi-agent reasoning, Gemini 2.0 Flash, and asynchronous orchestration to review code across logic, readability, performance, and security.

---

## ⭐ 1. Project Overview

This project automates the code review workflow by:

- **Fetching PR diffs** using GitHub API
- **Parsing and understanding** changed code lines
- **Running four specialized AI agents** in parallel
- **Aggregating their insights** into a single structured review
- **Returning a professional-grade review** response

Built entirely in **FastAPI**, **LangChain**, and the **Gemini LLM**, this backend reflects real-world engineering tasks.

---

## 🎥 Demo Video

Watch the full demonstration of the PR Review Agent in action:

[![PR Review Agent Demo](https://img.youtube.com/vi/KcGWHJFcSpE/maxresdefault.jpg)](https://youtu.be/KcGWHJFcSpE)

**[▶️ Watch on YouTube](https://www.youtube.com/watch?v=KcGWHJFcSpE)**

---

## ⭐ 2. High-Level Architecture

```
          GitHub PR
              │
              ▼
     [ GitHub Service ]
     - Fetch PR diff
              │
              ▼
     [ Diff Parser ]
     - Splits into hunks/files
              │
              ▼
      ┌────────────────────────────┐
      │   Multi-Agent Engine       │
      │  (Runs in parallel)        │
      │                            │
      │  • Logic Agent             │
      │  • Readability Agent       │
      │  • Performance Agent       │
      │  • Security Agent          │
      └────────────────────────────┘
              │
              ▼
     [ Aggregator Agent ]
     - Normalize
     - Deduplicate
     - Severity ranking
              │
              ▼
     Structured ReviewResponse JSON
```

Each agent focuses on one responsibility and operates independently using Gemini.

---

## ⭐ 3. Directory Structure

```
pr-review-agent/
│
├── app/
│   ├── api/
│   │   └── review_routes.py
│   │
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── logic_agent.py
│   │   ├── readability_agent.py
│   │   ├── performance_agent.py
│   │   ├── security_agent.py
│   │   └── aggregator_agent.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── settings.py
│   │   └── logger.py
│   │
│   ├── models/
│   │   ├── review_request.py
│   │   ├── review_response.py
│   │   └── review_comment.py
│   │
│   ├── services/
│   │   ├── diff_parser.py
│   │   ├── github_service.py
│   │   └── review_orchestrator.py
│   │
│   └── main.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⭐ 4. Multi-Agent Review Logic (Parallel Execution)

When a diff arrives, the orchestrator triggers:

### ✔ Logic Agent

Detects incorrect conditions, missing edge cases, incorrect returns, off-by-one errors.

### ✔ Readability Agent

Flags unclear names, deeply nested code, missing comments, inconsistent style.

### ✔ Performance Agent

Identifies heavy loops, repeated calculations, I/O bottlenecks, N+1 patterns.

### ✔ Security Agent

Finds insecure inputs, hard-coded secrets, weak crypto usage, missing auth checks.

### ⚡ How They Run in Parallel

```python
logic_task = run_logic_agent(diff_text)
read_task  = run_readability_agent(diff_text)
perf_task  = run_performance_agent(diff_text)
sec_task   = run_security_agent(diff_text)

logic, read, perf, sec = await asyncio.gather(
    logic_task, read_task, perf_task, sec_task
)
```

This cuts latency by **75%**, giving ultra-fast reviews.

---

## ⭐ 5. Backend API Routes

### `POST /review/diff`

Input: manually provided unified diff.

**Request:**

```json
{
  "diff": "diff --git a/app.py b/app.py ..."
}
```

**Response:** structured review.

---

### `POST /review/pr`

Fetches diff from GitHub automatically and runs full review.

**Request body:**

```json
{
  "owner": "octocat",
  "repo": "Hello-World",
  "pr_number": 1
}
```

**Response:** structured `ReviewResponse`.

---

## ⭐ 6. Important Files Explained

### `github_service.py`

Fetches PR diff using:

```
Accept: application/vnd.github.v3.diff
```

Fully async, logs every step.

### `base_agent.py`

The brain of every agent:

- Builds structured prompts
- Calls Gemini using `ainvoke()`
- Ensures output is pure JSON
- Handles failures gracefully

### `review_orchestrator.py`

Main orchestrator that:

- Parses diff
- Runs agent tasks in parallel
- Aggregates comments
- Returns final `ReviewResponse`

### `aggregator_agent.py`

Responsible for:

- Severity normalization
- Deduplication
- Sorting comments
- Summary generation

---

## ⭐ 7. How to Run the Project Locally

### 1. Clone repository

```bash
git clone <your-repo>
cd pr-review-agent
```

### 2. Create virtual environment

**Using conda:**

```bash
conda create -n pr-agent python=3.10
conda activate pr-agent
```

**Or using venv:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Copy `.env.example`:

```bash
cp .env.example .env
```

Set values inside (see section 8 below).

### 5. Run FastAPI backend

```bash
uvicorn app.main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## ⭐ 8. `.env.example`

```env
# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Gemini Model
GEMINI_MODEL_NAME=gemini-2.0-flash

# Optional GitHub Token (required for private repos)
GITHUB_TOKEN=ghp_yourtokenhere
```

---

## ⭐ 9. Testing the APIs

### Test Manual Diff Review

```bash
curl -X POST http://127.0.0.1:8000/review/diff \
  -H "Content-Type: application/json" \
  -d '{"diff": "diff --git a/app.py b/app.py\n@@ -1,4 +1,4 @@\nprint(\"Hello\")"}'
```

### Test GitHub PR Review

```bash
curl -X POST http://127.0.0.1:8000/review/pr \
  -H "Content-Type: application/json" \
  -d '{"owner":"octocat","repo":"Hello-World","pr_number":1}'
```

---

## ⭐ 10. Final Output Format

Every response returns:

```json
{
  "summary": "Found X potential issue(s)...",
  "comments": [
    {
      "file": "app.py",
      "line": 12,
      "severity": "HIGH",
      "category": "LOGIC",
      "comment": "Incorrect condition...",
      "suggestion": "Use === instead..."
    }
  ]
}
```

Clean, structured, and ready for PR annotations.

---

## ⭐ 11. Future Enhancements (Optional)

- [ ] Auto-comment back on GitHub PR
- [ ] Support for multi-file PR annotations
- [ ] Caching API calls
- [ ] Add more agents (security deep-scan, style guide agent)
- [ ] Add frontend dashboard for reviewing results

---

## 📄 License

MIT License - feel free to use this project for learning and production use.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📧 Contact

For questions or feedback, reach out via GitHub issues.

---

**Built with ❤️ using FastAPI, LangChain, and Gemini AI**
