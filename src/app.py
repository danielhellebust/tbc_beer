import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from dash_mantine_components import MantineProvider, Container,Image, Chip,ChipGroup, Slider
import pandas as pd
import dash_auth
from flask import request
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://beer:beer@cluster0.rhshz.mongodb.net/")  # Replace with your MongoDB connection string
db = client['Beer']  # Replace with your database name
collection = db['beer_review']  # Replace with your collection name

# Taste options
taste_options = [
    'Toast, tørket frukt, dadler, malt.',
    'Maltsødme, karamell, tørket frukt, røyk og sitrus',
    'Tørket frukt, karamell',
    'Sødmefull, balansert med smak av karamell, lett krydder og fiken',
    'Fruktig og lett sødmefull, god bitterhet.',
    'Kaffe, sjokolade, karamell, lær og kirsebær.'
]

# Aroma options
aroma_options = [
    'Fruktig, malt, lett karamell',
    'Krydder, nellik, appelsin, malt',
    'Røyk, sjokolade, kaffe, tørket frukt',
    'Karamell, fruktig, malt, nøtter',
    'Krydder, malt, karamell, fruktig',
    'Sjokolade, kaffe, karamell, tørket frukt'
]

# Øl stil
beer_style = [
    'Mørk lager',
    'Spesial',
    'Pale ale',
    'Porter & stout']

# Create an empty DataFrame to store the reviews
reviews_df = pd.DataFrame(
    columns=['Rytter','Juleøl_nummer','Navn_på_øl',
                      'Øl_stil', 'Rating', 'Aroma', 'Smak',
                      'Alkohol_prosent', 'Kommentarer'])

# Sample beer names for the dropdown
beer_names = ['','Løkka Julebokk', 'Nøgne Julequad', 'Nøgne My Big Fat Greek X-mas', 'Jacobsen Christmas Ale', 'Berentsens Jule Avec', 'Vossa Jol']
taste_number = ['Register','1','2','3','4','5','6','7','8','9','10']

# Define valid usernames and passwords
VALID_USERNAME_PASSWORD_PAIRS = {
    'Test':'Test',
    'Magnus': 'Lande', 'Daniel':'Hellebust', 'Fasit':'Fasit',
    'Daniel The Crest':'Haugen', 'Paul':'Kastmann', 'Håkon':'Ellekjær',
    'Øyvind':'Størdal'
    # Add more username-password pairs as needed
}



app = dash.Dash(__name__)
# Enable basic authentication
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server

app.layout = MantineProvider(
    theme={"colorScheme": "dark"},
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        Container(
            style={'maxWidth': '800px', 'margin': 'auto'},
            children=[
                html.H1("TBC Juleøl Smaking 2023", style={'textAlign': 'center', 'marginBottom': '20px'}),
                html.Img(src=app.get_asset_url('tbc.jpg'), style={'width': '100%', 'marginBottom': '20px'}),
                html.Label("Rytter:"),
                dcc.Textarea(id='participant-name', style={'marginBottom': 10, 'width': '100%'}, disabled=True),

                html.Label("Juleøl nummer:"),
                ChipGroup(
                    id='tasting-number',
                    children=[Chip(option, value=option) for option in taste_number],
                    value=taste_number[0],
                    style={'marginBottom': 10, 'width': '100%'}
                ),

                html.Label("Navn på øl:"),
                ChipGroup(
                    id='beer-name',
                    children=[Chip(option, value=option) for option in beer_names],
                    value=beer_names[0],
                    style={'marginBottom': 10, 'width': '100%'}
                ),

                html.Label("Øl stil:"),
                ChipGroup(
                    id='beer-style',
                    children=[Chip(option, value=option) for option in beer_style],
                    style={'marginBottom': 10, 'width': '100%'}
                ),

                html.Label("Rating:"),
                Slider(
                    id='rating',
                    value=0,
                    min=0,
                    max=5,
                    marks=[
                        {"value": "0", "label": "0"},
                        {"value": "1", "label": "1"},
                        {"value": "2", "label": "2"},
                        {"value": "3", "label": "3"},
                        {"value": "4", "label": "4"},
                        {"value": "5", "label": "5"},

                        ],
                    precision=1,
                    step=0.1,
                    style={'color': 'yellow','marginBottom': 15}
                ),

                html.Label("Aroma:"),
                ChipGroup(
                    id='aroma',
                    children=[Chip(option,value=option) for option in aroma_options],
                    style={'marginBottom': 10, 'width': '100%'}
                ),

                html.Label("Smak:"),
                ChipGroup(
                    id='taste',
                    children=[Chip(option,value=option) for option in taste_options],
                    style={'marginBottom': 10, 'width': '100%'}
                ),
                html.Label("Alkohol prosent:"),
                Slider(
                    id='alcohol-percentage',
                    value=0,
                    min=0,
                    max=20,
                    marks=[
                        {"value": "0", "label": "0"},
                        {"value": "1", "label": "1"},
                        {"value": "2", "label": "2"},
                        {"value": "3", "label": "3"},
                        {"value": "4", "label": "4"},
                        {"value": "5", "label": "5"},
                        {"value": "6", "label": "6"},
                        {"value": "7", "label": "7"},
                        {"value": "8", "label": "8"},
                        {"value": "9", "label": "9"},
                        {"value": "10", "label": "10"},
                        {"value": "11", "label": "11"},
                        {"value": "12", "label": "12"},
                        {"value": "13", "label": "13"},
                        {"value": "14", "label": "14"},
                        {"value": "15", "label": "15"},
                        {"value": "16", "label": "16"},
                        {"value": "17", "label": "17"},
                        {"value": "18", "label": "18"},
                        {"value": "19", "label": "19"},
                        {"value": "20", "label": "20"}

                    ],
                    precision=1,
                    step=0.1,
                    style={'color': 'yellow','marginBottom': 15}
                ),

                html.Label("Kommentarer:"),
                dcc.Textarea(id='comments', value='', style={'marginBottom': 10, 'width': '100%'}),

                html.Button('Send avgårde din mening', id='submit-button', n_clicks=0, style={'width': '100%'}),

                html.Div(id='review-table-container', style={'marginTop': '20px'}),
            ],
        ),
    ],
)


@app.callback(
    [Output('review-table-container', 'children'),
     Output('participant-name', 'value')],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('participant-name', 'value'),
     dash.dependencies.State('tasting-number', 'value'),
     dash.dependencies.State('beer-name', 'value'),
     dash.dependencies.State('beer-style', 'value'),
     dash.dependencies.State('rating', 'value'),
     dash.dependencies.State('aroma', 'value'),
     dash.dependencies.State('taste', 'value'),
     dash.dependencies.State('alcohol-percentage', 'value'),
     dash.dependencies.State('comments', 'value')]
)
def update_reviews(n_clicks, participant_name, tasting_number, beer_name, beer_style, rating, aroma, taste,
                   alcohol_percentage, comments):
    username = ''
    if n_clicks > 0:

        username = request.authorization['username']
        participant_name = username if not participant_name else participant_name
        key = f"{participant_name}_{tasting_number}"
        new_review = {'Rytter': participant_name, 'Juleøl_nummer': tasting_number, 'Navn_på_øl': beer_name,
                      'Øl_stil': beer_style, 'Rating': rating, 'Aroma': aroma, 'Smak': taste,
                      'Alkohol_prosent': alcohol_percentage, 'Kommentarer': comments}

        # Push data to MongoDB with the composite key
        if participant_name != '':
            collection.update_one({'_id': key}, {'$set': new_review}, upsert=True)

        # Create a new DataFrame for each review
        review_df = pd.DataFrame.from_dict([new_review], orient='columns')

        # Combine the new review DataFrame with the existing reviews
        global reviews_df
        reviews_df = pd.concat([reviews_df, review_df], ignore_index=True).drop_duplicates()
        username = request.authorization['username']


    return generate_review_table(reviews_df), username


def generate_review_table(reviews_df):
    table = html.Table(
        # Header
        [html.Tr([html.Th(col, style={'text-align': 'center'}) for col in reviews_df.columns])] +
        # Body
        [html.Tr([html.Td(str(reviews_df.iloc[i][col]), style={'text-align': 'center'}) for col in reviews_df.columns]) for i in range(len(reviews_df))]
    )
    return table



if __name__ == '__main__':
    app.run_server(debug=True)
