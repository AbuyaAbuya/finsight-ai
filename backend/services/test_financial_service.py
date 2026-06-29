from backend.services.financial_service import FinancialService
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

print("=" * 80)
print("FinSight Financial Service Test")
print("=" * 80)

service = FinancialService()

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

print("\nKPIs")
print("-" * 80)

print(service.kpis())

# ---------------------------------------------------------
# Available Years
# ---------------------------------------------------------

print("\nYears")
print("-" * 80)

print(service.years())

# ---------------------------------------------------------
# Available Countries
# ---------------------------------------------------------

print("\nCountries")
print("-" * 80)

print(service.countries())

# ---------------------------------------------------------
# Income Statement
# ---------------------------------------------------------

print("\nIncome Statement")
print("-" * 80)

income = service.income_statement()

print(income.head(20))

# ---------------------------------------------------------
# Balance Sheet
# ---------------------------------------------------------

print("\nBalance Sheet")
print("-" * 80)

balance = service.balance_sheet()

print(balance.head(20))

# ---------------------------------------------------------
# Trial Balance
# ---------------------------------------------------------

print("\nTrial Balance")
print("-" * 80)

trial = service.trial_balance()

print(trial.head(20))

service.close()

print("\nFinancial Service test completed successfully.")