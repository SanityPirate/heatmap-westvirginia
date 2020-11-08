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
