# Penjelasan Metrics untuk Association Rules

## 1. Support
**Definisi:** Proporsi transaksi yang mengandung itemset tertentu terhadap total transaksi.

**Formula:**
```
Support(A) = Count(transaksi mengandung A) / Total transaksi
Support(A → B) = Count(transaksi mengandung A dan B) / Total transaksi
```

**Interpretasi:**
- Support tinggi = itemset sering muncul bersama
- Support 0.01 (1%) = muncul di 1% dari semua transaksi (94-95 transaksi dari 9465)
- Support 0.05 (5%) = muncul di 5% dari semua transaksi (473 transaksi)

**Contoh:**
- Support(Coffee, Bread) = 0.095 = 9.5%
  Artinya: Coffee dan Bread dibeli bersama di 9.5% dari seluruh transaksi (sekitar 852 transaksi)

**Fungsi:** Filter itemset yang jarang (noise reduction)

---

## 2. Confidence
**Definisi:** Probabilitas bersyarat - seberapa sering item B dibeli ketika item A dibeli.

**Formula:**
```
Confidence(A → B) = Support(A ∪ B) / Support(A)
                  = P(B | A)
```

**Interpretasi:**
- Confidence 0.70 (70%) = ketika A dibeli, 70% kemungkinan B juga dibeli
- Confidence tinggi = rule lebih reliable untuk rekomendasi
- Range: 0 sampai 1 (0% sampai 100%)

**Contoh:**
- Confidence(Toast → Coffee) = 0.704 = 70.4%
  Artinya: Dari semua transaksi yang membeli Toast, 70.4% juga membeli Coffee
  Jika customer beli Toast, ada peluang 70.4% mereka akan beli Coffee

**Fungsi:** Mengukur kekuatan rule untuk prediksi

---

## 3. Lift
**Definisi:** Rasio antara confidence rule dengan expected confidence jika A dan B independen.

**Formula:**
```
Lift(A → B) = Confidence(A → B) / Support(B)
            = Support(A ∪ B) / (Support(A) × Support(B))
            = P(A,B) / (P(A) × P(B))
```

**Interpretasi:**
- **Lift > 1:** Asosiasi POSITIF - A dan B sering dibeli bersama (lebih sering dari yang diharapkan secara random)
- **Lift = 1:** A dan B INDEPENDEN - tidak ada hubungan khusus
- **Lift < 1:** Asosiasi NEGATIF - A dan B jarang dibeli bersama (lebih jarang dari yang diharapkan)

**Contoh:**
- Lift(Coke → Sandwich) = 3.71
  Artinya: Customer yang beli Coke memiliki kemungkinan 3.71 kali lebih besar untuk beli Sandwich dibanding customer random
  Ini asosiasi sangat kuat!

- Lift(Tea → Coffee) = 0.73
  Artinya: Customer yang beli Tea sebenarnya cenderung TIDAK beli Coffee (substitusi)

**Fungsi:** Mengidentifikasi rules yang benar-benar bermakna vs yang kebetulan

---

## Perbandingan Metrics

| Metric | Fungsi | Range | Interpretasi Terbaik |
|--------|--------|-------|---------------------|
| Support | Seberapa populer kombinasi | 0 - 1 | Tinggi = sering terjadi |
| Confidence | Seberapa reliable rule | 0 - 1 | Tinggi = prediksi akurat |
| Lift | Seberapa kuat asosiasi | 0 - ∞ | > 1 = asosiasi positif |

---

## Contoh Praktis dengan Data Bread Basket

### Rule 1: Toast → Coffee
- Support: 0.0356 (3.56%)
  → Toast dan Coffee dibeli bersama di 336 transaksi
- Confidence: 0.704 (70.4%)
  → 70.4% customer yang beli Toast juga beli Coffee
- Lift: 1.47
  → Customer yang beli Toast 1.47x lebih mungkin beli Coffee

**Rekomendasi:** Taruh Coffee display dekat Toast section!

### Rule 2: Coke → Sandwich
- Support: 0.0085 (0.85%)
  → Coke dan Sandwich dibeli bersama di 80 transaksi (jarang)
- Confidence: 0.459 (45.9%)
  → 45.9% customer yang beli Coke juga beli Sandwich (sedang)
- Lift: 3.71
  → Customer yang beli Coke 3.71x lebih mungkin beli Sandwich (sangat kuat!)

**Rekomendasi:** Buat combo meal Coke + Sandwich!

### Rule 3: Tea → Coffee
- Support: 0.0499 (4.99%)
  → Tea dan Coffee dibeli bersama di 472 transaksi
- Confidence: 0.350 (35%)
  → Hanya 35% customer yang beli Tea juga beli Coffee
- Lift: 0.73
  → Customer yang beli Tea sebenarnya cenderung TIDAK beli Coffee

**Interpretasi:** Tea dan Coffee adalah produk substitusi, bukan komplemen!

---

## Kapan Menggunakan Metric Mana?

1. **Support** → Filter awal, buang kombinasi yang terlalu jarang
   - Support terlalu rendah = rule tidak reliable (sample size kecil)
   - Support terlalu tinggi = hanya tangkap item populer

2. **Confidence** → Untuk prediksi dan rekomendasi
   - Confidence tinggi = aman untuk recommend
   - Tapi hati-hati dengan "misleading" rules (cek lift!)

3. **Lift** → Untuk menemukan insights tersembunyi
   - Lift tinggi = asosiasi kuat yang tidak obvious
   - Gunakan untuk strategi bundling, cross-selling, store layout

**Best Practice:** Gunakan kombinasi ketiganya!
- Min support: 0.5% (filter noise)
- Min confidence: 20% (reliable recommendation)
- Sort by Lift: prioritas rules dengan asosiasi terkuat
