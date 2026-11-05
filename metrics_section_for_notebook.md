# Penjelasan Metrics - Insert ke Notebook

Tambahkan markdown cell ini setelah section 4.1 dan sebelum 4.2:

```markdown
### 4.1.1 📊 Penjelasan Metrics Association Rules

Sebelum melanjutkan ke model final, penting untuk memahami 3 metrics utama yang digunakan dalam Apriori:

#### 1. Support (Dukungan)

**Definisi:** Proporsi transaksi yang mengandung itemset tertentu terhadap total transaksi.

**Formula:**
$$\text{Support}(A) = \frac{\text{Count}(A)}{\text{Total Transactions}}$$

$$\text{Support}(A \rightarrow B) = \frac{\text{Count}(A \cap B)}{\text{Total Transactions}}$$

**Interpretasi:**
- Mengukur seberapa populer/sering suatu kombinasi item
- Support tinggi = itemset sering muncul bersama
- Support rendah = itemset jarang (mungkin noise)

**Contoh dengan data kita:**
- Support(Coffee, Bread) = 0.095 = 9.5%
  - Coffee dan Bread dibeli bersama di **852 dari 9,465 transaksi**
- Support 0.005 (0.5%) = minimal **47 transaksi** dari 9,465

**Fungsi:** Filter itemset yang terlalu jarang untuk mengurangi noise.

---

#### 2. Confidence (Kepercayaan)

**Definisi:** Probabilitas bersyarat - seberapa sering item B dibeli ketika item A dibeli.

**Formula:**
$$\text{Confidence}(A \rightarrow B) = \frac{\text{Support}(A \cap B)}{\text{Support}(A)} = P(B|A)$$

**Interpretasi:**
- Mengukur reliability dari rule untuk prediksi
- Confidence 0.70 = ketika A dibeli, 70% kemungkinan B juga dibeli
- Range: 0 sampai 1 (0% sampai 100%)

**Contoh dengan data kita:**
- Confidence(Toast → Coffee) = 0.704 = 70.4%
  - Dari **semua transaksi yang beli Toast**, 70.4% juga beli Coffee
  - Artinya: jika customer beli Toast, kita 70% yakin mereka akan beli Coffee

**Fungsi:** Mengukur kekuatan rule untuk membuat rekomendasi.

---

#### 3. Lift (Pengangkat)

**Definisi:** Rasio antara confidence rule dengan expected confidence jika A dan B independen.

**Formula:**
$$\text{Lift}(A \rightarrow B) = \frac{\text{Confidence}(A \rightarrow B)}{\text{Support}(B)} = \frac{P(A,B)}{P(A) \times P(B)}$$

**Interpretasi:**
- **Lift > 1:** Asosiasi POSITIF
  - A dan B sering dibeli bersama (lebih dari yang diharapkan secara random)
  - Semakin tinggi lift, semakin kuat hubungannya
- **Lift = 1:** A dan B INDEPENDEN
  - Tidak ada hubungan khusus antara A dan B
- **Lift < 1:** Asosiasi NEGATIF
  - A dan B jarang dibeli bersama (produk substitusi)

**Contoh dengan data kita:**

**a) Asosiasi Kuat (Lift Tinggi):**
- Lift(Coke → Sandwich) = 3.71
  - Customer yang beli Coke memiliki kemungkinan **3.71 kali lebih besar** untuk beli Sandwich
  - Ini asosiasi sangat kuat! → **Strategi:** Buat combo meal Coke + Sandwich

**b) Asosiasi Lemah (Lift ≈ 1):**
- Lift(Bread → Pastry) = 1.03
  - Hampir tidak ada hubungan khusus (beli independen)

**c) Asosiasi Negatif (Lift < 1):**
- Lift(Tea → Coffee) = 0.73
  - Customer yang beli Tea cenderung **TIDAK** beli Coffee
  - Tea dan Coffee adalah **produk substitusi**, bukan komplemen!

**Fungsi:** Menemukan insights tersembunyi yang benar-benar bermakna (bukan kebetulan).

---

#### Perbandingan Metrics

| Metric | Fungsi | Range | Interpretasi Terbaik |
|--------|--------|-------|---------------------|
| **Support** | Popularitas | 0 - 1 | Tinggi = sering terjadi |
| **Confidence** | Reliability | 0 - 1 | Tinggi = prediksi akurat |
| **Lift** | Kekuatan asosiasi | 0 - ∞ | > 1 = asosiasi positif |

---

#### Contoh Praktis: Analisis 3 Rules

##### Rule 1: Toast → Coffee
- **Support:** 0.0356 (3.56%) → 336 transaksi
- **Confidence:** 0.704 (70.4%) → 70% customer yang beli Toast juga beli Coffee
- **Lift:** 1.47 → Customer yang beli Toast 1.47x lebih mungkin beli Coffee

**Insight:** Rule reliable dengan asosiasi positif  
**Actionable:** Taruh display Coffee dekat Toast section di toko

##### Rule 2: Coke → Sandwich
- **Support:** 0.0085 (0.85%) → 80 transaksi (jarang)
- **Confidence:** 0.459 (45.9%) → hampir 50% customer yang beli Coke juga beli Sandwich
- **Lift:** 3.71 → Customer yang beli Coke 3.71x lebih mungkin beli Sandwich!

**Insight:** Support rendah tapi lift sangat tinggi - hidden pattern!  
**Actionable:** Buat combo promo "Coke + Sandwich" untuk boost sales

##### Rule 3: Tea → Coffee
- **Support:** 0.0499 (4.99%) → 472 transaksi
- **Confidence:** 0.350 (35%) → hanya 35% customer yang beli Tea juga beli Coffee
- **Lift:** 0.73 → Customer yang beli Tea cenderung TIDAK beli Coffee

**Insight:** Tea dan Coffee adalah substitusi (kompetitor)  
**Actionable:** Jangan buat bundling Tea + Coffee (tidak masuk akal)

---

#### Kapan Menggunakan Metric Mana?

1. **Support** → Filter awal
   - Buang kombinasi yang terlalu jarang (noise)
   - Support terlalu rendah = sample size kecil, kurang reliable
   - Support terlalu tinggi = hanya tangkap item yang sudah pasti populer

2. **Confidence** → Untuk prediksi dan rekomendasi
   - Confidence tinggi = aman untuk recommend ke customer
   - Tapi hati-hati: confidence bisa misleading tanpa cek lift!

3. **Lift** → Untuk menemukan insights tersembunyi
   - Lift tinggi = asosiasi kuat yang mungkin tidak obvious
   - Gunakan untuk: bundling strategy, cross-selling, store layout optimization

**Best Practice untuk Market Basket Analysis:**
- Min support: 0.5% - 1% (filter noise tapi jangan terlalu ketat)
- Min confidence: 20% - 30% (reliable recommendation)
- **Sort by Lift** untuk prioritas: rules dengan lift tertinggi adalah yang paling actionable!

---

#### ⚠️ Common Pitfalls

**Pitfall 1: High Confidence, Low Lift**
- Confidence(Bread → Coffee) = 0.60 (60%)
- Lift(Bread → Coffee) = 1.02 (hampir 1)
- **Masalah:** Coffee memang populer, bukan karena hubungan khusus dengan Bread
- **Solusi:** Always check lift!

**Pitfall 2: Ignoring Support**
- Lift(A → B) = 5.0 (sangat tinggi!)
- Support = 0.0001 (hanya 1 transaksi)
- **Masalah:** Sample size terlalu kecil, bisa kebetulan
- **Solusi:** Set min support yang wajar

**Pitfall 3: Hanya Lihat Confidence**
- Confidence tinggi tidak selalu berarti good recommendation
- Coffee muncul di banyak rules dengan confidence tinggi karena memang populer
- **Solusi:** Prioritas rules dengan lift > 1.5 untuk insights yang actionable

---

Setelah memahami metrics di atas, sekarang kita siap untuk train model final dan menginterpretasikan hasilnya dengan benar!
```
