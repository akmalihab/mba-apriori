# Market Basket Analysis - Apriori Algorithm

Analisis keranjang belanja (Market Basket Analysis) menggunakan algoritma Apriori untuk menemukan asosiasi antar produk dan memberikan rekomendasi.

## 📁 Struktur Project

```
mba-apriori/
├── data/
│   ├── raw/                    # Data mentah
│   │   └── bread basket.csv
│   └── processed/              # Data hasil preprocessing
│       └── basket_format.csv
├── notebooks/
│   └── market_basket_analysis.ipynb  # Notebook lengkap EDA + Modeling
├── src/
│   ├── eda.py                  # Script exploratory data analysis
│   └── train_model.py          # Script training model
├── models/
│   └── apriori_model.pkl       # Trained model
├── outputs/
│   ├── eda_visualization.png   # Visualisasi EDA
│   └── association_rules.csv   # Association rules hasil training
├── app.py                      # Streamlit prediction app
├── requirements.txt
├── PROGRESS.md                 # Progress notes
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Streamlit App
```bash
streamlit run app.py
```

App akan buka di browser (default: http://localhost:8501)

## 📊 Dataset

**Bread Basket Dataset**
- Total records: 20,507
- Unique transactions: 9,465
- Unique items: 94
- Average items per transaction: 2.17

**Top 3 Items:**
1. Coffee (5,471)
2. Bread (3,325)
3. Tea (1,435)

## 🔬 Model Information

**Algorithm:** Apriori  
**Parameters:**
- Min Support: 0.005 (0.5%)
- Min Confidence: 0.20 (20%)

**Results:**
- Frequent itemsets: 114
- Association rules: 57
- Item coverage: 28 out of 94 items (29.8%)

**Top Association Rules (by lift):**
1. Coke → Sandwich (lift: 3.71)
2. Hot chocolate + Coffee → Cake (lift: 2.24)
3. Tea + Coffee → Cake (lift: 1.94)

## 📓 Jupyter Notebook

Untuk analisis lengkap, buka:
```bash
jupyter notebook notebooks/market_basket_analysis.ipynb
```

Notebook berisi:
- EDA lengkap dengan visualisasi
- Data preprocessing
- Apriori training dengan multiple parameter testing
- Rules analysis dan interpretasi

## 🛠️ Development

### Run EDA
```bash
cd src
python eda.py
```
Output: `outputs/eda_visualization.png`, `data/processed/basket_format.csv`

### Retrain Model
```bash
cd src
python train_model.py
```
Output: `models/apriori_model.pkl`, `outputs/association_rules.csv`

## 📱 Streamlit App Features

- **Item Selection:** Multi-select dropdown untuk pilih items di basket
- **Real-time Recommendations:** Otomatis kasih rekomendasi berdasarkan association rules
- **Metrics Display:** Confidence, Support, Lift untuk setiap rekomendasi
- **Metrics Explanation:** Penjelasan lengkap formula dan interpretasi metrics (expandable)
- **Top Rules View:** Lihat top 20 association rules dengan color gradient (default view)
- **Visual Indicators:** Highlight best recommendation, gradient by lift strength

## 📈 Metrics Explanation

### Support
Proporsi transaksi yang mengandung itemset tertentu.
```
Support(A → B) = Count(A ∩ B) / Total Transactions
```
- **Interpretasi:** Seberapa sering kombinasi muncul
- **Contoh:** Support 0.01 (1%) = muncul di ~95 dari 9,465 transaksi

### Confidence
Probabilitas item B dibeli ketika item A dibeli.
```
Confidence(A → B) = Support(A ∩ B) / Support(A) = P(B|A)
```
- **Interpretasi:** Seberapa reliable rule untuk prediksi
- **Contoh:** Confidence 70% = jika beli A, 70% kemungkinan juga beli B

### Lift
Kekuatan asosiasi - seberapa lebih sering A dan B muncul bersama vs independen.
```
Lift(A → B) = Confidence(A → B) / Support(B)
```
- **Lift > 1:** Asosiasi POSITIF (sering dibeli bersama)
- **Lift = 1:** INDEPENDEN (tidak ada hubungan)
- **Lift < 1:** Asosiasi NEGATIF (substitusi)
- **Contoh:** Lift 3.71 = customer yang beli A memiliki 3.71x lebih besar kemungkinan beli B

**Lihat `METRICS_EXPLANATION.md` untuk penjelasan lengkap dengan contoh praktis.**

---

## 🔍 Why Some Items Have No Rules?

66 items tidak memiliki association rules karena:
- Terlalu jarang dibeli (< 47 transaksi dari 9,465)
- Tidak punya pattern co-occurrence yang kuat
- Ini normal untuk market basket analysis - mayoritas item tidak punya asosiasi signifikan

## 📦 Dependencies

- pandas
- matplotlib
- seaborn
- mlxtend (Apriori implementation)
- streamlit (web app)

## 📝 Notes

Untuk parameter tuning, edit `MIN_SUPPORT` dan `MIN_CONFIDENCE` di `src/train_model.py` lalu retrain model.

Support lebih rendah = lebih banyak rules, tapi bisa jadi noise  
Confidence lebih tinggi = rules lebih reliable, tapi coverage lebih sedikit
