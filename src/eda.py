import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load data
df = pd.read_csv('../data/raw/bread basket.csv')

print("="*60)
print("STATISTIK DESKRIPTIF - MARKET BASKET ANALYSIS")
print("="*60)

# Basic info
print(f"\nTotal records: {len(df)}")
print(f"Total unique transactions: {df['Transaction'].nunique()}")
print(f"Total unique items: {df['Item'].nunique()}")

# Items per transaction
items_per_trans = df.groupby('Transaction').size()
print(f"\nItems per transaction:")
print(f"  Mean: {items_per_trans.mean():.2f}")
print(f"  Median: {items_per_trans.median():.0f}")
print(f"  Min: {items_per_trans.min()}")
print(f"  Max: {items_per_trans.max()}")

# Top items
item_counts = df['Item'].value_counts()
print(f"\nTop 20 items:")
print(item_counts.head(20))

# Period distribution
print(f"\nPeriod distribution:")
print(df['period_day'].value_counts())

print(f"\nWeekday/Weekend distribution:")
print(df['weekday_weekend'].value_counts())

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Top 20 items
item_counts.head(20).plot(kind='barh', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Top 20 Most Frequent Items', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Frequency')
axes[0, 0].invert_yaxis()

# Items per transaction distribution
axes[0, 1].hist(items_per_trans, bins=30, color='coral', edgecolor='black')
axes[0, 1].set_title('Distribution of Items per Transaction', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Number of Items')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].axvline(items_per_trans.mean(), color='red', linestyle='--', label=f'Mean: {items_per_trans.mean():.2f}')
axes[0, 1].legend()

# Period distribution
period_counts = df['period_day'].value_counts()
axes[1, 0].bar(period_counts.index, period_counts.values, color='lightgreen', edgecolor='black')
axes[1, 0].set_title('Transactions by Period of Day', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Period')
axes[1, 0].set_ylabel('Count')
axes[1, 0].tick_params(axis='x', rotation=45)

# Weekday vs Weekend
weekday_counts = df['weekday_weekend'].value_counts()
axes[1, 1].pie(weekday_counts.values, labels=weekday_counts.index, autopct='%1.1f%%', 
               colors=['lightblue', 'lightyellow'], startangle=90)
axes[1, 1].set_title('Weekday vs Weekend Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('../outputs/eda_visualization.png', dpi=300, bbox_inches='tight')
print("\n[OK] Visualization saved: ../outputs/eda_visualization.png")

# Additional analysis: Co-occurrence matrix for top items
print("\n" + "="*60)
print("PREPARING DATA FOR APRIORI")
print("="*60)

# Create basket format
basket = df.groupby(['Transaction', 'Item'])['Item'].count().unstack().fillna(0)
basket = basket.map(lambda x: 1 if x > 0 else 0)
print(f"\nBasket matrix shape: {basket.shape}")
print(f"Transactions: {basket.shape[0]}, Unique items: {basket.shape[1]}")

# Save basket format
basket.to_csv('../data/processed/basket_format.csv')
print("[OK] Basket format saved: ../data/processed/basket_format.csv")

print("\n" + "="*60)
print("EDA COMPLETE")
print("="*60)
