import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
#import chart_studio.plotly as py
import pandas as pd
from plotly.subplots import make_subplots
from pymongo import MongoClient

#logger = logging.getLogger(__name__)
client = MongoClient('mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority')
db_name = 'sihfinal'
db = client[db_name]
def trolley_hour(date, airport_code):
    col = db["api_trolleycalchour"]
    myquery_aicode = {'icao_code':airport_code,'date':date}
    mongodocs_trolley_hour= list(col.find(myquery_aicode))
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_trolley_hour = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_trolley_hour ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_trolley_hour = df_trolley_hour.append( series_obj )
    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(
        go.Scatter(x=df_trolley_hour.hour, y=df_trolley_hour.pct_utilization,name=" Hour wise % utilization of trolleys"),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df_trolley_hour.hour, y=df_trolley_hour.count_used,name=" Hour wise used trolleys"),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df_trolley_hour.hour, y=df_trolley_hour.count_unused,name=" Hour wise unused trolleys"),
        row=3, col=1
    )
    fig.update_xaxes(title_text="Hour", row=1, col=1)
    fig.update_yaxes(title_text="% Utilization", row=1, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text="Count Used", row=2, col=1)
    fig.update_xaxes(title_text="Hour", row=3, col=1)
    fig.update_yaxes(title_text="countunused", row=3, col=1)
    plot_div1 = fig.update_layout(height=600, width=1270, title_text=airport_code +" Data")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div

