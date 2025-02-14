import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Create dummy trade data
trade_data = pd.DataFrame({
    'Trade_ID': [1, 2, 3, 4, 5],
    'Symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
    'Quantity': [50, 100, 75, 40, 90],
    'Price': [150, 2800, 300, 750, 3500],
    'Settlement_Date': pd.date_range(start='2023-01-01', periods=5)
})

# Create dummy cash data
cash_data = pd.DataFrame({
    'Account_ID': [101, 102, 103, 104, 105],
    'Balance': [50000, 30000, 20000, 15000, 10000],
    'Margin_Requirement': [20000, 25000, 18000, 16000, 12000]
})

# Reconciliation: Check for unmatched trades
expected_trades = trade_data[['Trade_ID', 'Symbol', 'Quantity', 'Price']]
actual_trades = expected_trades.copy()  # Simulating actual trade execution data

# Introduce discrepancies for testing
actual_trades.loc[0, 'Quantity'] -= 10  # Modify one trade for reconciliation testing

trade_discrepancies = expected_trades.compare(actual_trades)
if not trade_discrepancies.empty:
    print("\n\033[1;31mTrade Discrepancies Found:\033[0m")
    print(tabulate(trade_discrepancies, headers='keys', tablefmt='fancy_grid'))
else:
    print("\n\033[1;32mNo trade discrepancies found.\033[0m")

# Cash and margin monitoring
cash_data['Shortfall'] = np.where(cash_data['Balance'] < cash_data['Margin_Requirement'],
                                  cash_data['Margin_Requirement'] - cash_data['Balance'], 0)

# Flag margin shortfalls
margin_shortfalls = cash_data[cash_data['Shortfall'] > 0]
if not margin_shortfalls.empty:
    print("\n\033[1;31mMargin Shortfalls Detected:\033[0m")
    print(tabulate(margin_shortfalls, headers='keys', tablefmt='fancy_grid'))
else:
    print("\n\033[1;32mNo margin shortfalls detected.\033[0m")

# Calculate additional statistics
average_balance = cash_data['Balance'].mean()
median_balance = cash_data['Balance'].median()
std_dev_balance = cash_data['Balance'].std()

# Visualizing cash balances
plt.figure(figsize=(8, 5))
plt.bar(cash_data['Account_ID'], cash_data['Balance'], color='blue', label='Cash Balance')
plt.axhline(y=cash_data['Margin_Requirement'].mean(), color='red', linestyle='--', label='Avg Margin Requirement')
plt.xlabel('Account ID')
plt.ylabel('Balance ($)')
plt.title('Account Cash Balances vs. Margin Requirements')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Generate summary report
report = {
    "Total Accounts": len(cash_data),
    "Total Margin Shortfall Accounts": len(margin_shortfalls),
    "Total Shortfall Amount": margin_shortfalls['Shortfall'].sum(),
    "Average Balance": round(average_balance, 2),
    "Median Balance": round(median_balance, 2),
    "Balance Standard Deviation": round(std_dev_balance, 2)
}

print("\n\033[1;34mSummary Report:\033[0m")
print(tabulate(report.items(), tablefmt='fancy_grid'))
