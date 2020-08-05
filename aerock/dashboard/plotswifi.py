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
def wifi_hour(date, airport_code):
    col = db["api_wifihour"]
    myquery_aicode = {'icao_code':airport_code,'date':date}
    mongodocs_wifi_hour= list(col.find(myquery_aicode))
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_wifi_hour = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_wifi_hour ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_wifi_hour = df_wifi_hour.append( series_obj )
    fig = make_subplots(rows=5, cols=1)
    fig.add_trace(
        go.Bar(x=df_wifi_hour.hour, y=df_wifi_hour.avg_utilization_min,name= " Average utilization of Wifi"),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=df_wifi_hour.hour, y=df_wifi_hour.total_download,name=" Total Downloads(GB)"),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=df_wifi_hour.hour, y=df_wifi_hour.total_upload,name=" Total Uploads(GB)"),
        row=3, col=1
    )
    fig.add_trace(
        go.Bar(x=df_wifi_hour.hour, y=df_wifi_hour.total_used_minutes,name=" Total used minutes"),
        row=4, col=1
    )
    fig.add_trace(
        go.Bar(x=df_wifi_hour.hour, y=df_wifi_hour.total_unique_users,name=" Total user count"),
        row=5, col=1
    )
    fig.update_xaxes(title_text="Hour", row=1, col=1)
    fig.update_yaxes(title_text="Average utilization min", row=1, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text="Total download", row=2, col=1)
    fig.update_xaxes(title_text="Hour", row=3, col=1)
    fig.update_yaxes(title_text="Total upload", row=3, col=1)
    fig.update_xaxes(title_text="Hour", row=4, col=1)
    fig.update_yaxes(title_text="Total used minutes", row=4, col=1)
    fig.update_xaxes(title_text="Hour", row=5, col=1)
    fig.update_yaxes(title_text="total unique users", row=5, col=1)
    plot_div1 = fig.update_layout(height=900, width=1270, title_text=airport_code+" Data")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div
