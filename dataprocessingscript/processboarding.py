import pandas as pd
import psycopg2
from pymongo import MongoClient
engine=psycopg2.connect(host ='localhost', dbname='aerock', user='postgres', password='sih2020', port='5432')

df_threshold=pd.read_sql_query('SELECT dt.id, sensor_type, sensor_threshold, threshold_value_high, capacity, airfac_id, threshold_value_low, icao_code, af.fac_id FROM public.dashboard_threshold as dt join dashboard_airportfacility as af on dt.airfac_id=af.id join dashboard_airport as da on af.air_id=da.id where af.fac_id=1;',con=engine)
#df_threshold

# build a new client instance of MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.nboardinggates
rawmapping=db.boardingmap
#print ("total docs in collection:", rawdata.count_documents( {} ))
#print ("total docs in collection:", rawmapping.count_documents( {} ))

# make an API call to the MongoDB server using a Collection object
mongodocs_boarding = list(rawdata.find())
mongodocs_mapping = list(rawmapping.find())

series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))

series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

# create an empty DataFrame obj for storing Series objects
df_boarding = pd.DataFrame(columns=[])
df_mapping = pd.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_boarding ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )

    # append the MongoDB Series obj to the DataFrame obj
    df_boarding = df_boarding.append( series_obj )

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_mapping ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )

    # append the MongoDB Series obj to the DataFrame obj
    df_mapping = df_mapping.append( series_obj )

del df_boarding['_id']
#print(df_boarding)
del df_mapping['_id']
#print(df_mapping)
df1=pd.merge(df_boarding,df_mapping)
#df1

df1['datetime'] = pd.to_datetime(df1['date and time'])
#df1['Month'] = pd.DatetimeIndex(df1['datetime']).month
df1['date'] = df1['datetime'].dt.strftime('%Y-%m-%d')
df1['hour'] = df1['datetime'].dt.hour
del df1['date and time']
#del df1['datetime']
#print(df1)
#df1.to_excel('aaa.xlsx')

df_mergethresh=pd.merge(df1, df_threshold[["sensor_threshold", "threshold_value_high", "capacity", "threshold_value_low", "icao_code"]], on="icao_code", how="left")
#df_mergethresh.to_excel('a.xlsx')

df_mergethresh.loc[df_mergethresh['value'] > df_mergethresh['sensor_threshold'], 'inuse'] = 1
df_mergethresh.loc[df_mergethresh['value'] <= df_mergethresh['sensor_threshold'], 'inuse'] = 0
df_mergethresh.loc[df_mergethresh['value'] <= df_mergethresh['sensor_threshold'], 'notinuse'] = 1
df_mergethresh.loc[df_mergethresh['value'] > df_mergethresh['sensor_threshold'], 'notinuse'] = 0
#df_mergethresh.to_excel('a.xlsx')
#df_mergethresh

# top 3 utilization
top3util=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum'),'seats': ('count')}))
top3util['pct_utilization']=top3util['inuse'] / top3util['seats'] * 100
top3util['rank']=top3util.groupby(['date','icao_code'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<2')
del top3util['inuse'],top3util['notinuse'],top3util['seats'],top3util['rank']
top3util['rank']=top3util.groupby(['date'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date'] = pd.to_datetime(top3util['date'])
top3util['date'] = top3util['date'].dt.strftime('%Y-%m-%d')
top3util.insert(1, 'newid', range(0, 0 + len(top3util)))
#top3util
top3util['date1'] = top3util['date'].astype(str)
top3util['newid'] = top3util['newid'].astype(str)
top3util['_id'] = top3util['date1']+top3util['newid']
del top3util['date1'],top3util['newid']
#print(top3util)

dict_boardingtop3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_boardingtop3util']
collectionInfo = db.api_boardingtop3util
ids=[data.pop("_id") for data in dict_boardingtop3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_boardingtop3util)]
response = collectionInfo.bulk_write(operations)  
print(response)

# all metrics of day
allmetricday=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum'),'seats': ('count')}))
allmetricday['pct_utilization']=allmetricday['inuse'] / allmetricday['seats'] * 100
allmetricday['date'] = pd.to_datetime(allmetricday['date'])
allmetricday['date'] = allmetricday['date'].dt.strftime('%Y-%m-%d')
allmetricday=allmetricday.rename(columns={"inuse": "count_used","notinuse":"count_unused","seats":"total_count"})
allmetricday
allmetricday['date1'] = allmetricday['date'].astype(str)
allmetricday['_id'] = allmetricday['date1']+allmetricday['icao_code']
del allmetricday['date1']
#allmetricday

dict_boardingday=pd.DataFrame.to_dict(allmetricday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_boardingday']
collectionInfo = db.api_boardingday
ids=[data.pop("_id") for data in dict_boardingday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_boardingday)]
response = collectionInfo.bulk_write(operations)  
print(response)

allmetrichour=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','hour'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum'),'seats': ('count')}))
allmetrichour['pct_utilization']=allmetrichour['inuse'] / allmetrichour['seats'] * 100
allmetrichour=allmetrichour.rename(columns={"inuse": "count_used","notinuse":"count_unused","seats":"total_count"})
allmetrichour['date'] = pd.to_datetime(allmetrichour['date'])
allmetrichour['date'] = allmetrichour['date'].dt.strftime('%Y-%m-%d')
#allmetrichour
allmetrichour['date1'] = allmetrichour['date'].astype(str)
allmetrichour['hour1'] = allmetrichour['hour'].astype(str)
allmetrichour['_id'] = allmetrichour['date1']+allmetrichour['icao_code']+allmetrichour['hour1']
del allmetrichour['date1'],allmetrichour['hour1']
#allmetrichour

dict_boardinghour=pd.DataFrame.to_dict(allmetrichour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_boardinghour']
collectionInfo = db.api_boardinghour
ids=[data.pop("_id") for data in dict_boardinghour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_boardinghour)]
response = collectionInfo.bulk_write(operations)  
print(response)

df_runningdata = pd.DataFrame(df_mergethresh[['icao_code','seats','datetime','inuse','notinuse','threshold_value_high','threshold_value_low']])
df_runningdata['date']= df_runningdata['datetime'].dt.date
df_hold=pd.DataFrame(df_runningdata.groupby(['icao_code','date','datetime','threshold_value_high','threshold_value_low'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum')}))
#df_hold.to_excel('hold.xlsx')

df_demoalert = pd.DataFrame(columns=[])
uniqueicao=list(df_hold['icao_code'].unique())
for i in uniqueicao:    
    df_air = pd.DataFrame(columns=[])
    df_air=df_hold[df_hold.icao_code==i]

    uniquedate=list(df_air['date'].unique())
    for k in uniquedate:    
        df_date = pd.DataFrame(columns=[])
        df_date=df_air[df_air.date==k]

        ls_inuse = []
        ls_notinuse = []# store result
        ls_percent = []
        cumsum_inuse = 0
        cumsum_notinuse = 0
        cumsum_percent = 0
        last_reset = 0
        for _, row in df_date.iterrows():
            cumsum_inuse = cumsum_inuse + row.inuse
            cumsum_notinuse = cumsum_notinuse+row.notinuse
            cumsum_percent = (cumsum_inuse/(cumsum_inuse+cumsum_notinuse)*100)
            ls_inuse.append(cumsum_inuse)
            ls_notinuse.append(cumsum_notinuse)
            ls_percent.append(cumsum_percent)
            if cumsum_percent >= row.threshold_value_high: #and cumsum_inuse > 0.2*last_reset:
                last_reset = cumsum_percent
                cumsum_inuse = 0
                cumsum_notinuse = 0
                cumsum_percent = 0

        df_date['cumsum_inuse']=ls_inuse
        df_date['cumsum_notinuse']=ls_notinuse
        df_date['cumsum_percent']=ls_percent
        df_demoalert = df_demoalert.append(df_date)
        #df_demoalert.to_excel('df_demoalert.xlsx')        

df_demoalert.loc[df_demoalert['cumsum_percent'] <= df_demoalert['threshold_value_low'], 'state'] = 'ORANGE'
df_demoalert.loc[df_demoalert['cumsum_percent'] >= df_demoalert['threshold_value_high'] , 'state'] = 'RED'
#df_demoalert.to_excel('state.xlsx')

df_excporg = df_demoalert[df_demoalert['state']=='ORANGE']
df_excpred = df_demoalert[df_demoalert['state']=='RED']
df_excporg=df_excporg.append(df_excpred, ignore_index=True)
df_excporg=df_excporg.rename(columns={'datetime': 'event_time','cumsum_percent':'actual_value','threshold_value_high':'high_threshold','threshold_value_low':'low_threshold'})
df_excporg['facility']='Boarding Gate'
df_excporg['deviceid']=''
df_excporg['areaid']=''
del df_excporg['inuse'],df_excporg['notinuse'],df_excporg['cumsum_inuse'],df_excporg['cumsum_notinuse']
#print(df_excporg)

df_excporg['_id'] = df_excporg['icao_code']+df_excporg['facility']+df_excporg['event_time'].astype(str)
del df_excporg['date']
#df_excporg

import datetime as dt
df_excporg['event_time']=(df_excporg['event_time'] - dt.datetime(1970,1,1)).dt.total_seconds()
#df_excporg.to_excel('afterallopr.xlsx')

dict_exceptions=pd.DataFrame.to_dict(df_excporg, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['sihfinal']#aerockdb
collection_currency = db['api_exception_details']
collectionInfo = db.api_exception_details
ids=[data.pop("_id") for data in dict_exceptions]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_exceptions)]
response = collectionInfo.bulk_write(operations)  
print(response)