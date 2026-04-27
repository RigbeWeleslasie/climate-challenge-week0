# Climate Challenge – Week 0  
## African Climate Trend Analysis (10 Academy KAIM9)

## Project Overview
Exploratory analysis of historical climate data from Ethiopia, Kenya, Sudan, Tanzania, and Nigeria (2015-2026) to support Ethiopia's COP32
position paper as host of the United Nations Climate Change Conference in Addis Ababa in 2027.

---

## Folder Structure
```
climate-challenge-week0/
├── .github/
│   └── workflows/
│       └── unittests.yml
├── notebooks/
│   ├── __init__.py
│   ├── README.md
│   ├── ethiopia_eda.ipynb
│   ├── kenya_eda.ipynb
│   ├── sudan_eda.ipynb
│   ├── tanzania_eda.ipynb
│   ├── nigeria_eda.ipynb
│   └── compare_countries.ipynb
├── scripts/
│   ├── __init__.py
│   ├── README.md
│   └── run_eda.py
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── eda_utils.py
│   └── comparison.py
├── tests/
│   ├── __init__.py
│   └── test_data_loader.py
├── .vscode/
│   └── settings.json
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How to Reproduce the Environment

### 1. Clone the Repository
```bash
git clone git@github.com:RigbeWeleslasie/climate-challenge-week0.git
cd climate-challenge-week0
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4. Run the EDA pipeline
```bash
python scripts/run_eda.py
```

### 5. Launch Jupyter notebooks
```bash
jupyter notebook
```

## Data
Data sourced from NASA POWER database covering 5 African countries.
- Ethiopia, Kenya, Sudan, Tanzania, Nigeria
- Period: January 2015 - March 2026
- 4,108 daily observations per country
- Data files excluded from version control via .gitignore

## Project Structure
- `src/data_loader.py` - Data loading and cleaning functions
- `src/eda_utils.py` - EDA visualization functions
- `src/comparison.py` - Cross-country comparison functions
- `scripts/run_eda.py` - Main pipeline script
- `tests/test_data_loader.py` - Unit tests
- `notebooks/` - Jupyter notebooks for each country EDA

## CI/CD
GitHub Actions workflow runs on every push to main:
- Sets up Python 3.10
- Installs all dependencies
- Runs unit tests

## Key Findings
- Sudan has the highest mean temperature (28.8°C) with 250+ extreme heat days/year
- Nigeria shows the most variable precipitation patterns
- Ethiopia and Kenya show clear bimodal rainfall patterns
- Kruskal-Wallis test confirms significant climate differences (p < 0.0001)
- Sudan ranked #1 for climate vulnerability and priority finance needs

## Team
- Facilitators: Kerod, Mahbubah, Feven
- Program: 10 Academy AI Mastery (KAIM9)
- GitHub: https://github.com/RigbeWeleslasie/climate-challenge-week0


