# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import pickle

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

model_data = load_model()
rules = model_data['rules']
all_items = model_data['basket_columns']
min_support = model_data.get('min_support', 0.005)
min_confidence = model_data.get('min_confidence', 0.20)

# Header
st.title("Market Basket Analysis")
st.markdown("### Sistem Rekomendasi Produk - Apriori Algorithm")
st.markdown("---")

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
        with st.expander("📚 Penjelasan Metrics Association Rules", expanded=False):
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
            st.info("💡 **Best Practice:** Gunakan Lift untuk prioritas recommendations (Lift > 1.5 = asosiasi kuat)")
        
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
