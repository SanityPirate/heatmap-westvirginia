from urllib.request import urlopen
import pandas as pd
import json
import plotly.express as px

# Get county geo data for map creation
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Load in the dataset and convert to dataframe
dataFile = 'wv-census.xlsx'
data = pd.read_excel(dataFile)
df = pd.DataFrame(data, columns=['FIPS', 'Geographic Area', 'Census'])

# Assemble heatmap
fig = px.choropleth(df,
                    geojson=counties,
                    locations='FIPS',
                    color='Census',
                    color_continuous_scale="Blues",
                    range_color=(0, 200000),
                    scope="usa",
                    hover_name="Geographic Area",
                    hover_data={'FIPS':False,
                                'Census':True},
                    labels={'Census': 'Population (2010) '}
                    )

fig.update_geos(fitbounds="locations", visible=False)  # Zoom map to WV
fig.update_layout(margin={"r": 100, "t": 100, "l": 100, "b": 100},
                  title_text='2010 West Virginia Population Totals')
fig.show()
