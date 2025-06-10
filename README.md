# 📊 Jira Tickets Analysis - Support & Development

This data project analyzes several years of Jira support (`CNSD`) and development (`CNXT`) tickets from a real software team. The goal is to uncover actionable insights that help the organization identify strengths, bottlenecks, and opportunities for process improvement.

> 🛡️ All data has been anonymized to remove any personally identifiable information (PII) and sensitive content.

---


📘 [Support tickets exploratory analysis Notebook](notebooks/01%20EDA%20Support.ipynb)


## Project structure

- `data/raw/`: `.pkl` files and raw data exported directly from Jira  
- `data/processed/`: Cleaned and merged datasets  
- `scripts/`: Python scripts used for data extraction and processing
- `notebooks/`: Jupyter notebooks containing the analysis
- `outputs/`: Generated charts and output files


## 📌 Key Questions Explored

- What is the volume and trend of tickets over time?
- Are there patterns in ticket creation by day of week or hour?
- How are tickets distributed by work category?
- How long do issues remain in each status?


This is an ongoing project, more analysis to come