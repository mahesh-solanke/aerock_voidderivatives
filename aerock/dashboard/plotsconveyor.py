import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot,iplot
from plotly.subplots import make_subplots
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority')
db_name = 'sihfinal'
db = client[db_name]

def conveyor_hour(date, airport_code):
    col1 = db["api_cbperutilhour"]
    col2 = db["api_cbavghour"]
    myquery_aicode = {'icao_code':airport_code,'date':date}
    mongodocs_conveyor_utilhour= list(col1.find(myquery_aicode))
    mongodocs_conveyor_avghour= list(col2.find(myquery_aicode))
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_conveyor_utilhour = pd.DataFrame(columns=[])
    df_conveyor_avghour = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_conveyor_utilhour ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_conveyor_utilhour = df_conveyor_utilhour.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_conveyor_avghour ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_conveyor_avghour = df_conveyor_avghour.append( series_obj )
    fig = make_subplots(rows=2, cols=1)
    #hour wise percentage opr time
    fig.add_trace(
        go.Bar(x=df_conveyor_utilhour.hour, y=df_conveyor_utilhour.pct_opr_allconveyorbelts,hovertext=df_conveyor_utilhour['cb_id'],name=" % Operational time of each CB"),
        row=1, col=1
    )
    #avg hour
    fig.add_trace(
        go.Bar(x=df_conveyor_avghour.hour, y=df_conveyor_avghour.avg_opr_allconveyorbelts_min, name=" Hourly Average operation tile of all CB"),
        row=2, col=1
    )
    fig.update_xaxes(title_text="Hour", row=1, col=1)
    fig.update_yaxes(title_text="Oprational of all CB", row=1, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text="Average oprerational min of all CB ", row=2, col=1)
    plot_div1 = fig.update_layout(height=600, width=1270, title_text=airport_code+" Data")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div

