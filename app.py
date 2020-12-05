import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go

from database import fetch_all_db_as_df

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions

def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Interactive visualization with Dash and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('Old boys', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/cengc13/data1050-final-project'),
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # US COVID-19 Tracker
        
        The coronavirus pandemic has caused more than a Million deaths in the globe. The situation is very severe
        in the United States. Therefore, it is of crucial importance to understand and project
        the trend of COVID-19 cases so that policy-makers can come up with short-term and long-term strategies to
        limit the spread and mitigate the effect of another outbreak in the near future.

        **US COVID-19 tracker is a "What-If" tool to assist making strategies.**
        It can be used to understand and project the trend if more precautions and restrictions are taken.

        ### Data Source
        Covid-19 tracker utilizes historical and live covid-19 data from 
        [New York Times github repository](https://github.com/nytimes/covid-19-data).
        The [data source](https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv) 
        **is updated every day**.
        Also, the data for state and county population is merged to obtain the positive rate over population at different 
        geographical levels.
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def time_series_cumulative(label):
    colors = { 
    "cases": 'rgba(80, 26, 80, 0.2)', 
    "deaths": 'rgba(16, 112, 2, 0.2)'
    }
    df_dict = fetch_all_db_as_df()
    df = df_dict['covid-us']
    x = df['date']
    trace = go.Scatter(x=x, y=df[label], mode='lines', name=label, fill='tozeroy',
                       fillcolor=colors[label], 
                       line={'width': 2, 'color': colors[label]})

    title = f'Cumulative Covid {label.lower()} in U.S. over time'
    layout = dict(title=title,
#                   plot_bgcolor='#23272c',
#                   paper_bgcolor='#23272c',
                  yaxis_title=f'# of {label}',
                  xaxis_title='Date/Time',
                 
                  font=dict(family="Courier New, monospace",
                            size=16))
    data = [trace]
    fig = dict(data=data, layout=layout)
    return fig



def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')


# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
        dcc.Graph(id='case-total-us', figure=time_series_cumulative(label='cases')),
        dcc.Graph(id='death-total-us', figure=time_series_cumulative(label='deaths')),
        # what_if_description(),
        # what_if_tool(),
        architecture_summary(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components

def what_if_description():
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        # " What If "
        So far, BPA has been relying on hydro power to balance the demand and supply of power. 
        Could our city survive an outage of hydro power and use up-scaled wind power as an
        alternative? Find below **what would happen with 2.5x wind power and no hydro power at 
        all**.   
        Feel free to try out more combinations with the sliders. For the clarity of demo code,
        only two sliders are included here. A fully-functioning What-If tool should support
        playing with other interesting aspects of the problem (e.g. instability of load).
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("Rescale Power Supply", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.Slider(id='wind-scale-slider', min=0, max=4, step=0.1, value=2.5, className='row',
                           marks={x: str(x) for x in np.arange(0, 4.1, 1)})
            ], style={'marginTop': '5rem'}),

            html.Div(id='wind-scale-text', style={'marginTop': '1rem'}),

            html.Div(children=[
                dcc.Slider(id='hydro-scale-slider', min=0, max=4, step=0.1, value=0,
                           className='row', marks={x: str(x) for x in np.arange(0, 4.1, 1)})
            ], style={'marginTop': '3rem'}),
            html.Div(id='hydro-scale-text', style={'marginTop': '1rem'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    ], className='row eleven columns')



@app.callback(
    dash.dependencies.Output('wind-scale-text', 'children'),
    [dash.dependencies.Input('wind-scale-slider', 'value')])
def update_wind_sacle_text(value):
    """Changes the display text of the wind slider"""
    return "Wind Power Scale {:.2f}x".format(value)


@app.callback(
    dash.dependencies.Output('hydro-scale-text', 'children'),
    [dash.dependencies.Input('hydro-scale-slider', 'value')])
def update_hydro_sacle_text(value):
    """Changes the display text of the hydro slider"""
    return "Hydro Power Scale {:.2f}x".format(value)


@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('wind-scale-slider', 'value'),
     dash.dependencies.Input('hydro-scale-slider', 'value')])
def what_if_handler(wind, hydro):
    """Changes the display graph of supply-demand"""
    df = fetch_all_db_as_df(allow_cached=True)
    x = df['date']
    supply = df['Wind'] * wind + df['Hydro'] * hydro + df['Fossil/Biomass'] + df['Nuclear']
    load = df['Load']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
                  fill='tozeroy'))
    fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
                  fill='tonexty'))
    fig.update_layout(template='plotly_dark', title='Supply/Demand after Power Scaling',
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='MW',
                      xaxis_title='Date/Time')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
