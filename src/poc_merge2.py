import pandas as pd

elecYrly = pd.read_csv("../data/raw/electricityYearly.csv")
bigDf = pd.read_csv("../primeContracts.csv")
seds = pd.read_csv("../data/raw/seds.csv")
sedCodes = pd.read_csv("../data/raw/sedCodes.csv")

# Filtering the big USASpending df
bigDf = bigDf[(bigDf["awarding_agency_name"].str.contains("Department of Energy", case=False, na=False)) |(bigDf["funding_agency_name"].str.contains("Department of Energy", case=False, na=False))]

filteredBigDf = bigDf[["action_date_fiscal_year","federal_action_obligation","primary_place_of_performance_state_code","primary_place_of_performance_state_name"]]

# Check if the dataframes were filtered successfully
# print("Success! Filtered size:", filteredBigDf.shape)
# print(f"{filteredBigDf.shape}, {filteredBigDf.head()}")

filteredBigDf = filteredBigDf.rename(columns = {"action_date_fiscal_year": "Year", "federal_action_obligation": "doe_contract_dollars", "primary_place_of_performance_state_code": "StateCode", "primary_place_of_performance_state_name": "state"})

filteredBigDf = filteredBigDf.groupby(["StateCode", "state", "Year"], as_index=False)["doe_contract_dollars"].sum()
# This function groups the usa data by the state code and year, adding the dollars as a running total.



# Filtering the electricityYearly df
elecYrly = elecYrly[(elecYrly["Category"] == "Electricity generation") & (elecYrly["Variable"] == "Renewables") & (elecYrly["Unit"] == "GWh")]



# Filtering the seds df
seds = seds[seds["MSN"] == "CDTPR"]



# Rename the common columns to merge in all three dataframes to be the same
elecYrly = elecYrly.rename(columns = {"State code": "StateCode"})



# Check the column names in each df
# print(filteredBigDf.columns)
# print(elecYrly.columns)
# print(seds.columns)



# Make sure all state codes don't have extra spaces and year entries are integers
filteredBigDf['Year'] = filteredBigDf['Year'].astype(int)
elecYrly['Year'] = elecYrly['Year'].astype(int)
seds['Year'] = seds['Year'].astype(int)
filteredBigDf['StateCode'] = filteredBigDf['StateCode'].str.strip()
elecYrly['StateCode'] = elecYrly['StateCode'].str.strip()
seds['StateCode'] = seds['StateCode'].str.strip()


# Merge all dfs
merged1 = pd.merge(filteredBigDf, elecYrly, on=["StateCode", "Year"])
finalMerged = pd.merge(merged1, seds, on=["StateCode", "Year"])

print(finalMerged)
