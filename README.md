# 🤖 AI Data Analyst Agent

An AI-powered data analysis web application that allows users to upload datasets and ask analytical questions in natural language.

The application automatically profiles the uploaded dataset, checks data quality, performs reliable numerical analysis using Pandas, generates visualizations, and provides answers to analytical questions without requiring the user to write Python or SQL queries.

---

## 🚀 Live Demo

🌐 **Live Application:**  
https://ai-data-analyst-agent-mocha.vercel.app/

---

## 📌 Project Overview

Data analysis often requires users to understand programming languages, SQL, or spreadsheet formulas before they can extract useful insights from their data.

The **AI Data Analyst Agent** simplifies this process by allowing users to interact with their datasets using natural language.

Users can:

- Upload CSV or Excel datasets
- Automatically inspect the dataset
- View data quality information
- Ask questions in natural language
- Calculate totals, averages, minimums, and maximums
- Compare values across categories
- Find top-performing products or categories
- Calculate unique values and row counts
- Generate charts automatically
- Receive AI-assisted analytical responses

The goal is to provide a simple interface where users can interact with data as if they were asking questions to a data analyst.

---

# ✨ Features

## 📂 1. Dataset Upload

The application supports common structured data formats:

- CSV
- Excel (`.xlsx`)
- Excel (`.xls`)

After uploading a dataset, the application automatically loads it into Pandas for analysis.

---

## 🔍 2. Automatic Data Profiling

The system automatically analyzes the uploaded dataset and identifies:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Unique values
- Duplicate rows
- Empty columns
- Numerical statistics

This provides an initial understanding of the dataset before analysis begins.

---

## 🧹 3. Data Quality Analysis

The application checks the uploaded dataset for common quality issues such as:

- Missing values
- Duplicate rows
- Completely empty columns
- Dataset structure
- Numerical column statistics

This helps identify potential data problems before drawing conclusions.

---

## 📊 4. Reliable Data Analysis

The application uses Pandas-based analysis functions for numerical calculations.

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

Example questions:

```text
What is the total sales?

What is the average sales?

What is the maximum sales?

How many rows are there?

How many unique products are there?

Show total sales by product.

Show average sales by product.

Show the top 2 products by sales.
