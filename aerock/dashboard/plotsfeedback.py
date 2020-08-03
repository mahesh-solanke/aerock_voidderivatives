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
def feedback_avgutil(airport_code):
    feedback_snapshot=db.api_fbavgutilsnapshot
    mongodocs_feedback_snapshot= list(feedback_snapshot.find())
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_feedback_snapshot = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_feedback_snapshot ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_feedback_snapshot = df_feedback_snapshot.append( series_obj )
    del df_feedback_snapshot['_id']
    df_icao_code_snapshot = df_feedback_snapshot[df_feedback_snapshot.icao_code == airport_code ]
    fig = make_subplots(rows=1, cols=1)
    #latest
    fig.add_trace(
        go.Bar(x=df_icao_code_snapshot.service_id, y=df_icao_code_snapshot.rating_for_service,name=airport_code+" rating of each service"),
        row=1, col=1
    )
    fig.update_xaxes(title_text="Service Id", row=1, col=1)
    fig.update_yaxes(title_text="Rating for Service", row=1, col=1)
    plot_div1 = fig.update_layout(height=600, width=1270, title_text=airport_code+" Data")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div
