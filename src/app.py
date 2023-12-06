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
    'Fyldig smak',
    'Lett smak.',
    'Røstet kaffe, karamell, sjokolade.',
    'Lett kornpreget malt, balansert bitterhet, fruktig humle med fokus på sitrus.',
    'Fyldig og søtt øl med smak av pepperkaker',
    'Kremet med god bitterhet, preg av mørkt malt, sitrus, ingefær, nellik og kanel, litt kaffe og rosin.',
    'Smak av gran og krydder, innslag av tropisk frukt.',
    'Moderat bitterhet og sødme'
    
]

# Aroma options
aroma_options = [
    'Aroma av brent karamell.',
    'Toner av malt og tørket frukt.',
    'Mørk sjokolade og kaffe.',
    'Appelsin, sitrus, furu.',
    'Kardemomme, korianderfrø, kanel, ingefær, nellikK',
    'Krydret og pepret preg av mørkt malt, rosin, ingefær og nellik, litt kanel, kardemomme og kaffe.',
    'Duft av furu, krydder, frukt.',
    'Aroma av malt og krydder.'
]

# Øl stil
beer_style = [
    'Mørk lager',
    'India pale ale',
    'Porter & stout',
'Krydret',
'Alkoholfritt øl']

# Create an empty DataFrame to store the reviews
reviews_df = pd.DataFrame(
    columns=['Rytter','Juleøl_nummer','Navn_på_øl',
                      'Øl_stil', 'Rating', 'Aroma', 'Smak',
                      'Alkohol_prosent', 'Kommentarer'])

# Sample beer names for the dropdown
beer_names = ['','Sagene Sterk Jul',
              'Flåklypa Spesial Juleøl',
              'The Piggy Chocomas Party',
              'John McClane Xmas',
              'Endelig Jul',
              'Nøgne Ø Julefri',
              'Graff Julejuice',
              'Juleglede'
              ]
taste_number = ['Register',
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                ]

# Define valid usernames and passwords
VALID_USERNAME_PASSWORD_PAIRS = {
    'Test1':'Test1',
    'Test2':'Test2',
    'Arnstein': 'Haugbråten',
    'Daniel':'Hellebust',
    'Fasit':'Fasit',
    'Kristin':'Haugbråten',
    'Siv':'Sarsten'
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
                html.Img(src=app.get_asset_url('alpingutu.jpg'), style={'width': '100%', 'marginBottom': '20px'}),
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
                    children=[Chip(option, value=option) for option in sorted(beer_names)],
                    value=beer_names[0],
                    style={'marginBottom': 10, 'width': '100%'}
                ),

                html.Label("Øl stil:"),
                ChipGroup(
                    id='beer-style',
                    children=[Chip(option, value=option) for option in sorted(beer_style)],
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
                    children=[Chip(option,value=option) for option in sorted(aroma_options)],
                    style={'marginBottom': 10, 'width': '100%'}
                ),

                html.Label("Smak:"),
                ChipGroup(
                    id='taste',
                    children=[Chip(option,value=option) for option in sorted(taste_options)],
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

        # Fetch the JSON object from MongoDB
        existing_review = collection.find_one({'_id': f'Fasit_{tasting_number}'})
        if existing_review:
            # Extract aroma and taste from the existing JSON
            existing_aroma = existing_review.get('Aroma', '')
            existing_taste = existing_review.get('Smak', '')
            existing_name = existing_review.get('Navn_på_øl', '')
            existing_style = existing_review.get('Øl_stil', '')
            existing_alcohol_percentage = existing_review.get('Alkohol_prosent', '')

            # Compare chosen chips with existing aroma and taste
            aroma_score = 10 if aroma == existing_aroma else 0
            taste_score = 10 if taste == existing_taste else 0
            name_score = 50 if beer_name == existing_name else 0
            style_score = 10 if beer_style == existing_style else 0
            calculate_percentage_match = lambda p1, p2, max_diff=100: max(0, 100 * (1 - abs(p1 - p2) / max_diff))
            alcohol_score = calculate_percentage_match(alcohol_percentage, existing_alcohol_percentage, 20)

            # Update the scores in the existing JSON
            new_review['Aroma_Score'] = aroma_score
            new_review['Taste_Score'] = taste_score
            new_review['Name_Score'] = name_score
            new_review['Style_Score'] = style_score
            new_review['Alcohol_Score'] = alcohol_score
            new_review['Total_Score'] = aroma_score + taste_score + name_score + style_score + alcohol_score



        # Push data to MongoDB with the composite key
        if participant_name != '':
            collection.update_one({'_id': key}, {'$set': new_review}, upsert=True)

        # Create a new DataFrame for each review
        review_df = pd.DataFrame.from_dict([new_review], orient='columns')

        # Combine the new review DataFrame with the existing reviews
        global reviews_df
        reviews_df = pd.concat([reviews_df, review_df], ignore_index=True).drop_duplicates()
        reviews_df = reviews_df[['Rytter', 'Juleøl_nummer', 'Navn_på_øl', 'Øl_stil', 'Rating', 'Aroma', 'Smak','Total_Score', 'Kommentarer']]
        username = request.authorization['username']
        reviews_df = reviews_df[reviews_df['Rytter'] == username]



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
