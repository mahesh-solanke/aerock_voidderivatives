import pandas as pd
import psycopg2
from pymongo import MongoClient
engine=psycopg2.connect(host ='localhost', dbname='aerock', user='postgres', password='sih2020', port='5432')
df_thr=pd.read_sql_query('SELECT dt.id, sensor_type, threshold_type, threshold_value_high, capacity, airfac_id, threshold_value_low, icao_code, af.fac_id FROM public.dashboard_threshold as dt join dashboard_airportfacility as af on dt.airfac_id=af.id join dashboard_airport as da on af.air_id=da.id where af.fac_id=4;',con=engine)
#print(df_thr)
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

db = mongo_client.rawdata
rawmap  = db.sanitizermap
rawsan = db.sanitize
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

df_merge['datetime1'] = pd.to_datetime(df_merge['datetime'])
df_merge['hour'] = df_merge['datetime1'].dt.hour
df_merge['date']=df_merge['datetime1'].dt.date

thresholddist=25
df_merge['dispense'] = df_merge['distance'] < thresholddist
df_merge['dispense'] = df_merge['dispense'].astype(int)

capacity = df_thr.loc[:, 'capacity'] 
capacity=int(capacity)
df_merge = df_merge.rename(columns={"dispense": "count_dispenses", 'containerid' : 'no_of_containers'})
df_calchour=pd.DataFrame(df_merge.groupby(['date','icao_code','areaid','hour'],as_index=False).agg({'count_dispenses':('sum'),"no_of_containers": pd.Series.nunique}))
df_calchour['refills']=(df_calchour['count_dispenses']/capacity).astype(int)
df_calchour['avg_dispenses']= df_calchour['count_dispenses'] / df_calchour['no_of_containers']
df_calchour['date'] = pd.to_datetime(df_calchour['date'])

df_calchour['date1'] = df_calchour['date'].astype(str)
df_calchour['hour1'] = df_calchour['hour'].astype(str)
df_calchour['_id'] = df_calchour['date1']+df_calchour['icao_code']+df_calchour['hour1']+df_calchour['areaid']
del df_calchour['date1'],df_calchour['hour1']
#print(df_calchour)

# top3 utilization
top3util=pd.DataFrame(df_merge.groupby(['date','icao_code','hour','areaid'],as_index=False).agg({'count_dispenses':('sum'),"no_of_containers": pd.Series.nunique}))
top3util['avg_dispenses']= top3util['count_dispenses'] / top3util['no_of_containers']
top3util['rank']=top3util.groupby(['date','icao_code'])['avg_dispenses'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date']=pd.to_datetime(top3util['date'])
top3util['date']=pd.to_datetime(top3util['date'].dt.date)
del top3util['count_dispenses'], top3util['no_of_containers']

top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
#print(top3util)

capacity = df_thr.loc[:, 'capacity'] 
capacity=int(capacity)
df_calcday=pd.DataFrame(df_merge.groupby(['date','icao_code','areaid'],as_index=False).agg({'count_dispenses':('sum'),"no_of_containers": pd.Series.nunique}))
df_calcday['refills']=(df_calcday['count_dispenses']/capacity).astype(int)
df_calcday['avg_dispenses']= df_calcday['count_dispenses'] / df_calcday['no_of_containers']
df_calcday['date'] = pd.to_datetime(df_calcday['date'])

df_calcday['date1'] = df_calcday['date'].astype(str)
df_calcday['_id'] = df_calcday['date1']+df_calcday['icao_code']+df_calcday['areaid']
del df_calcday['date1']
#print(df_calcday)

capacity = df_thr.loc[:, 'capacity'] 
capacity=int(capacity)
redthreshold = df_thr.loc[:, 'threshold_value_high'] 
redthreshold=int(redthreshold)
orangethreshold = df_thr.loc[:, 'threshold_value_low'] 
orangethreshold=int(orangethreshold)
df_temp=pd.DataFrame(df_merge.groupby(['date','icao_code','areaid','no_of_containers'],as_index=False).agg({'count_dispenses':('sum'),'datetime':('max')}))
df_temp['date'] = pd.to_datetime(df_temp['date'])
df_temp['actual_value']= df_temp['count_dispenses'] % capacity
df_temp.loc[df_temp['actual_value'] >= orangethreshold, 'state'] = 'ORANGE'
df_temp.loc[df_temp['actual_value'] >= redthreshold , 'state'] = 'RED'

df_calcexcepor = pd.DataFrame(columns=[])
df_calcexcepre = pd.DataFrame(columns=[])
df_calcexcepor = df_temp[df_temp['state']=='ORANGE']
df_calcexcepre = df_temp[df_temp['state']=='RED']
df_calcexcepor=df_calcexcepor.append(df_calcexcepre, ignore_index=True)
df_calcexcepor=df_calcexcepor.rename(columns={'datetime': 'event_time', 'no_of_containers' : 'deviceid'})
df_calcexcepor['facility']='sanitizer'
df_calcexcepor['threshold']='100'
del df_calcexcepor['count_dispenses'],df_calcexcepor['date']
#print(df_calcexcepor)

df_exception = pd.DataFrame(columns=[])
df_exception['date1'] = df_exception['event_time'].astype(str)
df_exception['_id'] = df_exception['date1']+df_exception['icao_code']+df_exception['areaid']+df_exception['deviceid']
del df_exception['date1']
#print(df_exception)

dict_calcexcep=pd.DataFrame.to_dict(df_exception, orient='records')
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

dict_sncalcday=pd.DataFrame.to_dict(df_calcday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['sihfinal']
collection_currency = db['api_sncalcday']
collectionInfo = db.api_sncalcday
ids=[data.pop("_id") for data in dict_sncalcday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_sncalcday)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_sncalchour=pd.DataFrame.to_dict(df_calchour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['sihfinal']
collection_currency = db['api_sncalchour']
collectionInfo = db.api_sncalchour
ids=[data.pop("_id") for data in dict_sncalchour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_sncalchour)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['sihfinal']
collection_currency = db['api_sntop3utilization']
collectionInfo = db.api_sntop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)
