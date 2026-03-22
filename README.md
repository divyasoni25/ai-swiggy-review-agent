
# AI Review Trend Agent

**Automated Agentic System for Trend Analysis of App Store Reviews**

---

## Overview

The **AI Review Trend Agent** is an end-to-end, production-oriented system designed to ingest daily Google Play Store reviews and generate a rolling **30-day trend analysis** of user issues, requests, and feedback.

The system uses an **agentic AI architecture** combining rule-based taxonomy, semantic normalization, memory, and autonomous topic discovery to ensure:

* **High recall** (captures most relevant issues)
* **Low duplication** (similar phrases consolidated into a single topic)
* **Scalability** for continuous daily ingestion
* **Actionable insights** for product and operations teams

---

## Key Capabilities

* **Daily Batch Processing** of Google Play Store reviews
* **Multi-issue Extraction** from individual reviews
* **Semantic Deduplication** using embeddings
* **Automatic Taxonomy Discovery** for emerging topics
* **Historical Memory** to track topic evolution
* **Trend Report Generation** (T-30 to T) in CSV format

---

## System Architecture

<img width="1536" height="1024" alt="ChatGPT Image Jan 8, 2026, 10_39_11 PM" src="https://github.com/user-attachments/assets/e53bee0f-4956-4764-a812-b15d1b135871" />


**Agent Pipeline:**

1. **Ingestion Agent**

   * Fetches Google Play Store reviews per date (batch mode)
   * Caches and persists raw data

2. **Extraction Agent**

   * High-recall keyword + taxonomy matching
   * Supports multi-issue extraction from a single review
   * Filters sentiment-only and non-actionable feedback

3. **Auto Taxonomy Agent**

   * Analyzes unmatched reviews
   * Clusters semantically similar text
   * Proposes new topics with keyword sets

4. **Normalization Agent**

   * Deduplicates topics using sentence embeddings
   * Consolidates variations into canonical topics
   * Enforces taxonomy consistency

5. **Memory Agent**

   * Persists topic embeddings
   * Tracks daily frequency per topic

6. **Report Agent**

   * Generates rolling **T-30 to T** trend tables
   * Output in CSV for analytics and dashboards

---

## Output Format

The system produces a structured trend report:

| Topic                         | 2026-01-01 | 2026-01-02 | … | 2026-01-07 |
| ----------------------------- | ---------- | ---------- | - | ---------- |
| delivery delay                | 8          | 5          | … | 8          |
| cancellation fee              | 2          | 1          | … | 5          |
| food quality issue            | 1          | 0          | … | 2          |
| customer support unresponsive | 1          | 2          | … | 4          |

Each cell represents **number of occurrences of the topic on that date**.

---

## Topic Intelligence

### 1. High-Recall Extraction

The Extraction Agent prioritizes recall using:

* Domain-specific keyword patterns
* Multi-issue detection per review
* Noise filtering (emoji, generic praise)

### 2. Semantic Normalization

Similar phrases are deduplicated using embeddings:

* *“Delivery guy was rude”*
* *“Delivery partner behaved badly”*
* *“Delivery person was impolite”*
  → **Delivery partner rude**

### 3. Automatic Topic Discovery

When reviews do not match existing taxonomy:

* Text is clustered semantically
* TF-IDF extracts representative keywords
* New topics are proposed and injected into:

  * `extractor.taxonomy`
  * `normalizer.allowed_topics`

This enables **evolution of the taxonomy without manual rules**.


## Technology Stack

* **Python 3.10**
* **google-play-scraper**
* **SentenceTransformers (MiniLM-L6-v2)**
* **scikit-learn**
* **pandas / numpy**

---

## Project Structure

```
ai-review-agent/
│
├── agents/
│   ├── ingestion_agent.py
│   ├── extraction_agent.py
│   ├── auto_taxonomy_agent.py
│   ├── normalization_agent.py
│   ├── memory_agent.py
│   └── report_agent.py
│
├── data/
│   ├── raw_reviews/
│   └── processed/
│
├── memory/
├── output/
├── main.py
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

Configuration in `main.py`:

```python
agent.run(
    app_id="in.swiggy.android",
    start_date="2026-01-01",
    target_date="2026-01-07"
)
```

---

## Use Case

This system enables:

* **Product teams** to identify emerging UX issues
* **Operations teams** to track logistics and service breakdowns
* **Business stakeholders** to monitor customer sentiment trends over time

Unlike traditional topic modeling (LDA/BERT-based clustering), this system:

* Avoids noisy topic fragmentation
* Preserves semantic consistency
* Supports evolving taxonomies via autonomous discovery

---

## Evaluation Focus

* **High Recall:** Maximum capture of real user issues
* **Low Duplication:** Semantic normalization of near-duplicate topics
* **Scalability:** Batch processing for continuous ingestion
* **Business Interpretability:** Clean topic names, actionable insights

---

## Author

**Divya Soni**
AI & Data Science Engineer
Portfolio: [https://divyagenaidev.lovable.app](https://divyagenaidev.lovable.app)
GitHub: [https://github.com/divyasoni25](https://github.com/divyasoni25)

