import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import flask

pio.templates.default = "plotly"


app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server = app, url_base_pathname = '/',external_stylesheets=[dbc.themes.FLATLY],)

url = 'https://raw.githubusercontent.com/lucaswb15/r6data/master/R6%20Data%20-%20Ranked.csv'
df = pd.read_csv(url)


#Kills Line
kills_long = pd.melt(df, id_vars=['Game'],value_vars=['Lucas Kills','Hans Kills','David Kills','Sam Kills','Ryan Kills'])
kills_long.columns= ['Game','Player','Kills']
kills_line = px.line(kills_long, x='Game', y='Kills', color='Player')
kills_line.update_traces(mode='lines+markers')
kills_line.update_layout(yaxis=dict(range=[0,14]),title={'text':'Kills by Player','xanchor':'center','x':.5})

#=============================================================================
#Kills Average
kills = df[['Lucas Kills','Hans Kills','David Kills','Sam Kills','Ryan Kills']]

kills_avg = kills.mean()
kills_avg = kills_avg.reset_index()
kills_avg = kills_avg.rename(columns={"index": "Player", 0: "Kills"})

#=============================================================================
#Kills Pie
kills_pie = px.pie(kills_avg, values = 'Kills', names = 'Player')
kills_pie.update_layout(title={'text':'Average Number of Kills per Player','xanchor':'center','x':.5})
kills_pie.update_traces(textinfo='value+label')

app.layout = html.Div([
        dbc.Row(
                dbc.Col(html.H3("Holy Milk R6 Dashboard"),
                        width={'size': 6, 'offset': 5},
                        ),
                ),
        dbc.Row([dbc.Col(dcc.Graph(id='kills_line',figure = kills_line),
                        width={'size':9,'offest':0,'order':2}),
                dbc.Col(dcc.Graph(id='kills_pie',figure=kills_pie),
                        width={'size':3,'order':1})
                ]
            ),

])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=80)
