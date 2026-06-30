# FinSight AI
### Enterprise Financial Planning & Analysis (FP&A) Platform
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Vite](https://img.shields.io/badge/Vite-Build-purple)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-orange)

---

## Overview

FinSight AI is an enterprise-grade Financial Planning & Analysis (FP&A) platform designed to transform traditional financial reporting into an intelligent decision-support system.

The platform integrates accounting data, financial statements, budgeting, forecasting, variance analysis, KPI monitoring, and AI-generated insights into one modern analytics environment.

Rather than simply displaying reports, FinSight AI helps finance professionals understand:

- Business performance
- Profitability drivers
- Cash flow trends
- Financial risks
- Strategic opportunities
- Executive decision support

The long-term vision is to build an AI-powered finance platform comparable to modern FP&A solutions used by global organizations.

---

# Live Demo

### Frontend

https://finsight-ai-ebon-tau.vercel.app

### Backend API

https://finsight-ai-xtss.onrender.com

---

# GitHub Repository

https://github.com/AbuyaAbuya/finsight-ai

---

# Current Features

## Executive Dashboard

Provides a comprehensive executive summary including:

- Revenue
- Expenses
- Net Profit
- Cash Position
- KPI Cards
- Monthly Revenue Trends
- Expense Trends
- Profitability Analysis
- Cash Position
- AI Insights
- Financial Recommendations

---

## Financial Reporting

Current reports include:

- Trial Balance
- Income Statement
- Balance Sheet
- Cash Flow Statement
- Statement of Changes in Equity

---

## Planning & Analysis

Current modules include:

- Budgeting
- Forecasting
- Variance Analysis
- Scenario Planning

---

## Financial Analytics

Includes:

- Financial Ratios
- Trend Analysis
- Revenue Analysis
- Expense Analysis
- Profitability Analysis

---

## AI Assistant

Current implementation includes:

- Executive Insights
- Automated Recommendations
- Financial Commentary

Future releases will include:

- Natural Language Queries
- Chat with Financial Statements
- AI Financial Advisor
- Predictive Analytics
- Root Cause Analysis
- Automated Board Reports

---

# Technology Stack

## Backend

- Python
- FastAPI
- DuckDB
- Pandas
- OpenPyXL

---

## Frontend

- React
- Vite
- React Router
- Axios
- TailwindCSS
- Recharts
- Lucide Icons

---

## Deployment

Frontend

- Vercel

Backend

- Render

---

# Architecture

```
Excel / ERP / Accounting Data
            │
            ▼
     Data Processing
        (Pandas)
            │
            ▼
        DuckDB Warehouse
            │
            ▼
      FastAPI REST API
            │
            ▼
      React Frontend
            │
            ▼
 Executive Financial Dashboards
            │
            ▼
      AI Recommendation Engine
```

---

# Current Dashboard Modules

✔ Executive Dashboard

✔ Trial Balance

✔ Income Statement

✔ Balance Sheet

✔ Cash Flow Statement

✔ Statement of Equity

✔ Budget

✔ Forecast

✔ Variance Analysis

✔ Scenario Planning

✔ Financial Ratios

✔ Reports

✔ AI Copilot

---

# Roadmap

## Phase 1 (Completed)

- Financial database
- Executive Dashboard
- Financial Statements
- KPI Reporting
- Revenue Analytics
- Expense Analytics
- Cash Analysis
- Interactive Dashboard
- REST API
- Cloud Deployment

---

## Phase 2

- Multi-company support
- User authentication
- Role-based security
- Audit logs
- Report scheduling
- PDF Export
- Excel Export
- PowerPoint Export

---

## Phase 3

Planning & Analysis

- Driver-based budgeting
- Rolling Forecasts
- Workforce Planning
- Sales Forecasting
- Capital Planning
- Scenario Modelling
- What-if Analysis

---

## Phase 4

Artificial Intelligence

- AI Financial Copilot
- Chat with Financial Statements
- Natural Language Queries
- Predictive Forecasting
- Cash Flow Prediction
- Risk Detection
- Automated Variance Explanations
- Executive Board Report Generation

---

## Phase 5

Enterprise Platform

- ERP Integration
- SAP
- Oracle
- Microsoft Dynamics
- QuickBooks
- Xero
- Odoo
- API Integrations

---

# Future Vision

The vision is to evolve FinSight AI into an intelligent Enterprise Performance Management (EPM) platform capable of supporting:

- CFOs
- FP&A Analysts
- Controllers
- Finance Managers
- CEOs
- Executive Leadership Teams

with AI-driven financial intelligence, planning, forecasting, and strategic decision support.

---

# Screenshots

(Add screenshots here as the application evolves.)

---

# Installation

Clone the repository

```bash
git clone https://github.com/AbuyaAbuya/finsight-ai.git
```

Move into the project

```bash
cd finsight-ai
```

Install frontend dependencies

```bash
cd frontend
npm install
```

Install backend dependencies

```bash
cd ../
pip install -r requirements.txt
```

Run backend

```bash
uvicorn backend.main:app --reload
```

Run frontend

```bash
cd frontend
npm run dev
```

---

# Project Structure

```
finsight-ai/

backend/
    analytics/
    api/
    services/
    main.py

frontend/
    components/
    pages/
    contexts/
    layouts/

database/
    finsight.duckdb

data/
    general_ledger.xlsx

requirements.txt
```

---

# Author

**Joseph Abuya**

Finance | Data Science | FP&A | Business Intelligence | Artificial Intelligence

GitHub

https://github.com/AbuyaAbuya

LinkedIn

(Add your LinkedIn URL)

---

# License

MIT License

---

## Acknowledgements

This project is being developed as a personal initiative to demonstrate how Artificial Intelligence, Financial Planning & Analysis (FP&A), Business Intelligence, and Modern Data Engineering can be integrated into a unified enterprise finance platform.

It serves as both a learning platform and a foundation toward building next-generation AI-powered financial decision support systems.
