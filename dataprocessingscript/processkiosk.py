import pandas as pd
import numpy as np
from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.kioskraw
rawmapping=db.kioskmap
#print ("total docs in collection:", rawdata.count_documents( {} ))
#print ("total docs in collection:", rawmapping.count_documents( {} ))

mongodocs_kiosk = list(rawdata.find())
mongodocs_mapping = list(rawmapping.find())

series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))
series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

df_kiosk = pd.DataFrame(columns=[])
df_mapping = pd.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_kiosk ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_kiosk = df_kiosk.append( series_obj )

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

del df_kiosk['_id']
del df_mapping['_id']
#print(df_kiosk)
#print(df_mapping)

df_merge=pd.merge(df_kiosk,df_mapping)
df_merge['value']=df_merge['value'].astype(int)

df_merge['datetime']= pd.to_datetime(df_merge['datetime'])
df_merge['hour']=df_merge['datetime'].dt.hour
df_merge['date']= df_merge['datetime'].dt.date

df_merge.loc[df_merge['value'] == 1, 'used'] = 1
df_merge.loc[df_merge['value'] != 1, 'used'] = 0
df_merge.loc[df_merge['value'] == 0, 'notused'] = 1
df_merge.loc[df_merge['value'] != 0, 'notused'] = 0
df_merge['used']=df_merge['used'].astype(int)
df_merge['notused']=df_merge['notused'].astype(int)
#print(df_merge)

#hourwise
#df_merge = df_merge.rename(columns={"used": "count_of_visits", 'deviceid' : 'count_of_devices'})
df_kioskhour=pd.DataFrame(df_merge.groupby(['date','icao_code','hour'],as_index=False).agg({'count_of_visits':('sum'),'count_of_devices':pd.Series.nunique}))
df_kioskhour['pct_utilization']= df_kioskhour['count_of_visits'] / df_kioskhour['count_of_devices'] /30 * 100
df_kioskhour['date']=pd.to_datetime(df_kioskhour['date'])
#print(df_kioskhour)

df_kioskhour['date1'] = df_kioskhour['date'].astype(str)
df_kioskhour['hour1'] = df_kioskhour['hour'].astype(str)
df_kioskhour['_id'] = df_kioskhour['date1']+df_kioskhour['icao_code']+df_kioskhour['hour1']
del df_kioskhour['date1'],df_kioskhour['hour1']
#print(df_kioskhour)

#daywise
#df_merge = df_merge.rename(columns={"used": "count_of_visits", 'deviceid' : 'count_of_devices'})
df_kioskday=pd.DataFrame(df_merge.groupby(['date','icao_code'],as_index=False).agg({'count_of_visits':('sum'),'count_of_devices':pd.Series.nunique}))
df_kioskday['pct_utilization']= df_kioskday['count_of_visits'] / df_kioskday['count_of_devices'] /1800 * 100
df_kioskday['date']=pd.to_datetime(df_kioskday['date'])
#print(df_kioskday)

df_kioskday['date1'] = df_kioskday['date'].astype(str)
df_kioskday['_id'] = df_kioskday['date1']+df_kioskday['icao_code']
del df_kioskday['date1']
#print(df_kioskday)

# top3 utilization
top3util=pd.DataFrame(df_merge.groupby(['date','icao_code','hour'],as_index=False).agg({'count_of_visits':('sum'),'count_of_devices':pd.Series.nunique}))
top3util['pct_utilization']= top3util['count_of_visits'] / top3util['count_of_devices'] /30 * 100
top3util['rank']=top3util.groupby(['date','icao_code'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date']=pd.to_datetime(top3util['date'])
top3util['date']=pd.to_datetime(top3util['date'].dt.date)
del top3util['count_of_visits'], top3util['count_of_devices']
#print(top3util)

top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
#print(top3util)

dict_kioskday=pd.DataFrame.to_dict(df_kioskday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_kioskday']
collectionInfo = db.api_kioskday
ids=[data.pop("_id") for data in dict_kioskday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_kioskday)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_kioskhour=pd.DataFrame.to_dict(df_kioskhour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_kioskhour']
collectionInfo = db.api_kioskhour
ids=[data.pop("_id") for data in dict_kioskhour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_kioskhour)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_kiosktop3utilization']
collectionInfo = db.api_kiosktop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)