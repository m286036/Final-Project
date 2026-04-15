import pandas as pd

df = pd.read_excel('Codes_and_Descriptions.xlsx')
df.to_csv("sedCodes.csv", index=False)
