import pandas as pd
import numpy as np
from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.parkingraw
rawmapping=db.parkingmap
#print ("total docs in collection:", rawdata.count_documents( {} ))
#print ("total docs in collection:", rawmapping.count_documents( {} ))

# make an API call to the MongoDB server using a Collection object
mongodocs_parking = list(rawdata.find())
mongodocs_mapping = list(rawmapping.find())
series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))

series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

# create an empty DataFrame obj for storing Series objects
df_parking = pd.DataFrame(columns=[])
df_mapping = pd.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_parking ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_parking = df_parking.append( series_obj )

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

del df_parking['_id']
del df_mapping['_id']

df_merge=pd.merge(df_parking,df_mapping)
#print(df_merge)

#threshold=5
df_merge['datetime']= pd.to_datetime(df_merge['datetime'])
df_merge['hour']=df_merge['datetime'].dt.hour
df_merge['date']= df_merge['datetime'].dt.date
df_merge['value']=df_merge['value'].astype(int)
#print(df_merge)

df_merge.loc[df_merge['value'] == 1, 'used'] = 1
df_merge.loc[df_merge['value'] != 1, 'used'] = 0
df_merge.loc[df_merge['value'] == 0, 'notused'] = 1
df_merge.loc[df_merge['value'] != 0, 'notused'] = 0
df_merge['used']=df_merge['used'].astype(int)
df_merge['notused']=df_merge['notused'].astype(int)
#print(df_merge)

df_merge = df_merge.rename(columns={"used": "count_of_occupancy", 'slotid' : 'count_of_slots'})
df_parkhour=pd.DataFrame(df_merge.groupby(['date','icao_code','hour'],as_index=False).agg({'count_of_occupancy':('sum'),'count_of_slots':pd.Series.nunique}))
df_parkhour['pct_utilization']= df_parkhour['count_of_occupancy'] / df_parkhour['count_of_slots'] /30 * 100
df_parkhour['date']=pd.to_datetime(df_parkhour['date'])
#print(df_parkhour)

df_parkhour['date1'] = df_parkhour['date'].astype(str)
df_parkhour['hour1'] = df_parkhour['hour'].astype(str)
df_parkhour['_id'] = df_parkhour['date1']+df_parkhour['icao_code']+df_parkhour['hour1']
del df_parkhour['date1'],df_parkhour['hour1']
#print(df_parkhour)

df_parkday=pd.DataFrame(df_merge.groupby(['date','icao_code'],as_index=False).agg({'count_of_occupancy':('sum'),'count_of_slots':pd.Series.nunique}))
df_parkday['pct_utilization']= df_parkday['count_of_occupancy'] / df_parkday['count_of_slots'] /1800 * 100
df_parkday['date']=pd.to_datetime(df_parkday['date'])
#print(df_parkday)

df_parkday['date1'] = df_parkday['date'].astype(str)
df_parkday['_id'] = df_parkday['date1']+df_parkday['icao_code']
del df_parkday['date1']
#print(df_parkday)

# top3 utilization
top3util=pd.DataFrame(df_merge.groupby(['date','icao_code','hour'],as_index=False).agg({'count_of_occupancy':('sum'),'count_of_slots':pd.Series.nunique}))
top3util['pct_utilization']= top3util['count_of_occupancy'] / top3util['count_of_slots'] /30 * 100
top3util['rank']=top3util.groupby(['date','icao_code'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date']=pd.to_datetime(top3util['date'])
top3util['date']=pd.to_datetime(top3util['date'].dt.date)
del top3util['count_of_occupancy'], top3util['count_of_slots']
#print(top3util)

top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
#print(top3util)

dict_parkday=pd.DataFrame.to_dict(df_parkday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_parkingday']
collectionInfo = db.api_parkingday
ids=[data.pop("_id") for data in dict_parkday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_parkday)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_parkhour=pd.DataFrame.to_dict(df_parkhour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_parkinghour']
collectionInfo = db.api_parkinghour
ids=[data.pop("_id") for data in dict_parkhour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_parkhour)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_parkingtop3utilization']
collectionInfo = db.api_parkingtop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)