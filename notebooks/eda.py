from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent   # resume-analyzer folder
df = pd.read_csv(ROOT/'data/DataEngineer.csv')

print(ROOT)
# 1. Kitni rows, kitne columns
print("Shape:", df.shape)
# 2. Column names
print("\nColumns:", list(df.columns))
# 3. Pehli 5 rows
print("\nHead:")
print(df.head())
# 4. Data types
print("\nDtypes:")
print(df.dtypes)
# 5. Missing values
print("\nNull counts:")
print(df.isnull().sum())