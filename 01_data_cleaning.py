import pandas as pd

df = pd.read_csv('olist_customers_dataset2.csv')
print(df.info())
print(df.head())

print("*******************************************************")

#Check for duplicate rows
print("Duplicate rows count:", df.duplicated().sum())

#Standardize city names (lowercase and strip accidental spaces)
df['customer_city'] = df['customer_city'].str.strip().str.lower()
df['customer_state'] = df['customer_state'].str.strip().str.upper()

#Quick check on unique counts
print("Total Orders/Transactions:", len(df))
print("Unique Individual Customers:", df['customer_unique_id'].nunique())

print("*******************************************************")

#Top 5 States by Customer Concentration
top_states = df['customer_state'].value_counts().head(5)
top_states_pct = (top_states / len(df) * 100).round(2)

state_summary = pd.DataFrame({'Orders': top_states, 'Share (%)': top_states_pct})
print("\n--- TOP 5 STATES ---")
print(state_summary)

#Repeat Customer Analysis
orders_per_customer = df['customer_unique_id'].value_counts()
repeat_customers = (orders_per_customer > 1).sum()
repeat_rate = (repeat_customers / df['customer_unique_id'].nunique()) * 100

print("\n--- RETENTION & REPEAT BUYERS ---")
print(f"Total Unique Individuals: {df['customer_unique_id'].nunique()}")
print(f"Repeat Buyers (Ordered > 1 time): {repeat_customers}")
print(f"Repeat Purchase Rate: {repeat_rate:.2f}%")
print(f"Max Orders by a Single Customer: {orders_per_customer.max()}")

print("*******************************************************")

df.to_csv('cleaned_olist_customers.csv', index=False)
print("\nCleaned dataset exported successfully as 'cleaned_olist_customers.csv'!")
