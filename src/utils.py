import pandas as pd

def load_csv_data(folder_path="../data"):
    customers = pd.read_csv(f"{folder_path}/customers.csv")
    agreements = pd.read_csv(f"{folder_path}/agreements.csv")
    payments = pd.read_csv(f"{folder_path}/payments.csv")
    collateral = pd.read_csv(f"{folder_path}/collateral.csv")
    return {
        "customers": customers,
        "agreements": agreements,
        "payments": payments,
        "collateral": collateral
    }
