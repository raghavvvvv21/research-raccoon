# 🦝 Research Raccoon: Autonomous Multi-Agent Research Pipeline

Research Raccoon is an autonomous, multi-agent AI pipeline built to automate deep-dive research tasks. Given a single topic, a team of specialized AI agents will autonomously search the live web, scrape relevant articles, synthesize the findings into a structured academic-style report, and ruthlessly critique its own work to ensure quality and factual accuracy.

It features a clean, enterprise-grade web interface powered by Streamlit.

## Core Features

* **Live Web Searching:** Uses the Tavily API to bypass generic AI knowledge cutoffs and fetch the most recent, reliable internet sources.
* **Deep URL Scraping:** Automatically selects the highest-value URL from search results and extracts clean, readable text, stripping away ads and noisy HTML.
* **Multi-Agent Orchestration:** Utilizes a specialized crew of LLM agents (Search Agent, Reader Agent, Writer Chain, and Critic Chain) working in sequence.
* **Self-Critique Mechanism:** The Critic Agent evaluates the final draft, highlighting strengths and areas for improvement before presenting the final result.
* **Interactive UI:** A modern, responsive Streamlit interface that extracts and displays verified source links and allows one-click downloading of the final `.txt` report.

## 📂 Project Structure

```text
.
├── app.py               # The Streamlit web interface and frontend UI logic
├── pipeline.py          # Orchestrates the sequential flow between the agents
├── agents.py            # Defines the LLM models, prompts, and agent behaviors
├── tool.py              # Custom tools (Tavily search and BeautifulSoup web scraper)
├── requirements.txt     # Python dependencies required to run the project
└── __pycache__/         # Compiled Python files (ignored in version control)
