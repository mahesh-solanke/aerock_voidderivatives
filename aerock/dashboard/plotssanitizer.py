import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot,iplot
from plotly.subplots import make_subplots
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority')
db_name = 'aerockdb'
db = client[db_name]

def sanitizer_hour(date, airport_code):
    col = db["api_sncalchour"]
    myquery_aicode = {'icao_code':airport_code,'date':date}
    mongodocs_sanitizer_hour= list(col.find(myquery_aicode))
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_sanitizer_hour = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_sanitizer_hour ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_sanitizer_hour = df_sanitizer_hour.append( series_obj )
    df_sanitizer_newhour=pd.DataFrame(df_sanitizer_hour.groupby(['date','hour'],as_index=False).agg({'avg_dispenses':(sum),'count_dispenses':(sum)}))
    fig = make_subplots(rows=2, cols=1)
    #hour
    fig.add_trace(
        go.Bar(x=df_sanitizer_newhour.hour, y=df_sanitizer_newhour.avg_dispenses,name="Averageg Dispenses"),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(x=df_sanitizer_newhour.hour, y=df_sanitizer_newhour.count_dispenses,name=" Count Dispenses "),
        row=2, col=1
    )
    fig.update_xaxes(title_text="Hour", row=1, col=1)
    fig.update_yaxes(title_text="avg dispenses", row=1, col=1)
    fig.update_xaxes(title_text="Hour", row=2, col=1)
    fig.update_yaxes(title_text="count_dispenses", row=2, col=1)
    plot_div1 = fig.update_layout(barmode='group', height=600, width=1270, title_text= airport_code + " Sanitizer data")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div


