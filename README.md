# Life Sciences Research Intelligence Dashboard

## Overview

This project is an interactive Streamlit dashboard developed for the Drug Discovery domain. It helps users view, search, filter, analyse, and interpret compound research data.

## Dataset

The dataset contains:
* 120 records
* 12 fields

Main fields include compound ID, compound name, target protein, research stage, researcher, toxicity, efficacy, processing days, status, priority, country, and study year.

## Main Features

* View complete dataset
* Search by compound ID, compound name, target protein, and researcher
* Filter by stage, status, priority, country, target, researcher, and year
* Display business metrics
* Generate scientific insights
* Show charts and trends
* Identify alerts
* Generate recommendations
* Export filtered data and reports

## Custom Feature

The custom feature is an Alert and Recommendation Engine.

It identifies:
* High-toxicity compounds
* Low-efficacy compounds
* Delayed compounds
* High-priority risks
* On Hold or Discontinued compounds

## Technology Stack

* Python
* Streamlit
* pandas
* CSV

CSV was selected because it is lightweight and portable. pandas was used for analysis, and Streamlit was used to build the interactive dashboard.

## Project Files

Task 5/
├── research_intelligence_dashboard.py
├── requirements.txt
├── README.md
├── technology_choice.docx
├── Dataset/
│   └── research_dashboard_data.csv
├── Screenshots/
└── Deployment Screenshots/
```

## How to Run

Install dependencies:
python -m pip install -r requirements.txt


Run the application:
python -m streamlit run research_intelligence_dashboard.py


## Deployment
The dashboard was deployed using Streamlit Community Cloud through a GitHub repository.

Public URL:

## Author

Ramana Maharshi Mellacheruvu
