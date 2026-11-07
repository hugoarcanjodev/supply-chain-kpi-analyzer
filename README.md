<div align="center">

# 📦 Supply Chain Data Analytics
### Auditing Logistics Metrics & Process Deviations

*Exploratory data analysis with SQL and Python to uncover inventory inefficiencies, supplier risk and costly logistics failures.*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-MVP-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 📑 Table of Contents
- [Overview](#-overview)
- [Business Problem](#-business-problem)
- [Objectives](#-objectives)
- [Tech Stack](#️-tech-stack)
- [Repository Structure](#-repository-structure)
- [Data Model](#️-data-model)
- [Methodology & Analyses](#-methodology--analyses)
- [Key Insights & Recommendations](#-key-insights--recommendations)
- [Getting Started](#-getting-started)
- [Roadmap](#️-roadmap)
- [Author](#-author)

---

## 🔎 Overview

This project is an end-to-end **MVP** that audits supply chain and logistics operations through **Exploratory Data Analysis (EDA)**. It combines **SQL** for data extraction and aggregation with **Python** for statistical analysis and visualization, simulating a real manufacturing scenario where data supports operational decisions.

It connects **Production Engineering concepts** (ABC Analysis, Lead Time variability, Pareto Principle, Quality Control) with modern **Data Analytics tooling**.

> **Note:** The dataset is **synthetic**, generated to replicate realistic supply chain behavior. All company names, figures and findings are illustrative and do not represent real organizations.

---

## 🏭 Business Problem

**Alpha Industry**, a fictional manufacturer, faced three recurring problems over the last year:

| Problem | Impact |
|---|---|
| **High operational costs** | Excess safety stock with no strategic classification criteria |
| **Production bottlenecks** | Stockouts and delays caused by unstable supplier lead times |
| **Financial losses** | Transit damage, invoice errors and short shipments causing direct losses |

---

## 🎯 Objectives

1. Audit historical purchasing and logistics data to locate the root causes of the problems above.
2. Quantify **supplier reliability** through lead time averages and variability.
3. Classify inventory by value using **ABC Analysis** to prioritize management focus.
4. Rank failure types by **financial impact** using **Pareto Analysis**.
5. Propose **3 actionable operational strategies** backed by data.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **Languages** | SQL, Python 3.10+ |
| **Database** | SQLite |
| **Libraries** | `pandas`, `numpy`, `matplotlib`, `seaborn`, `sqlite3` |
| **Environment** | Jupyter Notebook |
| **Logistics Concepts** | ABC Curve, Lead Time Variability (standard deviation), Pareto Principle, Safety Stock |

---

## 📁 Repository Structure

```text
supply-chain-analytics/
├── data/
│   └── supply_chain_data.db        # SQLite database with historical records
├── queries/
│   ├── inventory_audit.sql         # Inventory and stock valuation queries
│   └── lead_time_analysis.sql      # Delivery auditing with window functions
├── notebooks/
│   └── supply_chain_eda.ipynb      # Main analysis: Python EDA and charts
├── requirements.txt                # Python dependencies
├── LICENSE
├── .gitignore
└── README.md
```

---

## 🗄️ Data Model

The SQLite database simulates the core tables of a purchasing and inventory process:

| Table | Description |
|---|---|
| `tb_pedidos_compra` | Purchase orders: supplier, order date, promised and actual delivery dates |
| `tb_fornecedores` | Supplier registry |
| `tb_estoque` | SKUs with current stock, safety stock level and unit cost |
| `tb_desvios_logisticos` | Logistics failure events: type, date and financial loss |

> Adjust table and column names to match your final schema.

---

## 📊 Methodology & Analyses

### 1. Supplier Lead Time Audit (SQL)
Compares **actual** versus **promised** delivery times per supplier, exposing the gap between contract and reality.

```sql
SELECT
    id_fornecedor,
    COUNT(id_pedido) AS total_pedidos,
    AVG(julianday(data_entrega_real) - julianday(data_pedido))      AS lead_time_medio_real,
    AVG(julianday(data_entrega_prometida) - julianday(data_pedido)) AS lead_time_acordado
FROM tb_pedidos_compra
WHERE data_entrega_real IS NOT NULL
GROUP BY id_fornecedor
ORDER BY lead_time_medio_real DESC;
```

The standard deviation of lead time is then calculated in Python, since SQLite has no native `STDDEV`.

### 2. ABC Inventory Classification (Python)
SKUs are ranked by capital tied up in stock and grouped by cumulative value:

| Class | Share of SKUs | Share of inventory value | Management approach |
|:---:|:---:|:---:|---|
| **A** | ~20% | ~80% | Tight control, frequent review |
| **B** | ~30% | ~15% | Moderate control |
| **C** | ~50% | ~5% | Simplified control |

### 3. Failure Analysis (Pareto)
Logistics deviations are compared by **frequency** and by **financial impact** to show that the most frequent failure is not always the most expensive.

---

## 📈 Key Insights & Recommendations

> Results below refer to the synthetic dataset and demonstrate the analytical approach.

### 🔹 Insight 1: Supplier lead time variability
**XYZ Logistics** averages a 12-day lead time with a standard deviation of ±5 days. This variability is linked to **40% of raw material stockouts** on Production Line A.
- ✅ **Recommendation:** Renegotiate SLAs or qualify backup suppliers closer to the plant.

### 🔹 Insight 2: Capital tied up in overstock
**15 Class C SKUs** are **200% above** their safety stock limit, freezing working capital with little operational benefit.
- ✅ **Recommendation:** Run a Just-In-Time (JIT) review of these items to release capital.

### 🔹 Insight 3: Hidden cost of transit damage
*Damage during transit* is only **15% of failure events** but causes **65% of total financial losses**, driven by high-value products.
- ✅ **Recommendation:** Tighten packaging standards and audit the carrier's cargo security protocols.

---

## 🚀 Getting Started

**Prerequisites:** Python 3.10+ and Jupyter.

```bash
# 1. Clone the repository
git clone https://github.com/hugoarcanjodev/supply-chain-analytics.git
cd supply-chain-analytics

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the notebook
jupyter notebook notebooks/supply_chain_eda.ipynb
```

Suggested `requirements.txt`:

```text
pandas
numpy
matplotlib
seaborn
jupyter
```

---

## 🗺️ Roadmap

- [x] SQL audit of supplier lead times
- [x] ABC inventory classification
- [x] Pareto analysis of logistics failures
- [ ] Interactive dashboard (Streamlit or Power BI)
- [ ] Safety stock and reorder point calculation
- [ ] Supplier scorecard with a composite performance index
- [ ] Demand forecasting module

---

## 👤 Author

**Hugo Arcanjo**
Production Engineering Student | Logistics & Supply Chain

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hugo-arcanjo)
[![GitHub](https://img.shields.io/badge/GitHub-hugoarcanjodev-181717?logo=github&logoColor=white)](https://github.com/hugoarcanjodev)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?logo=gmail&logoColor=white)](mailto:hugoarcanjodev@gmail.com)

---

<div align="center">
<sub>If this project was useful, consider leaving a ⭐</sub>
</div>