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

def top3(date, airport_code):
    col1 = db["api_boardtop3utilization"]
    col2 = db["api_trolleytop3utilization"]
    col3 = db["api_wifihour"]
    col5 = db["api_parkingtop3utilization"]
    col6 = db["api_cbtop3utilization"]
    col7 = db["api_sntop3utilization"]
    col8 = db["api_kiosktop3utilization"]
    myquery_aicode = {'date':date}
    myquery_aicode1 = {'icao_code':airport_code}
    mongodocs_boarding_top3 = list(col1.find(myquery_aicode))
    mongodocs_trolley_top3 = list(col2.find(myquery_aicode))
    mongodocs_wifi_top3 = list(col3.find(myquery_aicode))
    mongodocs_parking_top3= list(col5.find(myquery_aicode))
    mongodocs_conveyor_top3= list(col6.find(myquery_aicode))
    mongodocs_sanitizer_top3= list(col7.find(myquery_aicode))
    mongodocs_kiosk_top3= list(col8.find(myquery_aicode))
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_boarding_top3 = pd.DataFrame(columns=[])
    df_trolley_top3 = pd.DataFrame(columns=[])
    df_wifi_top3 = pd.DataFrame(columns=[])
    df_parking_top3 = pd.DataFrame(columns=[])
    df_conveyor_top3 = pd.DataFrame(columns=[])
    df_sanitizer_top3 = pd.DataFrame(columns=[])
    df_kiosk_top3 = pd.DataFrame(columns=[])
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_boarding_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_boarding_top3 = df_boarding_top3.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_trolley_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_trolley_top3= df_trolley_top3.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_wifi_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_wifi_top3= df_wifi_top3.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_parking_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_parking_top3 = df_parking_top3.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_conveyor_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_conveyor_top3 = df_conveyor_top3.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_sanitizer_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_sanitizer_top3 = df_sanitizer_top3.append( series_obj )
    # iterate over the list of MongoDB dict documents
    for num, doc in enumerate( mongodocs_kiosk_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_kiosk_top3 = df_kiosk_top3.append( series_obj )
    #groupby as date boarding date
    df_icao_code = pd.DataFrame(df_boarding_top3.groupby(['icao_code'],as_index=False).agg({'pct_utilization':('sum')}))
    df_large3_boarding = df_boarding_top3.nlargest(3, "pct_utilization") 
    #groupby as date trolley
    df_icao_code_trolley = pd.DataFrame(df_trolley_top3.groupby(['icao_code'],as_index=False).agg({'pct_utilization':('sum')}))
    df_large3_trolley = df_trolley_top3.nlargest(4, "pct_utilization") 
    #groupby as date parking
    df_icao_code_parking = pd.DataFrame(df_parking_top3.groupby(['icao_code'],as_index=False).agg({'pct_utilization':('sum')}))
    df_large3_parking = df_parking_top3.nlargest(3, "pct_utilization") 
    #groupby as date wifi
    df_icao_code_wifi = pd.DataFrame(df_wifi_top3.groupby(['icao_code'],as_index=False).agg({'avg_utilization_min':('sum')}))
    df_large3_wifi = df_wifi_top3.nlargest(3, "avg_utilization_min") 
    #groupby as date sanitizer
    df_icao_code_sanitizer = pd.DataFrame(df_sanitizer_top3.groupby(['icao_code'],as_index=False).agg({'avg_dispenses':('sum')}))
    df_large3_sanitizer = df_sanitizer_top3.nlargest(4, "avg_dispenses") 
    #groupby as date kiosk
    df_icao_code_kiosk = pd.DataFrame(df_kiosk_top3.groupby(['icao_code'],as_index=False).agg({'pct_utilization':('sum')}))
    df_large3_kiosk = df_kiosk_top3.nlargest(3, "pct_utilization") 
    #groupby as date CB
    df_icao_code_CB = pd.DataFrame(df_conveyor_top3.groupby(['icao_code'],as_index=False).agg({'pct_utilization':('sum')}))
    df_large3_CB = df_conveyor_top3.nlargest(3, "pct_utilization") 
    fig = make_subplots(rows=7, cols=1)
    #boarding
    fig.add_trace(
        go.Bar(x=df_large3_boarding.icao_code, y=df_large3_boarding.pct_utilization,hovertext=df_boarding_top3['rank'],name=" Average utilization of used seats"),
        row=1, col=1
    )
    #trolley
    fig.add_trace(
        go.Bar(x=df_large3_trolley.icao_code, y=df_large3_trolley.pct_utilization,hovertext=df_trolley_top3['rank'],name=" Average utilization of Trolley"),
        row=2, col=1
    )
    #wifi
    fig.add_trace(
        go.Bar(x=df_large3_wifi.icao_code, y=df_large3_wifi.avg_utilization_min,name=" Average utilization min of Wifi"),
        row=3, col=1
    )

    #parking
    fig.add_trace(
        go.Bar(x=df_large3_parking.icao_code, y=df_large3_parking.pct_utilization,hovertext=df_parking_top3['rank'],name=" Percenatge Utilization of parking"),
        row=4, col=1
    )
    #cb
    fig.add_trace(
        go.Bar(x=df_large3_CB.icao_code, y=df_large3_CB.pct_utilization,hovertext=df_conveyor_top3['rank'],name=" Percenatge Utilization of CB"),
        row=5, col=1
    )
    #sanitizer
    fig.add_trace(
        go.Bar(x=df_large3_sanitizer.icao_code, y=df_large3_sanitizer.avg_dispenses,hovertext=df_sanitizer_top3['rank'],name=" Average dispenses of Sanitizer"),
        row=6, col=1
    )
    #kiosk
    fig.add_trace(
        go.Bar(x=df_large3_kiosk.icao_code, y=df_large3_kiosk.pct_utilization,hovertext=df_kiosk_top3['rank'],name=" Percenatge Utilization of checkInKiosk"),
        row=7, col=1
    )
    fig.update_xaxes(title_text="icao_code", row=1, col=1)
    fig.update_yaxes(title_text=" Utilization ", row=1, col=1)
    fig.update_xaxes(title_text="icao_code", row=2, col=1)
    fig.update_yaxes(title_text="Utilization ", row=2, col=1)
    fig.update_xaxes(title_text="icao_code", row=3, col=1)
    fig.update_yaxes(title_text="Avg Utilization", row=3, col=1)
    fig.update_xaxes(title_text="icao_code", row=4, col=1)
    fig.update_yaxes(title_text="Utilization", row=4, col=1)
    fig.update_xaxes(title_text="icao_code", row=5, col=1)
    fig.update_yaxes(title_text="Utilization", row=5, col=1)
    fig.update_xaxes(title_text="icao_code", row=6, col=1)
    fig.update_yaxes(title_text="Average dispenses", row=6, col=1)
    fig.update_xaxes(title_text="icao_code", row=7, col=1)
    fig.update_yaxes(title_text="Utilization", row=7, col=1)
    plot_div1 = fig.update_layout(height=1200, width=1270, title_text="Services of Airport")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div

