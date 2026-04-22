import pandas as pd

df=pd.read_csv("merged.csv", sep="\t")
early_df = df[df['Year']==2017]
Wyoming_df=df[df["state"]=="Wyoming"]
California_df=df[df["state"]=="California"][df['Year'] != 2015][df['Year'] != 2016]
late_df=df[df['Year']==2023]
##print(early_df)

import plotly.express as px
from plotly.colors import sequential as colors #got this from SD211 covid lab
fig = px.choropleth(
    data_frame=early_df,
    color_continuous_scale=colors.Reds,
    locations='StateCode',      
    locationmode="USA-states",   
    color='doe_funding_dollars',     
    scope="usa",        
    range_color=[0,300000000],
    title="DOE spending per state (2017)"                  
)  ##I got this command from Gemini Gem. In SD211 we had a lab where we made a heat map of Covid Cases and Hudson gave me the idea to do this. My biggest problem was mapping the state names to the abbreviation, which I did with a large dictionary.

##fig.show()


line_fig = px.line(df, 
              x="Year", 
              y="Data", 
              color="state",
              title="Change in Renewable Energy Generation by State (2015-2023)")

#line_fig.show()

line_fig2 = px.line(df, 
              x="Year", 
              y="doe_funding_dollars", 
              color="state",
              title="Change in Government DOE Funding to States (2015-2023)")

#line_fig2.show()



Cal_fig = px.line(California_df, 
              x= "Year", 
              y="doe_funding_dollars", 
              color="state",
              title="Change in DOE funding to California (2017-2023)")

Cal_fig.show()


Flo_df=df[df["state"]=="Florida"]
Flo_fig = px.line(Flo_df, 
              x= "Year", 
              y="doe_funding_dollars", 
              color="state",
              title="Change in DOE funding to Florida (2017-2023)")

Flo_fig2 = px.line(Flo_df, 
              x= "Year", 
              y="Data", 
              color="state",
              title="Change in Renewable Energy Generation in Florida (2015-2023)")

#Flo_fig2.show()

Col_df=df[df["state"]=="Colorado"][df['Year'] != 2016]
Col_fig = px.line(Col_df, 
              x= "Year", 
              y="doe_funding_dollars", 
              color="state",
              title="Change in DOE funding to Colorado (2017-2023)")

Col_fig2 = px.line(Col_df, 
              x= "Year", 
              y="Data", 
              color="state",
              title="Change in Renewable Energy Generation in Colorado (2015-2023)")

##Col_fig.show()

Ken_df=df[df["state"]=="Kentucky"][df['Year'] != 2023]
Ken_fig = px.line(Ken_df, 
              x= "Year", 
              y="doe_funding_dollars", 
              color="state",
              title="Change in DOE funding to Kentucky (2017-2023)")

Ken_fig2 = px.line(Ken_df, 
              x= "Year", 
              y="Data", 
              color="state",
              title="Change in Renewable Energy Generation in Kentucky (2015-2023)")

#Ken_fig2.show()