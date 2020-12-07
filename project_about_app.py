# Build AppViewer
# from jupyterlab_dash import AppViewer
# viewer = AppViewer()

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions
def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Project Outline')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('Old boys', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/cengc13/data1050-final-project'),
    ], className="row")


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            ## Project Architecture 
            This section is copied from [EnergyPlanner](https://github.com/blownhither/EnergyPlanner).
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


def project_about():
    """
    Returns the outline of the project
    """
    return html.Div(children=[dcc.Markdown('''
        ## About

        * Names of all team members: Cheng Zeng, Tianqi Tang, Zhi Wang
        * Project & Executive Summary
            * We will create a live data-science web application named “Covid-19 tracker”.
            It uses covid-19 data from the New York Times to understand and project the
            spread of the outbreak in the United States at hierarchical granularity,
            ranging from national to county level. It will allow users to interactively
            view the covid cases and death at different levels.
            * This final project uses gitpod as the platform, an online IDE for github
            repo for data collection, clean-up, transformation and visualization.
            The data will be stored in Mongodb, through the adaptor of a python module named “pymongo”.
            The EDA, visualization and enhancement will be  in jupyter notebooks.
            The interactive web application will be realized using plotly and Dash.
            It will mainly comprise three sections, namely Introduction, EDA & Visualization and Enhancement.
            The enhancement section is aimed at figure out whether two factors of interest might affect the transmission
            in states, and also a simple regression model is constructed to  project the trend of the pandemic in US.
            * At the end of this project, we hope to build up a web application which tracks the up-to-date Covid-19 situation
             at various geographical levels. Meanwhile it aims to provide some insights on if restrictions, such as wearing masks,
             can help to contain the pandemic.
        * Datasets used:
            * The covid national-level and state-level datasets  are from The New York Times,
         based on reports from state and local health agencies. They contain a series of data files with cumulative counts of
         coronavirus cases in the United States, at the national and state level, over time. They are regularly updated every day.
         The national level data is about 7 KB. The state level data is 463 KB. The covid datasets lives on the github repo by the New York Times.
         These are raw texts that can be scraped in a straightforward way using the “request” python module.
         The raw data will be updated every day. So the incremental updates using the web scraping method will be done automatically.
            * The static survey data regarding the propensity to wearing masks (109 KB), state-level population data (1 KB),
            and state area data (884 B) are used to understand how the role of wearing face coverings and population density
            in the course of the pandemic.
        * Summary of performance with respect to the baseline model(s)
            * We figure out that there is a strong correlation between infection rate and population density in US states.
            * There exists a high negative correlation between the propensity to wear masks and the case fatality rate in states.
            * In the next steps, we aim to build a simple regression model to predict the trend of outbreak in US. 
            We use the historical covid data and demongraphic featurs ad predictors, and we target on prediction of
            near-future case and death count. It is an ongoing work 
            (Please see [this notebook](https://github.com/cengc13/data1050-final-project/blob/main/Enhancement_Tianqi.ipynb)) 
        * Possible next steps
            * Since the county-level data contains mountains of items, it is not shown in the web application. In view of this, next we can
            move on to some other cloud platforms for data storage/update/fetch, and web engine, for example GCP and AWS.
            * We could explore more features to improve the model performance (accuracy and training efficiency)
            * Based on the insights gained through the correlation analysis, we can estimate the 'what-if' trend of 
            the outbreak in each state if more people are willing to comply with rules such as social distancing and wearing face coverings.
        * References to related work
            * A detailed map of who is wearing masks in the U.S. from
            [NYTimes](https://www.nytimes.com/interactive/2020/07/17/upshot/coronavirus-face-mask-map.html).
            This website uses the mask-use-by-counties data to show patterns of wearing masks by county.
            * Covid in the U.S.: Latest Map and Case Count from [NYTimes](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html).
            Combining demographic and population data, it shows the map for positive and death rates at state and county level.
            * CDC calls on Americans to wear masks to prevent COVID-19 spread from
            [CDC](https://www.cdc.gov/media/releases/2020/p0714-americans-to-wear-masks.html). It highlights the importance of
            wearing face coverings in slowing the spread of covid.


        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def additional_project_details():
    """
    Returns the additional project details.
    """
    return html.Div(children=[dcc.Markdown('''
        ## Additional details

        * Development Process and Final Technology Stack.
            Please find the project architecture for details.
        * Data Acquisition, Caching, ETL Processing, Database Design
            * Data Acquisition: the covid datasets and mask-use dataset are scraped from NYTime github repo. The population and area data for states come
            from wikipedia.
            * Caching: the datasets are cached with the aid of `expiringdict` module. No more than 10 elements can be in the caching and if the length exceeds
            the limit, the oldest item will be removed.
            * ETL Processing: datasets are upserted in to local MongoDB databases through the python 'adapter' `pymongo` module. Then the dataset can be
            readily loaded.
            * Database Design: all datasets in this project are saved in a MongoDB database named 'covid-us'. Then each dataset, corresponding to
            a collection in MongoDB, is updated. In this way the database in this project looks like a two-level tree structure.
        * Link to the 'ETL_EDA.ipynb' notebook: [ETL_EDA](https://github.com/cengc13/data1050-final-project/blob/main/ETL_EDA.ipynb)
        * Link to the 'Enhancement.ipynb' notebook: [Enhancement](https://github.com/cengc13/data1050-final-project/blob/main/Enhancement.ipynb).
        Note that figures plotted with `plotly` cannot be shown in jupyter notebooks on github.


        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        project_about(),
        additional_project_details(),
        architecture_summary(),
    ], className='row', id='content')

# set layout to a function which updates upon reloading
app.layout = dynamic_layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')
    # viewer.show(app)