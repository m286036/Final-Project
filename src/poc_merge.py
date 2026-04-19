import pandas as pd



# Combine all of the FY csv into one
files = ["../data/raw/FY2014.csv", "../data/raw/FY2015.csv", "../data/raw/FY2016.csv", "../data/raw/FY2017.csv", "../data/raw/FY2018.csv", "../data/raw/FY2019.csv", "../data/raw/FY2020.csv", "../data/raw/FY2021.csv", "../data/raw/FY2022.csv", "../data/raw/FY2023.csv"]
bigDf= pd.concat([pd.read_csv(f) for f in files], ignore_index=True) # Used Gemini Gem for help using pd.concat for files in the same folder
# Read in the rest of the files
elecYrly = pd.read_csv("../data/raw/electricityYearly.csv")
seds = pd.read_csv("../data/raw/seds.csv")
sedCodes = pd.read_csv("../data/raw/sedCodes.csv")



# Filtering the big USASpending df
filteredBigDf = bigDf[["action_date_fiscal_year","federal_action_obligation","primary_place_of_performance_state_name"]]
filteredBigDf = filteredBigDf.rename(columns = {"action_date_fiscal_year": "Year", "federal_action_obligation": "doe_funding_dollars", "primary_place_of_performance_state_name": "state"})



# Filtering the electricityYearly df
elecYrly = elecYrly[(elecYrly["Category"] == "Electricity generation") & (elecYrly["Variable"] == "Renewables") & (elecYrly["Unit"] == "GWh")]



# Filtering the seds df
seds = seds[seds["MSN"] == "CDTPR"]



# The fiscal year DOE csvs don't have a column for state abbreviations, so we need to create a one-time map (Gemini helped with this):
stateMap = {"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
    "Colorado":"CO","Connecticut":"CT","Delaware":"DE","District of Columbia":"DC",
    "Florida":"FL","Georgia":"GA","Hawaii":"HI","Idaho":"ID","Illinois":"IL",
    "Indiana":"IN","Iowa":"IA","Kansas":"KS","Kentucky":"KY","Louisiana":"LA",
    "Maine":"ME","Maryland":"MD","Massachusetts":"MA","Michigan":"MI","Minnesota":"MN",
    "Mississippi":"MS","Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV",
    "New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM","New York":"NY",
    "North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR",
    "Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD",
    "Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA",
    "Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY"}
filteredBigDf["state"] = filteredBigDf["state"].str.strip().str.title() # Gemin helped with cleaning parameters
filteredBigDf["StateCode"] = filteredBigDf["state"].map(stateMap) # Gemini helped refresh how to use the map function for dataframes
filteredBigDf = filteredBigDf.dropna(subset=["StateCode"]) # Drop all state names that don't match


# This function groups the usa data by the state code and year, adding the dollars as a running total.
filteredBigDf = filteredBigDf.groupby(["StateCode", "state", "Year"], as_index=False)["doe_funding_dollars"].sum()



# Rename the common columns to merge in all three dataframes to be the same
elecYrly = elecYrly.rename(columns = {"State code": "StateCode"})



# Make sure all state codes don't have extra spaces and year entries are integers; used Gemini Gem to learn how to use .astype
filteredBigDf['Year'] = filteredBigDf['Year'].astype(int)
elecYrly['Year'] = elecYrly['Year'].astype(int)
seds['Year'] = seds['Year'].astype(int)
filteredBigDf['StateCode'] = filteredBigDf['StateCode'].str.strip()
elecYrly['StateCode'] = elecYrly['StateCode'].str.strip()
seds['StateCode'] = seds['StateCode'].str.strip()



# Restrict dataframes to common year ranges
filteredBigDf = filteredBigDf[filteredBigDf["Year"] <= 2023]
elecYrly = elecYrly[elecYrly["Year"] <= 2023]
seds = seds[seds["Year"] <= 2023]



# Merge all dfs
merged1 = pd.merge(filteredBigDf, elecYrly, on=["StateCode", "Year"], how="left")
finalMerged = pd.merge(merged1, seds, on=["StateCode", "Year"], how="left")



print(finalMerged)