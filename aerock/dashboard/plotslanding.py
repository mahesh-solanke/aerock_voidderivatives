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


def top3(date,airport_code):
    boarding_top3= db.api_boardtop3utilization
    trolley_top3 = db.api_trolleytop3utilization
    wifi_top3 = db.api_wifitop3utilization
    feedback_top3=db.api_fbtop3utilization
    parking_top3=db.api_parkingtop3utilization
    conveyor_top3=db.api_cbtop3utilization
    sanitizer_top3=db.api_sntop3utilization
    kiosk_top3=db.api_kiosktop3utilization
    mongodocs_boarding_top3 = list(boarding_top3.find())
    mongodocs_trolley_top3 = list(trolley_top3.find())
    mongodocs_wifi_top3 = list(wifi_top3.find())
    mongodocs_feedback_top3= list(feedback_top3.find())
    mongodocs_parking_top3= list(parking_top3.find())
    mongodocs_conveyor_top3= list(conveyor_top3.find())
    mongodocs_sanitizer_top3= list(sanitizer_top3.find())
    mongodocs_kiosk_top3= list(kiosk_top3.find())
    series_obj = pd.Series({"a key":"a value"})
    series_obj = pd.Series( {"one":"index"} )
    series_obj.index = [ "one" ]
    df_boarding_top3 = pd.DataFrame(columns=[])
    df_trolley_top3 = pd.DataFrame(columns=[])
    df_wifi_top3 = pd.DataFrame(columns=[])
    df_feedback_top3 = pd.DataFrame(columns=[])
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
    for num, doc in enumerate( mongodocs_feedback_top3 ):
        # convert ObjectId() to str
        doc["_id"] = str(doc["_id"])
        # get document _id from dict
        doc_id = doc["_id"]
        # create a Series obj from the MongoDB dict
        series_obj = pd.Series( doc, name=doc_id )
        # append the MongoDB Series obj to the DataFrame obj
        df_feedback_top3 = df_feedback_top3.append( series_obj )
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
    del df_boarding_top3['_id'],df_trolley_top3['_id'],df_wifi_top3['_id'],df_feedback_top3['_id'],df_parking_top3['_id'],df_conveyor_top3['_id'],df_sanitizer_top3['_id'],df_kiosk_top3['_id']
    df_boarding_top3_date = df_boarding_top3[df_boarding_top3.date == date]
    df_wifi_top3_date= df_wifi_top3[df_wifi_top3.date == date]
    df_trolley_top3_date= df_trolley_top3[df_trolley_top3.date == date]
    df_icao_code_top3 = df_feedback_top3[df_feedback_top3.icao_code == airport_code ]
    df_parking_top3_date= df_parking_top3[df_parking_top3.date == date]
    df_conveyor_top3_date= df_conveyor_top3[df_conveyor_top3.date == date]
    df_sanitizer_top3_date= df_sanitizer_top3[df_sanitizer_top3.date == date]
    df_kiosk_top3_date= df_kiosk_top3[df_kiosk_top3.date == date]
    fig = make_subplots(rows=8, cols=1)
    #boarding
    fig.add_trace(
        go.Bar(x=df_boarding_top3_date.icao_code, y=df_boarding_top3_date.pct_utilization,hovertext=df_boarding_top3['rank'],name=" Average utilization of used seats<br>x-axis :icao_code<br>y-aixs : percentage utilization<br>_______________________________"),
        row=1, col=1
    )
    #trolley
    fig.add_trace(
        go.Bar(x=df_trolley_top3_date.icao_code, y=df_trolley_top3_date.pct_utilization,hovertext=df_trolley_top3['rank'],name=" Average utilization of Wifi<br>x-axis : service_id<br>y-aixs : Percentage utilization<br>_______________________________"),
        row=2, col=1
    )
    #wifi
    fig.add_trace(
        go.Bar(x=df_wifi_top3_date.icao_code, y=df_wifi_top3_date.avg_utilization_min,hovertext=df_wifi_top3['rank'],name=" Average utilization of Wifi<br>x-axis :icao_code <br>y-aixs :  Average utilization_min<br>_______________________________"),
        row=3, col=1
    )
    #feedback
    fig.add_trace(
        go.Bar(x=df_feedback_top3.icao_code, y=df_feedback_top3.rating_for_service,hovertext=df_feedback_top3['rank'], name="feedback rating of services<br>x-axis : icao_code<br>y-aixs : rating for service<br>_______________________________"),
        row=4, col=1
    )
    #parking
    fig.add_trace(
        go.Bar(x=df_parking_top3_date.icao_code, y=df_parking_top3_date.pct_utilization,hovertext=df_parking_top3['rank'],name=" Percenatge Utilization<br>x-axis : icao_code <br>y-aixs :  Percenatge utilization_min<br>_______________________________"),
        row=5, col=1
    )
    #cb
    fig.add_trace(
        go.Bar(x=df_conveyor_top3_date.icao_code, y=df_conveyor_top3_date.pct_utilization,hovertext=df_conveyor_top3['rank'],name=" Percenatge Utilization<br>x-axis : icao_code <br>y-aixs :  Percenatge utilization_min<br>_______________________________"),
        row=6, col=1
    )
    #sanitizer
    fig.add_trace(
        go.Bar(x=df_sanitizer_top3_date.icao_code, y=df_sanitizer_top3_date.avg_dispenses,hovertext=df_sanitizer_top3['rank'],name=" Average dispenses<br>x-axis : icao_code <br>y-aixs :  avg_dispenses<br>_______________________________"),
        row=7, col=1
    )
    #kiosk
    fig.add_trace(
        go.Bar(x=df_kiosk_top3_date.icao_code, y=df_kiosk_top3_date.pct_utilization,hovertext=df_kiosk_top3['rank'],name=" Percenatge Utilization<br>x-axis : icao_code <br>y-aixs :  Percenatge utilization_min<br>_______________________________"),
        row=8, col=1
    )
    plot_div1 = fig.update_layout(height=800, width=1270, title_text="Services of Airport")
    plot_div= plot(plot_div1, output_type='div', include_plotlyjs=False)
    return plot_div



