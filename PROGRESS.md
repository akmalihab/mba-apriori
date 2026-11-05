# Market Basket Analysis - Apriori Algorithm

## Project Structure

```
mba-apriori/
├── data/
│   ├── raw/                    # Data mentah
│   │   └── bread basket.csv
│   └── processed/              # Data hasil preprocessing
│       └── basket_format.csv
├── notebooks/
│   └── market_basket_analysis.ipynb  # Complete EDA + Modeling
├── src/
│   ├── eda.py                  # Exploratory data analysis script
│   └── train_model.py          # Model training script
├── models/
│   └── apriori_model.pkl       # Trained Apriori model
├── outputs/
│   ├── eda_visualization.png   # EDA visualizations
│   └── association_rules.csv   # All association rules
├── app.py                      # Streamlit prediction interface
├── requirements.txt            # Python dependencies
├── PROGRESS.md                 # This file
└── README.md                   # Complete documentation
```

## Dataset Summary
- **File**: `bread basket.csv`
- **Total records**: 20,507
- **Unique transactions**: 9,465
- **Unique items**: 94
- **Avg items per transaction**: 2.17

### Exploratory Data Analysis (EDA)
✓ File: `eda.py`

**Key Findings**:
- Top 3 items: Coffee (5471), Bread (3325), Tea (1435)
- Most transactions: afternoon (56.4%), morning (41.0%)
- Weekday vs Weekend: 62.4% weekday, 37.6% weekend
- Item distribution: highly skewed, few popular items dominate

**Output**:
- `eda_visualization.png` - 4 visualisasi (top items, distribution, period, weekday/weekend)
- `basket_format.csv` - matrix format untuk apriori

## Model Performance (Final)

**Parameters (Optimized for Coverage)**:
- Min support: 0.005 (0.5%)
- Min confidence: 0.20 (20%)

**Results**:
- Frequent itemsets: 114
- Association rules: 57
- Item coverage: 28/94 items (29.8%)

**Top Rules (by lift)**:
1. Coke → Sandwich (confidence: 45.9%, lift: 3.71)
2. Hot chocolate + Coffee → Cake (lift: 2.24)
3. Tea + Coffee → Cake (lift: 1.94)

**Output**:
- `models/apriori_model.pkl` - trained model
- `outputs/association_rules.csv` - all rules

### Streamlit Prediction App
✓ File: `app.py`

**Features**:
- Multi-select item input dengan sidebar stats
- Real-time product recommendations sorted by lift
- Best recommendation highlight
- Metrics explanation dengan formula LaTeX (expandable)
- Display confidence, support, lift dengan color gradient
- Show top 20 rules by default dengan ranking
- Model parameters dan dataset stats display

## Usage

### Run Streamlit App
```bash
streamlit run app.py
```

### Run EDA
```bash
cd src
python eda.py
```

### Retrain Model
```bash
cd src
python train_model.py
```

### Open Notebook
```bash
jupyter notebook notebooks/market_basket_analysis.ipynb
```

### Dependencies
- pandas
- matplotlib
- seaborn
- mlxtend
- streamlit

## Files Created
1. **notebooks/market_basket_analysis.ipynb** - Complete notebook (EDA + modeling)
2. **src/eda.py** - EDA script
3. **src/train_model.py** - Model training script (improved)
4. **app.py** - Streamlit prediction interface dengan metrics explanation
5. **models/apriori_model.pkl** - Trained model
6. **outputs/eda_visualization.png** - EDA visualizations
7. **outputs/association_rules.csv** - All association rules
8. **data/processed/basket_format.csv** - Preprocessed data
9. **requirements.txt** - Dependencies
10. **README.md** - Complete documentation
11. **METRICS_EXPLANATION.md** - Detailed metrics explanation dengan contoh
12. **metrics_section_for_notebook.md** - Metrics section untuk insert ke notebook
13. **PROGRESS.md** - This file

## Notes

**Why 66 items have no rules?**
- Too rare (< 47 transactions out of 9,465)
- No strong co-occurrence patterns
- Normal for market basket analysis

**Parameter Tradeoff:**
- Lower support → more rules, more noise
- Higher confidence → more reliable, less coverage

Current params optimized for balance between coverage and reliability.
