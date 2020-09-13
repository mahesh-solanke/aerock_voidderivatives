import pandas as pd
import psycopg2
from pymongo import MongoClient
engine=psycopg2.connect(host ='localhost', dbname='aerock', user='postgres', password='sih2020', port='5432')
df_thr=pd.read_sql_query('SELECT dt.id, sensor_type, sensor_threshold, threshold_value_high, capacity, airfac_id, threshold_value_low, icao_code, af.fac_id FROM public.dashboard_threshold as dt join dashboard_airportfacility as af on dt.airfac_id=af.id join dashboard_airport as da on af.air_id=da.id where af.fac_id=4;',con=engine)
#df_thr
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = mongo_client.rawdata
rawmap  = db.sanitizermap
rawsan = db.nSanitizer
#print ("total docs in collection:", rawmap.count_documents( {} ))
#print ("total docs in collection:", rawsan.count_documents( {} ))
mongodocs_map = list(rawmap.find())
mongodocs_san = list(rawsan.find())

series_obj = pd.Series({"a key":"a value"})
series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
df_map = pd.DataFrame(columns=[])
df_raw = pd.DataFrame(columns=[])

for num, doc in enumerate( mongodocs_map ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )

    # append the MongoDB Series obj to the DataFrame obj
    df_map = df_map.append( series_obj )

for num, doc in enumerate( mongodocs_san ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])

    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )

    # append the MongoDB Series obj to the DataFrame obj
    df_raw = df_raw.append( series_obj )

del df_map['_id']
del df_raw['_id']
df_merge=pd.merge(df_map, df_raw)
#df_merge

df_merge['datetime'] = pd.to_datetime(df_merge['datetime'])
df_merge['hour'] = df_merge['datetime'].dt.hour
df_merge['date'] = df_merge['datetime'].dt.strftime('%Y-%m-%d')
#df_merge

df_mergethresh=pd.merge(df_merge, df_thr[["sensor_threshold", "threshold_value_high", "capacity", "threshold_value_low", "icao_code"]], on="icao_code", how="left")
#df_mergethresh

df_mergethresh['dispense'] = df_mergethresh['distance'] < df_mergethresh['sensor_threshold']
df_mergethresh['dispense'] = df_mergethresh['dispense'].astype(int)
#df_mergethresh.to_excel('a.xlsx')
df_mergethresh = df_mergethresh.rename(columns={"dispense": "count_dispenses", 'containerid' : 'no_of_containers'})
#df_mergethresh

# top3 utilization
top3util=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'count_dispenses':('sum'),"no_of_containers": pd.Series.nunique}))
top3util['avg_dispenses']= top3util['count_dispenses'] / top3util['no_of_containers']
top3util['rank']=top3util.groupby(['date','icao_code'])['avg_dispenses'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<2')
del top3util['count_dispenses'], top3util['no_of_containers'], top3util['rank']
top3util['rank']=top3util.groupby(['date'])['avg_dispenses'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date'] = pd.to_datetime(top3util['date'])
top3util['date'] = top3util['date'].dt.strftime('%Y-%m-%d')
top3util.insert(1, 'newid', range(0, 0 + len(top3util)))
top3util['date1'] = top3util['date'].astype(str)
top3util['newid'] = top3util['newid'].astype(str)
top3util['_id'] = top3util['date1']+top3util['newid']
del top3util['date1'],top3util['newid']
#print(top3util)
#top3util.dtypes

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_sntop3utilization']
collectionInfo = db.api_sntop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)

# all daily metric (average utilization of all containers in each areaid)
df_calcday=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','areaid','capacity'],as_index=False).agg({'count_dispenses':('sum'),"no_of_containers": pd.Series.nunique}))
df_calcday['refills']=(df_calcday['count_dispenses']/df_calcday['capacity']).astype(int)
df_calcday['avg_dispenses']= df_calcday['count_dispenses'] / df_calcday['no_of_containers']
df_calcday['date'] = pd.to_datetime(df_calcday['date'])
del df_calcday['capacity']
top3util['date'] = pd.to_datetime(top3util['date'])
df_calcday['date'] = df_calcday['date'].dt.strftime('%Y-%m-%d')
df_calcday['date1'] = df_calcday['date'].astype(str)
df_calcday['_id'] = df_calcday['date1']+df_calcday['icao_code']+df_calcday['areaid']
del df_calcday['date1']
#print(df_calcday)
#df_calcday.dtypes

dict_sncalcday=pd.DataFrame.to_dict(df_calcday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_sncalcday']
collectionInfo = db.api_sncalcday
ids=[data.pop("_id") for data in dict_sncalcday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_sncalcday)]
response = collectionInfo.bulk_write(operations)  
print(response)

df_runningdata = pd.DataFrame(df_mergethresh[['icao_code','datetime','areaid','no_of_containers','count_dispenses','threshold_value_high','threshold_value_low']])
df_runningdata['date']= df_runningdata['datetime'].dt.date
df_hold=pd.DataFrame(df_runningdata.groupby(['icao_code','areaid','no_of_containers','date','datetime','threshold_value_high','threshold_value_low'],as_index=False).agg({'count_dispenses':('sum')}))
#df_hold.to_excel("hold.xlsx")

df_demoalert = pd.DataFrame(columns=[])
uniqueicao=list(df_hold['icao_code'].unique())
for i in uniqueicao: 
    df_air = pd.DataFrame(columns=[])
    df_air=df_hold[df_hold.icao_code==i]
    
    uniquearea=list(df_air['areaid'].unique())
    for k in uniquearea: 
        df_area = pd.DataFrame(columns=[])
        df_area=df_air[df_air.areaid==k]

        uniquecont=list(df_area['no_of_containers'].unique())
        for m in uniquecont: 
            df_cont = pd.DataFrame(columns=[])
            df_cont=df_area[df_area.no_of_containers==m]

            uniquedate=list(df_cont['date'].unique())
            for l in uniquedate:    
                df_date = pd.DataFrame(columns=[])
                df_date=df_cont[df_cont.date==l]

                ls_dispense = []
                cumsum_dispense = 0
                last_reset = 0
                for _, row in df_date.iterrows():
                    cumsum_dispense = cumsum_dispense + row.count_dispenses
                    ls_dispense.append(cumsum_dispense)
                    if cumsum_dispense >= row.threshold_value_high: #and cumsum_inuse > 0.2*last_reset:
                        last_reset = cumsum_dispense
                        cumsum_dispense = 0
                
                df_date['cumsum_dispense']=ls_dispense
                df_demoalert = df_demoalert.append(df_date)
                #df_demoalert.to_excel('df_demoalert.xlsx')        

df_demoalert.loc[df_demoalert['cumsum_dispense'] <= df_demoalert['threshold_value_low'], 'state'] = 'ORANGE'
df_demoalert.loc[df_demoalert['cumsum_dispense'] >= df_demoalert['threshold_value_high'] , 'state'] = 'RED'
#df_demoalert.to_excel('state.xlsx')

df_excporg = pd.DataFrame(columns=[])
df_excpred = pd.DataFrame(columns=[])
df_excporg = df_demoalert[df_demoalert['state']=='ORANGE']
df_excpred = df_demoalert[df_demoalert['state']=='RED']
df_excporg=df_excporg.append(df_excpred, ignore_index=True)
df_excporg=df_excporg.rename(columns={'cumsum_dispense':'actual_value','no_of_containers':'deviceid','datetime': 'event_time','threshold_value_high':'high_threshold','threshold_value_low':'low_threshold'})
df_excporg['facility']='Sanitizer'
del df_excporg['count_dispenses'],df_excporg['date']
df_excporg['_id'] = df_excporg['icao_code']+df_excporg['facility']+df_excporg['deviceid']+df_excporg['event_time'].astype(str)
#df_excporg.to_excel('afterallopr.xlsx')
#print(df_excporg)

import datetime as dt
df_excporg['event_time']=(df_excporg['event_time'] - dt.datetime(1970,1,1)).dt.total_seconds()
#print(df_excporg)
#df_excporg.to_excel('afterallopr.xlsx')

dict_calcexcep=pd.DataFrame.to_dict(df_excporg, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['sihfinal']
collection_currency = db['api_exception_details']
collectionInfo = db.api_exception_details
ids=[data.pop("_id") for data in dict_calcexcep]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_calcexcep)]
response = collectionInfo.bulk_write(operations)  
print(response)

# all hourly metric
df_calchour=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','areaid','hour'],as_index=False).agg({'count_dispenses':('sum'),"no_of_containers": pd.Series.nunique}))
df_calchour['avg_dispenses']= df_calchour['count_dispenses'] / df_calchour['no_of_containers']
df_calchour['date'] = pd.to_datetime(df_calchour['date'])
df_calchour['date'] = df_calchour['date'].dt.strftime('%Y-%m-%d')
df_calchour['date1'] = df_calchour['date'].astype(str)
df_calchour['hour1'] = df_calchour['hour'].astype(str)
df_calchour['_id'] = df_calchour['date1']+df_calchour['icao_code']+df_calchour['hour1']+df_calchour['areaid']
del df_calchour['date1'],df_calchour['hour1']
#print(df_calchour)
#df_calchour.to_excel('hour.xlsx')

dict_sncalchour=pd.DataFrame.to_dict(df_calchour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_sncalchour']
collectionInfo = db.api_sncalchour
ids=[data.pop("_id") for data in dict_sncalchour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_sncalchour)]
response = collectionInfo.bulk_write(operations)  
print(response)