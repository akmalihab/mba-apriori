# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Page config
st.set_page_config(
    page_title="Market Basket Analysis",
    page_icon="🛒",
    layout="wide"
)

# Load model
@st.cache_resource
def load_model():
    with open('models/apriori_model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    return pd.read_csv('data/raw/bread basket.csv')

model_data = load_model()
rules = model_data['rules']
all_items = model_data['basket_columns']
min_support = model_data.get('min_support', 0.005)
min_confidence = model_data.get('min_confidence', 0.20)

# Header
st.title("Market Basket Analysis")
st.markdown("### Sistem Rekomendasi Produk - Apriori Algorithm")
st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["Prediksi & Rekomendasi", "Analisis Data & Model"])

# ============================================================================
# TAB 1: PREDIKSI & REKOMENDASI
# ============================================================================
with tab1:
    st.sidebar.title("Customer Basket")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Pilih item yang dibeli customer:**")

    # Multi-select untuk item
    selected_items = st.sidebar.multiselect(
        "Items in basket:",
        options=sorted(all_items),
        default=[],
        help="Pilih satu atau lebih item untuk mendapatkan rekomendasi"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Model Stats")
    st.sidebar.metric("Frequent Itemsets", len(model_data['frequent_itemsets']))
    st.sidebar.metric("Association Rules", len(rules))
    st.sidebar.metric("Items Coverage", f"{len(set([i for _, r in rules.iterrows() for i in list(r['antecedents']) + list(r['consequents'])]))} / {len(all_items)}")
    st.sidebar.markdown(f"**Min Support:** {min_support*100:.1f}%")
    st.sidebar.markdown(f"**Min Confidence:** {min_confidence*100:.0f}%")

    if selected_items:
        # Display selected items
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Items in Basket")
            st.info(" • ".join(selected_items))
        
        with col2:
            st.metric("Items Selected", len(selected_items))
        
        st.markdown("---")
        
        # Find matching rules
        recommendations = []
        
        for idx, rule in rules.iterrows():
            antecedents = set(rule['antecedents'])
            consequents = set(rule['consequents'])
            
            # Check if all antecedents are in selected items
            if antecedents.issubset(set(selected_items)):
                # Check if consequents are not already in basket
                new_items = consequents - set(selected_items)
                if new_items:
                    recommendations.append({
                        'Based on': ', '.join(sorted(antecedents)),
                        'Recommend': ', '.join(sorted(new_items)),
                        'Confidence': rule['confidence'],
                        'Support': rule['support'],
                        'Lift': rule['lift']
                    })
        
        if recommendations:
            st.markdown("### Recommended Products")
            st.markdown(f"Found **{len(recommendations)}** recommendation(s) based on association rules")
            
            rec_df = pd.DataFrame(recommendations)
            rec_df = rec_df.sort_values('Lift', ascending=False)
            
            # Top recommendation highlight
            if len(rec_df) > 0:
                top_rec = rec_df.iloc[0]
                st.success(f"**Best Recommendation:** {top_rec['Recommend']} (Lift: {top_rec['Lift']:.2f}, Confidence: {top_rec['Confidence']:.1%})")
            
            st.dataframe(
                rec_df.style.format({
                    'Confidence': '{:.1%}',
                    'Support': '{:.2%}',
                    'Lift': '{:.2f}'
                }).background_gradient(subset=['Lift'], cmap='YlGn'),
                width='stretch',
                height=400,
                hide_index=True
            )
            
            # Metrics explanation in expander
            with st.expander("Penjelasan Metrics Association Rules", expanded=False):
                st.markdown("### 1. Support")
                st.write("**Definisi:** Proporsi transaksi yang mengandung itemset tertentu")
                st.latex(r"\text{Support}(A \rightarrow B) = \frac{\text{Count}(A \cap B)}{\text{Total Transactions}}")
                st.write("**Interpretasi:**")
                st.write("- Support tinggi = kombinasi sering muncul")
                st.write("- Support 1% = muncul di ~95 dari 9,465 transaksi")
                st.write("- Support 5% = muncul di ~473 dari 9,465 transaksi")
                st.write("**Contoh:** Support(Coffee, Bread) = 9.5% → dibeli bersama di 900 transaksi")
                
                st.markdown("---")
                st.markdown("### 2. Confidence")
                st.write("**Definisi:** Probabilitas item B dibeli ketika item A dibeli")
                st.latex(r"\text{Confidence}(A \rightarrow B) = \frac{\text{Support}(A \cap B)}{\text{Support}(A)} = P(B|A)")
                st.write("**Interpretasi:**")
                st.write("- Confidence 70% = jika beli A, 70% kemungkinan juga beli B")
                st.write("- Confidence tinggi = rule reliable untuk rekomendasi")
                st.write("**Contoh:** Confidence(Toast → Coffee) = 70.4% → 70.4% customer yang beli Toast juga beli Coffee")
                
                st.markdown("---")
                st.markdown("### 3. Lift")
                st.write("**Definisi:** Kekuatan asosiasi - seberapa lebih sering A dan B muncul bersama vs independen")
                st.latex(r"\text{Lift}(A \rightarrow B) = \frac{\text{Confidence}(A \rightarrow B)}{\text{Support}(B)} = \frac{P(A,B)}{P(A) \times P(B)}")
                st.write("**Interpretasi:**")
                st.write("- **Lift > 1:** Asosiasi POSITIF - A dan B sering dibeli bersama")
                st.write("- **Lift = 1:** A dan B INDEPENDEN - tidak ada hubungan")
                st.write("- **Lift < 1:** Asosiasi NEGATIF - A dan B jarang dibeli bersama (substitusi)")
                st.write("**Contoh:** Lift(Coke → Sandwich) = 3.71 → customer yang beli Coke 3.71x lebih mungkin beli Sandwich")
                
                st.markdown("---")
                st.info("Best Practice: Gunakan Lift untuk prioritas recommendations (Lift > 1.5 = asosiasi kuat)")
            
        else:
            st.warning("Tidak ada rekomendasi untuk kombinasi item ini. Coba tambah atau ubah item lain.")
    else:
        st.info("Pilih item di sidebar untuk mendapatkan rekomendasi produk")
        
        # Model information in columns
        st.markdown("### Model Information")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Frequent Itemsets", len(model_data['frequent_itemsets']))
        with col2:
            st.metric("Association Rules", len(rules))
        with col3:
            st.metric("Unique Items", len(all_items))
        with col4:
            items_covered = len(set([i for _, r in rules.iterrows() for i in list(r['antecedents']) + list(r['consequents'])]))
            st.metric("Coverage", f"{items_covered}/{len(all_items)}", f"{items_covered/len(all_items)*100:.1f}%")
        
        st.markdown("---")
        
        # Parameters
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Model Parameters")
            st.write(f"**Min Support:** {min_support*100:.2f}% ({int(min_support*9465)} transactions)")
            st.write(f"**Min Confidence:** {min_confidence*100:.0f}%")
            st.write(f"**Algorithm:** Apriori")
        
        with col2:
            st.markdown("#### Dataset Stats")
            st.write(f"**Total Transactions:** 9,465")
            st.write(f"**Avg Items/Transaction:** 2.17")
            st.write(f"**Date Range:** Oct-Nov 2016")
        
        st.markdown("---")
        
        # Top rules
        st.markdown("### Top 20 Association Rules (by Lift)")
        
        top_rules = rules.sort_values('lift', ascending=False).head(20).copy()
        top_rules['antecedents'] = top_rules['antecedents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_rules['consequents'] = top_rules['consequents'].apply(lambda x: ', '.join(sorted(list(x))))
        
        # Add rank
        top_rules.insert(0, 'Rank', range(1, len(top_rules) + 1))
        
        st.dataframe(
            top_rules[['Rank', 'antecedents', 'consequents', 'confidence', 'support', 'lift']].style.format({
                'confidence': '{:.1%}',
                'support': '{:.2%}',
                'lift': '{:.2f}'
            }).background_gradient(subset=['lift'], cmap='RdYlGn'),
            width='stretch',
            height=600,
            hide_index=True
        )
        
        # Footer
        st.markdown("---")
        st.caption("Item dengan lift > 1 menunjukkan asosiasi positif. Semakin tinggi lift, semakin kuat hubungannya.")

# ============================================================================
# TAB 2: ANALISIS DATA & MODEL
# ============================================================================
with tab2:
    st.header("Exploratory Data Analysis & Model Performance")
    
    # Load data
    df = load_data()
    
    # Dataset Overview
    st.markdown("## 1. Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Unique Transactions", f"{df['Transaction'].nunique():,}")
    with col3:
        st.metric("Unique Items", df['Item'].nunique())
    with col4:
        items_per_trans = df.groupby('Transaction').size()
        st.metric("Avg Items/Transaction", f"{items_per_trans.mean():.2f}")
    
    st.markdown("---")
    
    # EDA Visualizations
    st.markdown("## 2. Exploratory Data Analysis")
    
    try:
        # Load EDA visualization
        eda_img = Image.open('outputs/eda_visualization.png')
        st.image(eda_img, caption="EDA Visualizations: Top Items, Distribution, Period, Weekday/Weekend")
    except:
        st.warning("EDA visualization not found. Run `python src/eda.py` to generate.")
    
    # Top Items Analysis
    with st.expander("Top 20 Items Detail", expanded=False):
        item_counts = df['Item'].value_counts().head(20)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Frequency")
            freq_df = pd.DataFrame({
                'Item': item_counts.index,
                'Count': item_counts.values
            })
            st.dataframe(
                freq_df,
                hide_index=True,
                height=400
            )
        
        with col2:
            st.markdown("### Percentage")
            item_pct = (item_counts / len(df) * 100).round(2)
            st.dataframe(
                pd.DataFrame({
                    'Item': item_pct.index,
                    'Percentage': item_pct.values.astype(str) + '%'
                }),
                hide_index=True,
                height=400
            )
    
    # Period & Weekday Analysis
    with st.expander("Time-based Analysis", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Period Distribution")
            period_dist = df['period_day'].value_counts()
            period_df = pd.DataFrame({
                'Period': period_dist.index,
                'Count': period_dist.values,
                'Percentage': (period_dist.values / len(df) * 100).round(1).astype(str) + '%'
            })
            st.dataframe(period_df, hide_index=True)
        
        with col2:
            st.markdown("### Weekday vs Weekend")
            weekday_dist = df['weekday_weekend'].value_counts()
            weekday_df = pd.DataFrame({
                'Type': weekday_dist.index,
                'Count': weekday_dist.values,
                'Percentage': (weekday_dist.values / len(df) * 100).round(1).astype(str) + '%'
            })
            st.dataframe(weekday_df, hide_index=True)
    
    st.markdown("---")
    
    # Model Performance
    st.markdown("## 3. Model Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Training Parameters")
        params_df = pd.DataFrame({
            'Parameter': ['Algorithm', 'Min Support', 'Min Confidence', 'Transactions', 'Min Transaction Count'],
            'Value': [
                'Apriori',
                f'{min_support*100:.2f}% (0.5%)',
                f'{min_confidence*100:.0f}%',
                '9,465',
                f'~{int(min_support*9465)} ({min_support*100:.1f}%)'
            ]
        })
        st.dataframe(params_df, hide_index=True)
    
    with col2:
        st.markdown("### Model Results")
        results_df = pd.DataFrame({
            'Metric': ['Frequent Itemsets', 'Association Rules', 'Items with Rules', 'Coverage', 'Date Trained'],
            'Value': [
                str(len(model_data['frequent_itemsets'])),
                str(len(rules)),
                f"{len(set([i for _, r in rules.iterrows() for i in list(r['antecedents']) + list(r['consequents'])]))}/94",
                f"{len(set([i for _, r in rules.iterrows() for i in list(r['antecedents']) + list(r['consequents'])]))/len(all_items)*100:.1f}%",
                '2026-11-05'
            ]
        })
        st.dataframe(results_df, hide_index=True)
    
    st.markdown("---")
    
    # Top Rules Analysis
    st.markdown("## 4. Top Association Rules Analysis")
    
    # Top by Lift
    with st.expander("Top 10 Rules by Lift", expanded=True):
        top_lift = rules.sort_values('lift', ascending=False).head(10).copy()
        top_lift['antecedents'] = top_lift['antecedents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_lift['consequents'] = top_lift['consequents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_lift['rank'] = range(1, len(top_lift) + 1)
        
        st.dataframe(
            top_lift[['rank', 'antecedents', 'consequents', 'support', 'confidence', 'lift']].style.format({
                'support': '{:.2%}',
                'confidence': '{:.1%}',
                'lift': '{:.2f}'
            }).background_gradient(subset=['lift'], cmap='Greens'),
            hide_index=True
        )
        
        st.info(f"**Insight:** Rule dengan lift tertinggi adalah **{top_lift.iloc[0]['antecedents']} → {top_lift.iloc[0]['consequents']}** (Lift: {top_lift.iloc[0]['lift']:.2f})")
    
    # Top by Confidence
    with st.expander("Top 10 Rules by Confidence", expanded=False):
        top_conf = rules.sort_values('confidence', ascending=False).head(10).copy()
        top_conf['antecedents'] = top_conf['antecedents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_conf['consequents'] = top_conf['consequents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_conf['rank'] = range(1, len(top_conf) + 1)
        
        st.dataframe(
            top_conf[['rank', 'antecedents', 'consequents', 'support', 'confidence', 'lift']].style.format({
                'support': '{:.2%}',
                'confidence': '{:.1%}',
                'lift': '{:.2f}'
            }).background_gradient(subset=['confidence'], cmap='Blues'),
            hide_index=True
        )
    
    # Top by Support
    with st.expander("Top 10 Rules by Support", expanded=False):
        top_supp = rules.sort_values('support', ascending=False).head(10).copy()
        top_supp['antecedents'] = top_supp['antecedents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_supp['consequents'] = top_supp['consequents'].apply(lambda x: ', '.join(sorted(list(x))))
        top_supp['rank'] = range(1, len(top_supp) + 1)
        
        st.dataframe(
            top_supp[['rank', 'antecedents', 'consequents', 'support', 'confidence', 'lift']].style.format({
                'support': '{:.2%}',
                'confidence': '{:.1%}',
                'lift': '{:.2f}'
            }).background_gradient(subset=['support'], cmap='Oranges'),
            hide_index=True
        )
    
    st.markdown("---")
    
    # Key Insights
    st.markdown("## 5. Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Strongest Associations")
        top_3_lift = rules.sort_values('lift', ascending=False).head(3)
        for i, (_, rule) in enumerate(top_3_lift.iterrows(), 1):
            ant = ', '.join(sorted(list(rule['antecedents'])))
            cons = ', '.join(sorted(list(rule['consequents'])))
            st.write(f"{i}. **{ant} → {cons}**")
            st.write(f"   - Lift: {rule['lift']:.2f} | Confidence: {rule['confidence']:.1%}")
    
    with col2:
        st.markdown("### Business Recommendations")
        st.write("**Bundle Opportunities:**")
        st.write("- Coke + Sandwich combo (Lift 3.71)")
        st.write("- Hot chocolate + Coffee → suggest Cake")
        st.write("- Tea + Coffee drinkers like Cake")
        st.write("")
        st.write("**Cross-selling Strategy:**")
        st.write("- Place Sandwich display near Coke cooler")
        st.write("- Offer Cake when selling hot beverages")
        st.write("- Create morning Coffee + Bread bundle")
    
    # Coverage Analysis
    st.markdown("### Coverage Analysis")
    items_with_rules = len(set([i for _, r in rules.iterrows() for i in list(r['antecedents']) + list(r['consequents'])]))
    items_without_rules = len(all_items) - items_with_rules
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Items with Rules", items_with_rules)
    with col2:
        st.metric("Items without Rules", items_without_rules)
    with col3:
        st.metric("Coverage Rate", f"{items_with_rules/len(all_items)*100:.1f}%")
    
    st.info("Note: 66 items tidak memiliki rules karena terlalu jarang dibeli (< 47 transaksi) atau tidak memiliki pattern co-occurrence yang kuat. Ini normal untuk market basket analysis.")
    
    st.markdown("---")
    
    # Footer
    st.caption("Untuk analisis lebih detail, lihat notebooks/market_basket_analysis.ipynb")
