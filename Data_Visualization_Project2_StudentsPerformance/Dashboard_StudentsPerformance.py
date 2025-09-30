import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data
df = pd.read_csv("StudentsPerformance.csv")

# Initialize Dash app
app = Dash(__name__)
app.title = "Students Performance Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Students Performance Dashboard", style={'textAlign':'center'}),
    
    # Filters
    html.Div([
        html.Label("Select Gender:"),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[{'label': g, 'value': g} for g in df['gender'].unique()],
            value=df['gender'].unique().tolist(),
            multi=True
        ),
    ], style={'width':'30%', 'display':'inline-block'}),
    
    html.Div([
        html.Label("Select Test Preparation Course:"),
        dcc.Dropdown(
            id='prep-dropdown',
            options=[{'label': p, 'value': p} for p in df['test preparation course'].unique()],
            value=df['test preparation course'].unique().tolist(),
            multi=True
        ),
    ], style={'width':'30%', 'display':'inline-block', 'marginLeft':'10px'}),
    
    html.Div([
        html.Label("Select Parental Level of Education:"),
        dcc.Dropdown(
            id='parent-edu-dropdown',
            options=[{'label': p, 'value': p} for p in df['parental level of education'].unique()],
            value=df['parental level of education'].unique().tolist(),
            multi=True
        ),
    ], style={'width':'30%', 'display':'inline-block', 'marginLeft':'10px'}),
    
    html.Br(),
    
    # Graphs
    dcc.Graph(id='avg-score-bar'),
    dcc.Graph(id='gender-race-count'),
    dcc.Graph(id='test-prep-pie')
])

# Callbacks
@app.callback(
    Output('avg-score-bar', 'figure'),
    Output('gender-race-count', 'figure'),
    Output('test-prep-pie', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('prep-dropdown', 'value'),
    Input('parent-edu-dropdown', 'value')
)
def update_charts(selected_genders, selected_prep, selected_parent_edu):
    # Filter data
    filtered_df = df[
        df['gender'].isin(selected_genders) &
        df['test preparation course'].isin(selected_prep) &
        df['parental level of education'].isin(selected_parent_edu)
    ]
    
    # 1. Average Scores by Gender
    avg_scores = filtered_df.groupby('gender')[['math score','reading score','writing score']].mean().reset_index()
    avg_scores_melted = avg_scores.melt(id_vars='gender', var_name='Subject', value_name='Average Score')
    fig_avg = px.bar(avg_scores_melted, x='gender', y='Average Score', color='Subject', barmode='group',
                     title="Average Scores by Gender")
    
    # 2. Gender count in each Race/Ethnicity
    race_gender = filtered_df.groupby(['race/ethnicity','gender']).size().reset_index(name='Count')
    fig_race = px.bar(race_gender, x='race/ethnicity', y='Count', color='gender', barmode='group',
                      title="Number of Students by Gender in Each Race/Ethnicity")
    
    # 3. Test Preparation Course distribution
    prep_counts = filtered_df['test preparation course'].value_counts().reset_index()
    prep_counts.columns = ['Test Prep', 'Count']
    fig_pie = px.pie(prep_counts, values='Count', names='Test Prep', title='Test Preparation Course Distribution')
    
    return fig_avg, fig_race, fig_pie

# Run server
if __name__ == '__main__':
    app.run(debug=True)
