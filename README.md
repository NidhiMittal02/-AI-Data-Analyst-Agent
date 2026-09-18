# 🤖 AI Data Analyst Agent

An AI-powered data analysis web application that allows users to upload datasets and ask analytical questions in natural language.

The application automatically profiles the uploaded dataset, checks data quality, performs reliable numerical analysis using Pandas, generates visualizations, and provides AI-assisted analytical responses.

---

## 🚀 Live Demo

🌐 **Live Application:**  
https://ai-data-analyst-agent-mocha.vercel.app/

---

## 📌 Project Overview

Data analysis often requires knowledge of Python, SQL, or spreadsheet formulas. The **AI Data Analyst Agent** simplifies this process by allowing users to interact with their datasets using natural language.

Users can upload a CSV or Excel file and ask questions such as:

> "What is the total sales?"

> "Show total sales by product."

> "Show the top 2 products by sales."

The application interprets the analytical question, performs calculations on the uploaded dataset, and presents the result in an understandable format.

---

## ✨ Features

### 📂 Dataset Upload

Supports:

- CSV files
- Excel `.xlsx` files
- Excel `.xls` files

---

### 🔍 Automatic Data Profiling

The application automatically analyzes the uploaded dataset and provides information about:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Unique values
- Duplicate rows
- Empty columns
- Numerical statistics

---

### 🧹 Data Quality Analysis

The system checks the dataset for common data-quality issues, including:

- Missing values
- Duplicate rows
- Completely empty columns
- Data types
- Numerical statistics

---

### 📊 Reliable Data Analysis

The application uses Pandas-based analytical functions for numerical calculations.

Supported operations include:

- Total / Sum
- Average / Mean
- Minimum
- Maximum
- Row count
- Unique count
- Grouped totals
- Grouped averages
- Top-N analysis

---

### 🗣️ Natural Language Queries

Users can ask analytical questions without knowing Python or SQL.

Examples:

```text
What is the total sales?
