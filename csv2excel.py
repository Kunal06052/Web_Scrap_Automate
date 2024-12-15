import pandas as pd

df = pd.read_csv('dhaturi_extraction.csv')
df.to_excel('dhaturi_extraction.xlsx', index=False)
print(df.info())