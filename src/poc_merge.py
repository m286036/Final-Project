import pandas as pd


energy=pd.read_csv("electricityYearly.csv")
usa=pd.read_csv("primeContracts.csv")
seds = pd.read_csv("raw/seds.csv", low_memory=False)





usa = usa[(usa["awarding_agency_name"].str.contains("Department of Energy", case=False, na=False)) |(usa["funding_agency_name"].str.contains("Department of Energy", case=False, na=False))]
##gemini gave us these functions to filter down the rows and columns in the usa dataset that we need.
usa = usa[["action_date_fiscal_year","federal_action_obligation","primary_place_of_performance_state_code","primary_place_of_performance_state_name"]]

##gemini explained dropna function to drop the rows/columns that have Na in them
usa = usa.dropna(subset=["state_code", "state", "year", "doe_contract_dollars"])
usa["year"] = usa["year"].astype(int)


grouped_usa_df = usa.groupby(["state_code", "state", "year"], as_index=False)["doe_contract_dollars"].sum()
##This function groups the usa data by the state code and year, adding the dollars as a running total.



renew = electric[(electric["Category"] == "Electricity generation") &(electric["Variable"] == "Renewables") &(electric["Unit"] == "GWh")]