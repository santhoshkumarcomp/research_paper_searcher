# 🧬 PubMed Research Paper Fetcher

A Python-based CLI and Flask web service that fetches PubMed articles based on user queries, filters for authors affiliated with pharmaceutical or biotech companies, and exports the results as a downloadable CSV file.

---

## 📦 Features

- ✅ Fetch research papers using the **PubMed API**
- ✅ Parse **XML responses** to JSON using `xmltodict`
- ✅ Identify authors affiliated with **non-academic institutions**
- ✅ Extract:
  - PubMed ID
  - Title
  - Publication Date
  - Company-affiliated authors
  - Corresponding author emails
- ✅ Export results as **CSV**
- ✅ Web API via **Flask**
- ✅ Command-line interface via **Poetry**

---

## 🚀 Usage Options

### 🔹 1. Web Interface (Flask)

Start the server:

```bash
poetry run python research_paper_searcher/app.py


Make a request from browser:

/get-data?search=your+query
Downloads a filtered report.csv file in the response.

### 🔹 2. Command Line Tool
poetry install
Once installed, you can use the CLI:


poetry run get-papers-list "cancer vaccine" --debug --file "your_filename.csv" (This will get us the csv file in the project folder)

| Flag            | Description                               |
| --------------- | ----------------------------------------- |
| `-h`, `--help`  | Show usage instructions                   |
| `-d`, `--debug` | Print debug info during execution         |
| `-f`, `--file`  | Specify output filename (default: stdout) |

```
