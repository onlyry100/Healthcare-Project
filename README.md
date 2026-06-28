# Healthcare Data Analytics Project

End-to-end healthcare data analytics project built using Python, SQL, and data visualization tools — covering the full pipeline from raw data to actionable insights.

## 📊 Project Overview

This project analyzes a healthcare dataset (54,860+ patient records after cleaning) to uncover insights about medical conditions, billing patterns, doctor/hospital performance, and patient length of stay.

## 🛠️ Tools & Technologies

- **Python**: Pandas, NumPy, Matplotlib, Seaborn
- **Database**: MySQL (via SQLAlchemy)
- **Data Source**: Excel/CSV (Kaggle healthcare dataset)
- **Export**: Excel (openpyxl)

## 🔄 Project Workflow

1. **Data Cleaning** (Python/Pandas)
   - Removed 534 duplicate rows
   - Removed 106 rows with invalid (negative) billing amounts
   - Standardized column names and text formatting
   - Converted date columns to proper datetime format

2. **Database Design & Load** (MySQL)
   - Normalized data into 2 tables: `patients` and `admission`
   - Loaded cleaned data into MySQL using SQLAlchemy

3. **SQL Analysis**
   - Wrote 6 queries covering JOINs, GROUP BY, subqueries, and date functions
   - Identified top doctors/hospitals by revenue and average billing

4. **Python Analysis**
   - Pulled data back into Python using `pd.read_sql()`
   - Used NumPy to calculate length-of-stay statistics (mean, median, std dev)

5. **Data Visualization** (Matplotlib/Seaborn)
   - 6 charts covering medical conditions, doctor/hospital billing, and distributions

6. **Excel Export**
   - Exported a multi-sheet summary report (`healthcare_analysis_summary.xlsx`)

## 🔍 Key Insights

- Most common medical condition: **arthritis** — though all conditions were nearly equal in count (~9,000-9,200), suggesting a synthetically balanced dataset
- Highest revenue doctor (by total billing): **Michael Smith**; most expensive doctor (by average billing): **Kathleen Griffin** — showing total revenue and per-patient cost are different insights
- Highest revenue hospital: **Johnson PLC**
- Average length of stay: **15.5 days** (median: 15.0 days)
- No correlation found between patient age and billing amount, and both billing amount and length of stay were uniformly distributed — indicating this is a synthetically generated dataset rather than real-world skewed healthcare data

## 📁 Files in this Repository

- `main.py` — full Python pipeline (cleaning, MySQL load, analysis, visualization, Excel export)
- `healthcare_dataset.csv` — raw dataset
- `SQL File For Healthcare Project.sql` — SQL queries used for analysis
- `healthcare_analysis_summary.xlsx` — final exported summary report

## 📈 Sample Visualizations

(Charts available in the project — medical condition distribution, top doctors/hospitals by billing, billing amount distribution, length of stay distribution, age vs billing scatter plot)
