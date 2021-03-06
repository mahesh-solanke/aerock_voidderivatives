
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot,iplot
from plotly.subplots import make_subplots
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority')
db_name = 'sihfinal'
db = client[db_name]


def kiosk_hour(date,airport_code):
    col = db["api_kioskhour"]
    myquery_aicode = {'icao_code':airport_code,'date':date}
    mongodocs_kiosk_hour= list(col.find(myquery_aicode))
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_kiosk_hour = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_kiosk_hour ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_kiosk_hour = df_kiosk_hour.append( series_obj )
    fig = make_subplots(rows=3, cols=1)
    fig.add_trace(
        go.Bar(x=df_kiosk_hour.hour, y=df_kiosk_hour.count_of_visits,hovertext=df_kiosk_hour['hour'] ,name=' number of visits '),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=df_kiosk_hour.hour, y=df_kiosk_hour.count_of_visits,hovertext=df_kiosk_hour['hour'] ,name=' pct_utilization'),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=df_kiosk_hour.hour, y=df_kiosk_hour.count_of_devices,hovertext=df_kiosk_hour['hour'] ,name=' count of devices'),
        row=3, col=1
    )
    fig.update_xaxes(title_text="Hour", row=1, col=1)
    fig.update_yaxes(title_text="Count of visits", row=1, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text="% Utilization", row=2, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text="Count of devices", row=3, col=1)
    plot_div1 = fig.update_layout(height=600, width=1270, title_text=airport_code + " Self Check-In Kiosk")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div
