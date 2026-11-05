import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pickle

print("="*60)
print("APRIORI MODEL TRAINING - IMPROVED COVERAGE")
print("="*60)

# Load data
df = pd.read_csv('../data/raw/bread basket.csv')

# Create transaction list format
transactions = df.groupby('Transaction')['Item'].apply(list).values.tolist()
print(f"\nTotal transactions: {len(transactions)}")

# Encode transactions to basket format
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
basket_df = pd.DataFrame(te_ary, columns=te.columns_)

print(f"Basket shape: {basket_df.shape}")

# Test with lower support values
test_configs = [
    {'support': 0.01, 'confidence': 0.25},
    {'support': 0.008, 'confidence': 0.20},
    {'support': 0.005, 'confidence': 0.20},
]

for config in test_configs:
    print(f"\n{'='*60}")
    print(f"Support: {config['support']}, Confidence: {config['confidence']}")
    print(f"{'='*60}")
    
    frequent_itemsets = apriori(basket_df, min_support=config['support'], use_colnames=True)
    print(f"Frequent itemsets: {len(frequent_itemsets)}")
    
    if len(frequent_itemsets) > 0:
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=config['confidence'])
        print(f"Association rules: {len(rules)}")
        
        # Count unique items in rules
        all_items = set()
        for _, rule in rules.iterrows():
            all_items.update(rule['antecedents'])
            all_items.update(rule['consequents'])
        print(f"Unique items covered: {len(all_items)} out of {basket_df.shape[1]}")

# Final model with better coverage
print(f"\n{'='*60}")
print("FINAL MODEL - OPTIMIZED FOR COVERAGE")
print(f"{'='*60}")

MIN_SUPPORT = 0.005  # 0.5% = ~47 transactions
MIN_CONFIDENCE = 0.20  # 20%

frequent_itemsets = apriori(basket_df, min_support=MIN_SUPPORT, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=MIN_CONFIDENCE)

print(f"\nFrequent itemsets: {len(frequent_itemsets)}")
print(f"Association rules: {len(rules)}")

# Analyze coverage
all_items = set()
for _, rule in rules.iterrows():
    all_items.update(rule['antecedents'])
    all_items.update(rule['consequents'])

print(f"Items with rules: {len(all_items)} out of {basket_df.shape[1]} ({len(all_items)/basket_df.shape[1]*100:.1f}%)")

# Top rules
rules_sorted = rules.sort_values('lift', ascending=False)
print(f"\nTop 20 rules by lift:")
print(rules_sorted[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(20))

# Save model
with open('../models/apriori_model.pkl', 'wb') as f:
    pickle.dump({
        'frequent_itemsets': frequent_itemsets,
        'rules': rules,
        'basket_columns': basket_df.columns.tolist(),
        'min_support': MIN_SUPPORT,
        'min_confidence': MIN_CONFIDENCE
    }, f)

print("\n[OK] Model saved: ../models/apriori_model.pkl")

# Save rules
rules_sorted.to_csv('../outputs/association_rules.csv', index=False)
print("[OK] Rules saved: ../outputs/association_rules.csv")

print("\n" + "="*60)
print("MODEL TRAINING COMPLETE")
print("="*60)
