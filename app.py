# Data Visualization Final Project
#
# Jeff Shen & Anay Gangal
# July 28, 2023

# Import statements
from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template



app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')

server = app.server

df = pd.read_csv("pollution_new.csv")
df.drop(df.loc[df['State Code'] == 11].index, inplace=True)
df.drop(df.loc[df['State Code'] == 80].index, inplace=True)

usabbv = {
    'Alabama':'AL',
    'Alaska':'AK',
    'Arizona':'AZ',
    'Arkansas':'AR',
    'California':'CA',
    'Colorado':'CO',
    'Connecticut':'CT',
    'Delaware':'DE',
    'Florida':'FL',
    'Georgia':'GA',
    'Hawaii':'HI',
    'Idaho':'ID',
    'Illinois':'IL',
    'Indiana':'IN',
    'Iowa':'IA',
    'Kansas':'KS',
    'Kentucky':'KY',
    'Louisiana':'LA',
    'Maine':'ME',
    'Maryland':'MD',
    'Massachusetts':'MA',
    'Michigan':'MI',
    'Minnesota':'MN',
    'Missouri':'MO',
    'Nevada':'NV',
    'New Hampshire':'NH',
    'New Jersey':'NJ',
    'New Mexico':'NM',
    'New York':'NY',
    'North Carolina':'NC',
    'North Dakota':'ND',
    'Ohio':'OH',
    'Oklahoma':'OK',
    'Oregon':'OR',
    'Pennsylvania':'PA',
    'Rhode Island':'RI',
    'South Carolina':'SC',
    'South Dakota':'SD',
    'Tennessee':'TN',
    'Texas':'TX',
    'Utah':'UT',
    'Virginia':'VA',
    'Washington':'WA',
    'Wisconsin':'WI',
    'Wyoming':'WY'
}

df['State'].replace(usabbv, inplace=True)

navbar = dbc.NavbarSimple(
    children = [
        dbc.DropdownMenu(
            children = [
                dbc.DropdownMenuItem('Choropleth', href='#Choropleth_title', external_link = True),
                dbc.DropdownMenuItem('Scatterplot', href='#scatter', external_link = True),
                dbc.DropdownMenuItem('Parallel Coordinates', href='#parallel', external_link = True),
                dbc.DropdownMenuItem('Jointplot (Histogram)', href='#jointhist', external_link = True),
                dbc.DropdownMenuItem('Jointplot (KDE)', href='#jointkde', external_link = True),
                dbc.DropdownMenuItem('References & Dataset', href='#references', external_link = True),
            ],
            in_navbar = True,
            label = 'Visualization Selections',
            size='md',
        ),
    ],
    brand = 'Data Visualization Final Project',
#    sticky = 'top',

)

app.layout = html.Div([
    navbar,
    html.Div([dcc.Markdown('''
            #### Summer 2023
            #### Jeff Shen and Anay Gangal
        '''),
        ], style={'marginTop': 15, 'marginLeft': 150, 'marginRight': 150},
    ),
    html.Hr(),
    html.Div([dcc.Markdown('''
            ### Visualizing Historical United States Pollution Data 2000-2016
            This project leverages historical United States pollution data from 2000 to 2016 to create interesting and unique visualizations. Sourced from the Environmental Protection Agency and compiled on Kaggle by a third party, this dataset is utilized to extract meaningful insights into how prevalent four major pollutants (Nitrogen Dioxide, Sulphur Dioxide, Carbon Monoxide, and Ozone) are in the atmosphere. Existing visualizations were explored and critiqued while fresh, interesting visuals were created. Interactive choropleth maps juxtaposed with jointplots and scatterplots serve to support the claim that air quality has improved in the United States between 2000 and 2016.  
            
            This topic of this project really captured our interest as it is extremely relevant in the current media. Smoke from wildfires raging in Quebec, Canada has traveled south and shrouded parts of the United States, severely affecting air quality. Most notably, New York’s air quality index (AQI) was declared the worst in the world. According to CNN, New York had a concentration of PM2.5 (a dangerous pollutant) of more than 10 times the recommended guideline provided by the World Health Organization.  Poor air quality can have a serious effect on public health. The National Institute of Environmental Health Sciences states that air pollution is a threat to respiratory health and is responsible for over 6.5 million deaths a year globally. With this being a very relevant and serious issue, this project explores pollution data limited to the United States to identify trends and extract other meaningful insights. The focus is on the following four major pollutants that affect air quality: Nitrogen Dioxide (NO2), Sulphur Dioxide (SO2), Carbon Monoxide (CO), and Ozone (O3).
        '''),
        ], style={'marginTop': 50 , 'marginBottom': 50, 'marginLeft': 150, 'marginRight': 150},
    ),
    html.Hr(),
    html.Div([
        html.Div([
            dcc.Markdown('''### Choropleth Plots''', id = 'Choropleth_title'),
            dcc.Slider(2000, 2016, step = None, marks = {2000:'2000',2001:'2001',2002:'2002',2003:'2003',
                                                         2004:'2004',2005:'2005',2006:'2006',2007:'2007',
                                                         2008:'2008',2009:'2009',2010:'2010',2011:'2011',
                                                         2012:'2012',2013:'2013',2014:'2014',2015:'2015',
                                                         2016:'2016'}, value = 2000, id='date_slider'),
            dcc.RadioItems(options = [{'label' : 'NO2 (ppb)', 'value' : 'NO2 Mean'},
                                      {'label' : 'O3 (ppm)', 'value' : 'O3 Mean'},
                                      {'label' : 'SO2 (ppb)', 'value' : 'SO2 Mean'},
                                      {'label' : 'CO (ppm)', 'value' : 'CO Mean'}
                                      ],
                           value = 'NO2 Mean', inline = False, id = 'pollutant_radio'),
            dcc.Graph(figure = {}, id = 'choropleth'),

            html.Div([dcc.Markdown('''
                    #### Choropleth plot of pollutant concentrations (ppm / ppb)
                    This choropleth plot can be used to visualize how pollution has changed over time as well as what states are key pollutant contributors. Pollutant concentration is analyzed over time using an interactive year slider and radio buttons for pollutant selection.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150, 'marginBottom': 50, 'textAlign': 'left'},
            ),
            html.Hr(),
            
            dcc.Slider(2000, 2016, step = None, marks = {2000:'2000',2001:'2001',2002:'2002',2003:'2003',
                                                         2004:'2004',2005:'2005',2006:'2006',2007:'2007',
                                                         2008:'2008',2009:'2009',2010:'2010',2011:'2011',
                                                         2012:'2012',2013:'2013',2014:'2014',2015:'2015',
                                                         2016:'2016'}, value = 2000, id='date_slider_AQI'),
            dcc.RadioItems(options = [{'label' : 'NO2', 'value' : 'NO2 AQI'},
                                      {'label' : 'O3', 'value' : 'O3 AQI'},
                                      {'label' : 'SO2', 'value' : 'SO2 AQI'},
                                      {'label' : 'CO', 'value' : 'CO AQI'}
                                      ],
                           value = 'NO2 AQI', inline = False, id = 'pollutant_radio_AQI'),
            dcc.Graph(figure = {}, id = 'choroplethAQI'),
            html.Div([dcc.Markdown('''
                    #### Choropleth plot of pollutant air quality index (AQI)
                    This choropleth plot can be used to visualize how pollution has changed over time as well as what states are key pollutant contributors. Pollutant air quality index is analyzed over time using an interactive year slider and radio buttons for pollutant selection.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150, 'textAlign': 'left'},
            ),  
        ], style={'marginTop': 50, 'marginBottom': 50, 'textAlign': 'center'}),
        html.Hr(),
        html.Div([
            dcc.Markdown('''### Scatterplots''', id = 'scatter'),
            dcc.RadioItems(options = [{'label' : 'NO2', 'value' : 'NO2 AQI'},
                                      {'label' : 'O3', 'value' : 'O3 AQI'},
                                      {'label' : 'SO2', 'value' : 'SO2 AQI'},
                                      {'label' : 'CO', 'value' : 'CO AQI'}
                                      ],
                           value = 'NO2 AQI', inline = False, id = 'scatter_choice'),                        
            dcc.Graph(figure = {}, id = 'scatter1'),
            html.Div([dcc.Markdown('''
                    #### Scatterplot of mean AQI for a given day in the United States
                    This scatterplot shows daily fluctuations in air quality index averaged across the entire United States for any given day. These values were all compiled and plotted into this scatterplot for 2000 to 2016 with a Y axis of air quality index for the specific pollutant selected from the radio buttons.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150, 'textAlign': 'left'},
            ),
        ], style={'marginTop': 50, 'marginBottom': 50, 'textAlign': 'center'}),
        html.Hr(),
        html.Div([                           
            dcc.Markdown('''### Region Parallel Coordinate Plots''', id = 'parallel'),
            html.Img(src='assets/parallel1.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### New England
                    The New England parallel coordinates plot covers the states of Connecticut, Maine, Massachusetts, New Hampshire, and Rhode Island.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            html.Img(src='assets/parallel2.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### Mid-Atlantic
                    The Mid-Atlantic parallel coordinates plot covers the states of New York, New Jersey, and Pennsylvania.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            html.Img(src='assets/parallel3.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### Southern
                    The Southern parallel coordinates plot covers the states of Delaware, Maryland, Virginia, Kentucky, Arkansas, Louisiana, Florida, Georgia, and Alabama.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            html.Img(src='assets/parallel4.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### Southwest
                    The Southern parallel coordinates plot covers the states of Texas, Arizona, New Mexico, and Oklahoma.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            html.Img(src='assets/parallel5.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### Pacific Coastal
                    The Pacific Coastal parallel coordinates plot covers the states of California, Oregon, and Washington.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            html.Img(src='assets/parallel6.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### Midwest
                    The Midwest parallel coordinates plot covers the states of Michigan, North Dakota, South Dakota, Minnesota, Kansas, Ohio, Indiana, Illinois, Wisconsin, and Missouri.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            html.Img(src='assets/parallel7.png', alt='Parallel Coordinates Plot'),
            html.Div([dcc.Markdown('''
                    #### Rocky Mountain
                    The Rocky Mountain parallel coordinates plot covers the states of Idaho, Colorado, Utah, Wyoming, and Nevada.
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
        ], style={'marginTop': 50, 'marginBottom': 50, 'textAlign': 'center'}),
        html.Hr(),
        html.Div([                             
            dcc.Markdown('''### Jointplots with Histogram''', id = 'jointhist'),
            html.Img(src='assets/jointplot1.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
    
            html.Img(src='assets/jointplot2.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
    
            html.Img(src='assets/jointplot3.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            
            html.Img(src='assets/jointplot4.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
        ], style={'marginTop': 50, 'marginBottom': 50, 'textAlign': 'center'}),
        html.Hr(),        
        html.Div([                             
            dcc.Markdown('''### Jointplots with Kernal Density Estimate''', id = 'jointkde'),
            html.Img(src='assets/jointplot5.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
    
            html.Img(src='assets/jointplot6.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
    
            html.Img(src='assets/jointplot7.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
            
            html.Img(src='assets/jointplot8.png', alt='Jointplot'),
            html.Div([dcc.Markdown('''
                    #### Comparison between 
                    This shows
                '''),
                ], style={'marginLeft': 150, 'marginRight': 150,'marginBottom': 100, 'textAlign': 'left'},
            ),
        ], style={'marginTop': 50, 'marginBottom': 50, 'textAlign': 'center'}),
                            
       
    ], style={'marginLeft': 150, 'marginRight': 150},
    ),
    
    html.Hr(),
    html.Div([dcc.Markdown('''
            ### References
            1. Kaggle - U.S. Pollution Dataset  
            https://www.kaggle.com/datasets/sogun3/uspollution?datasetId=312  
            
            2. CNN - New York City’s air pollution among the world’s worst as Canada wildfire smoke shrouds Northeast  
            https://www.cnn.com/2023/06/06/us/new-york-air-pollution-canada-wildfires-climate/index.html  

            3. NIH - Air Pollution and Your Health  
            https://www.niehs.nih.gov/health/topics/agents/air-pollution/index.cfm


        ''', id = 'references'),
        ], style={'marginTop': 50 , 'marginBottom': 50, 'marginLeft': 150, 'marginRight': 150},
    ),
    
], style={'marginLeft': 0, 'marginRight': 0},
)

@callback(
    Output(component_id='choropleth', component_property='figure'),
    Input(component_id='pollutant_radio', component_property='value'),
    Input(component_id='date_slider', component_property='value')
)
def update_choropleth(pollutant, date):
    df2 = df[df['Date Local'].str[:4].astype(int)== date]
    state_avg = df2.groupby('State', as_index = False)[pollutant].mean()
    state_avg_max = df.groupby('State', as_index = False)[pollutant].mean()
    fig = px.choropleth(state_avg, locations = state_avg['State'],
                        locationmode = 'USA-states', color = state_avg[pollutant],
                        hover_name = state_avg['State'], scope = 'usa',
                        color_continuous_scale = 'viridis', range_color = (0, state_avg_max[pollutant].max()))
    return fig

@callback(
    Output(component_id='choroplethAQI', component_property='figure'),
    Input(component_id='pollutant_radio_AQI', component_property='value'),
    Input(component_id='date_slider_AQI', component_property='value')
)
def update_choroplethAQI(pollutant, date):
    df2 = df[df['Date Local'].str[:4].astype(int)== date]
    state_avg = df2.groupby('State', as_index = False)[pollutant].mean()
    state_avg_max = df.groupby('State', as_index = False)[pollutant].mean()
    fig = px.choropleth(state_avg, locations = state_avg['State'],
                        locationmode = 'USA-states', color = state_avg[pollutant],
                        hover_name = state_avg['State'], scope = 'usa',
                        color_continuous_scale = 'viridis', range_color = (0, state_avg_max[pollutant].max()))
    return fig

@callback(
    Output(component_id='scatter1', component_property='figure'),
    Input(component_id='scatter_choice', component_property='value'),
)
def update_scatter(pollutant):
    dfnew = df.groupby('Date Local', as_index = False)[pollutant].mean()
    return px.scatter(dfnew, x = 'Date Local', y = pollutant)
 
# @callback(
#     Output(component_id='scatter1', component_property='figure'),
#     Input(component_id='scatter_choice', component_property='value'),
#     Input(component_id='date_slider_scatter', component_property='value')
# )
# def update_scatter(pollutant, date):
#     dftest = df[df['Date Local'].str[:4].astype(int)== date]
#     return px.scatter(dftest, x = 'Date Local', y = pollutant, hover_name = 'City')    

if __name__ == '__main__':
    app.run(debug=True)
