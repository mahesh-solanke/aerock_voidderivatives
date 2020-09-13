import pandas as pd
from pymongo import MongoClient

# build a new client instance of MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.feedbackraw
#print ("total docs in collection:", rawdata.count_documents( {} ))
mapdata = db.feedbackmap
#print ("total docs in collection:", mapdata.count_documents( {} ))

# make an API call to the MongoDB server using a Collection object
mongodocs_feedback = list(rawdata.find())
mongodocs_feedbackmap = list(mapdata.find())
series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))

series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

# create an empty DataFrame obj for storing Series objects
df_raw = pd.DataFrame(columns=[])
df_map = pd.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_feedback ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_raw = df_raw.append( series_obj )

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_feedbackmap ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_map = df_map.append( series_obj )

del df_map['_id']
#df_map
del df_raw['_id']
#df_raw

#df_merge=pd.DataFrame(df_map,df_raw)
df_merge=pd.merge(df_map,df_raw)
#df_merge

df_merge['datetime'] = pd.to_datetime(df_merge['datetime'])
df_merge['date'] = pd.to_datetime(df_merge['datetime'].dt.date)
df_merge['hour'] = df_merge['datetime'].dt.hour
#df_merge

# Average time of all conveyor belt at each airport latest
m1avgsnapshot=pd.DataFrame(df_merge.groupby(['icao_code','service_id'],as_index=False).agg({'rating':('mean')}))
m1avgsnapshot=m1avgsnapshot.rename(columns={"rating": "rating_for_service"})
#print(m1avgsnapshot)

m1avgsnapshot['service_id1']=m1avgsnapshot['service_id'].astype(str)
m1avgsnapshot['_id']=m1avgsnapshot['icao_code']+m1avgsnapshot['service_id1']
del m1avgsnapshot['service_id1']
#m1avgsnapshot

# Average time of all conveyor belt at each airport daily
m1avgday=pd.DataFrame(df_merge.groupby(['date','icao_code','service_id'],as_index=False).agg({'rating':('mean')}))
m1avgday=m1avgday.rename(columns={"rating": "rating_for_service"})
m1avgday['date'] = pd.to_datetime(m1avgday['date'].dt.date)
#print(m1avgday)

m1avgday['service_id1']=m1avgday['service_id'].astype(str)
m1avgday['date1']=m1avgday['date'].astype(str)
m1avgday['_id'] = m1avgday['date1']+m1avgday['icao_code']+m1avgday['service_id1']
del m1avgday['service_id1'],m1avgday['date1']
#m1avgday

top3util=pd.DataFrame(df_merge.groupby(['icao_code','service_id'],as_index=False).agg({'rating':('mean')}))
top3util=top3util.rename(columns={"rating": "rating_for_service"})
top3util['rank']=top3util.groupby(['icao_code'])['rating_for_service'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['icao_code']).query('rank<4')
#top3util

top3util['service_id1']=top3util['service_id'].astype(str)
top3util['_id'] = top3util['icao_code']+top3util['service_id1']
del top3util['service_id1']
#top3util

dict_m1avgsnapshot=pd.DataFrame.to_dict(m1avgsnapshot, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_fbavgutilsnapshot']
collectionInfo = db.api_fbavgutilsnapshot
ids=[data.pop("_id") for data in dict_m1avgsnapshot]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_m1avgsnapshot)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_m1avgday=pd.DataFrame.to_dict(m1avgday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_fbavgutilday']
collectionInfo = db.api_fbavgutilday
ids=[data.pop("_id") for data in dict_m1avgday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_m1avgday)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_fbtop3utilization']
collectionInfo = db.api_fbtop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)