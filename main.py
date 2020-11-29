# West Virginia Population data from:
# https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html
# Opioid Prescriptions by County data from: https://www.cdc.gov/drugoverdose/maps/rxcounty2017.html
# Covid Case by County data from: https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv
# Covid Deaths by County data from:
# https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-in-the-United-St/kn79-hsxy
# Reported Crime by County data from:
# https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/tables/table-8/table-8-state-cuts/west-virginia.xls


import json
import pandas as pd
import plotly.express as px
from urllib.request import urlopen

# Get county geo data for map creation
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Load population dataset and convert to dataframe
popFile = 'wv-census.xlsx'
popData = pd.read_excel(popFile)
popDF = pd.DataFrame(popData, columns=['FIPS', 'Geographic Area', 'Census'])

# Load opioid prescription dataset and convert to dataframe
opioidFile = 'opioid-county.xlsx'
opioidData = pd.read_excel(opioidFile)
opioidDF = pd.DataFrame(opioidData, columns=['FIPS', 'County', 'Opioid Prescribing Rate per 100'])

# Load crime dataset and convert to dataframe
crimeFile = 'west-virginia-crime.xlsx'
crimeData = pd.read_excel(crimeFile)
crimeDF = pd.DataFrame(crimeData, columns=['FIPS', 'County', 'Violent crime'])

# Load covid deaths by county dataset and convert to dataframe
covidFile = 'covid-county.csv'
covidData = pd.read_csv(covidFile, usecols=
['County name', 'FIPS County Code', 'Deaths involving COVID-19'])
covidDF = pd.DataFrame(covidData)

# Load covid infections by county dataset and convert to dataframe
infectFile = 'covid-infect.csv'
infectData = pd.read_csv(infectFile, usecols=
['county', 'fips', 'cases'])
infectDF = pd.DataFrame(infectData)

# Data Comparisons
print("Top 3 Most Populous Counties: ")
print(popDF.nlargest(3, 'Census'))

print("\nTop 3 Counties by Opioid Abuse Rates per 100 People: ")
print(opioidDF.nlargest(3, 'Opioid Prescribing Rate per 100'))

print("\nAverage Opioid Abuse Rate: " + str(opioidDF["Opioid Prescribing Rate per 100"].mean()))

print("\nTop 3 Counties by Reports of Violent Crimes: ")
print(crimeDF.nlargest(3, 'Violent crime'))

print("\nAverage Violent Crime Reports: " + str(crimeDF["Violent crime"].mean()))

print("\nTop 3 Counties by Covid Deaths: ")
print(covidDF.nlargest(3, 'Deaths involving COVID-19'))

print("\nAverage COVID Deaths: " + str(covidDF["Deaths involving COVID-19"].mean()))

print("\nTop 3 Counties by Covid Infections: ")
print(infectDF.nlargest(3, 'cases'))

print("\nAverage COVID Infections: " + str(infectDF["cases"].mean()))

# Assemble heatmap for opioid cases by county
opioidFig = px.choropleth(opioidDF,
                          geojson=counties,
                          locations='FIPS',
                          color='Opioid Prescribing Rate per 100',
                          color_continuous_scale="OrRd",
                          range_color=(0, 200),
                          scope="usa",
                          hover_name='County',
                          hover_data={'FIPS': False,
                                      'Opioid Prescribing Rate per 100': True},
                          labels={'Opioid Prescribing Rate per 100': 'Opioid Prescribing Rate (per 100) '}
                          )
opioidFig.update_geos(fitbounds="locations", visible=False)  # Zoom map to WV
opioidFig.update_layout(margin={"r": 100, "t": 100, "l": 100, "b": 100},
                        title_text='2017 West Virginia County Opioid Prescribing Rates per 100 People')

opioidFig.show()

# Assemble heatmap for covid cases by county
infectFig = px.choropleth(infectDF,
                          geojson=counties,
                          locations='fips',
                          color='cases',
                          color_continuous_scale="OrRd",
                          range_color=(0, 5000),
                          scope="usa",
                          hover_name='county',
                          hover_data={'fips': False,
                                      'cases': True},
                          labels={'cases': 'COVID-19 Cases '}
                          )

infectFig.update_geos(fitbounds="locations", visible=False)  # Zoom map to WV
infectFig.update_layout(margin={"r": 100, "t": 100, "l": 100, "b": 100},
                        title_text='West Virginia COVID-19 Cases by County as of 11/07/2020')

infectFig.show()

# Assemble heatmap for covid deaths by county
covidFig = px.choropleth(covidDF,
                         geojson=counties,
                         locations='FIPS County Code',
                         color='Deaths involving COVID-19',
                         color_continuous_scale="OrRd",
                         range_color=(0, 150),
                         scope="usa",
                         hover_name='County name',
                         hover_data={'FIPS County Code': False,
                                     'Deaths involving COVID-19': True},
                         labels={'Deaths involving COVID-19': 'COVID-19 Deaths '}
                         )

covidFig.update_geos(fitbounds="locations", visible=True)  # Zoom map to WV
covidFig.update_layout(margin={"r": 100, "t": 100, "l": 100, "b": 100},
                       title_text='West Virginia COVID-19 Death Counts by County as of 11/04/2020 - '
                                  '(Counties not shown have <10 deaths)')

covidFig.show()

# Assemble heatmap for crime
crimeFig = px.choropleth(crimeDF,
                         geojson=counties,
                         locations='FIPS',
                         color='Violent crime',
                         color_continuous_scale="OrRd",
                         range_color=(0, 150),
                         scope="usa",
                         hover_name='County',
                         hover_data={'FIPS': False,
                                     'Violent crime': True},
                         labels={'Violent crime': 'Violent Crime Reports'}
                         )

crimeFig.update_geos(fitbounds="locations", visible=True)  # Zoom map to WV
crimeFig.update_layout(margin={"r": 100, "t": 100, "l": 100, "b": 100},
                       title_text='Violent Crime Offenses Known to Law Enforcement, 2016')

crimeFig.show()

# Assemble heatmap for population
popFig = px.choropleth(popDF,
                       geojson=counties,
                       locations='FIPS',
                       color='Census',
                       color_continuous_scale="Blues",
                       range_color=(0, 200000),
                       scope="usa",
                       hover_name="Geographic Area",
                       hover_data={'FIPS': False,
                                   'Census': True},
                       labels={'Census': 'Population (2010) '}
                       )

popFig.update_geos(fitbounds="locations", visible=False)  # Zoom map to WV
popFig.update_layout(margin={"r": 100, "t": 100, "l": 100, "b": 100},
                     title_text='2010 West Virginia Population Totals')

popFig.show()
