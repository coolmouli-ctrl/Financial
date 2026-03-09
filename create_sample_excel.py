import pandas as pd

# Create sample data
data = {
    'Principal': [10000, 20000, 15000, 25000, 30000, 12000, 18000, 22000, 16000, 28000],
    'Interest': [500, 1200, 825, 1500, 1800, 720, 990, 1320, 880, 1680]
}

df = pd.DataFrame(data)

# Calculate rates for reference
df['Interest_Rate_%'] = (df['Interest'] / df['Principal']) * 100

# Save to Excel
df.to_excel('sample_interest_data.xlsx', index=False)

print("Sample Excel file created: sample_interest_data.xlsx")
print("\nData preview:")
print(df)
print(f"\nAverage Interest Rate: {df['Interest_Rate_%'].mean():.2f}%")
