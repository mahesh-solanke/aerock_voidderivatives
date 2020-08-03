import pandas as pd
from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

db = mongo_client.rawdata
wifiraw = db.wifiraw
wifimap=db.wifimap
#print ("total docs in collection:", wifiraw.count_documents( {} ))
#print ("total docs in collection:", wifimap.count_documents( {} ))

# make an API call to the MongoDB server using a Collection object
mongodocs_wifi = list(wifiraw.find())
mongodocs_map = list(wifimap.find())

series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))

series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

# create an empty DataFrame obj for storing Series objects
df_wifi = pd.DataFrame(columns=[])
df_map = pd.DataFrame(columns=[])

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_wifi ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_wifi = df_wifi.append( series_obj )

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_map ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_map = df_map.append( series_obj )

del df_wifi['_id']
del df_map['_id']
df_merge=pd.merge(df_wifi,df_map)

df_merge['sdatetime'] = pd.to_datetime(df_merge['sdatetime'])
df_merge['edatetime'] = pd.to_datetime(df_merge['edatetime'])
df_merge['hour']=df_merge['sdatetime'].dt.hour

df_merge['usage_minutes']= ((df_merge['edatetime']-df_merge['sdatetime']).dt.seconds)/60

df_merge['date']=pd.to_datetime(df_merge['sdatetime']).dt.date
#print(df_merge)

#Total count of users daily
#Sum of download,upload daily
#Average utilization daily
df_allmetricday=pd.DataFrame(df_merge.groupby(['date','icao_code'],as_index=False).agg({'macaddress':('count'),'usage_minutes':('sum'),'dwnld_KB':('sum'),'upld_KB':('sum')}))
df_allmetricday.rename(columns = {'macaddress':'total_unique_users','usage_minutes':'total_used_minutes'},inplace=True)
df_allmetricday['avg_utilization_min'] = df_allmetricday['total_used_minutes'] / df_allmetricday['total_unique_users']  # / opr
df_allmetricday.rename(columns = {'dwnld_KB':'total_download','upld_KB':'total_upload'},inplace=True)
df_allmetricday['total_download']=df_allmetricday['total_download']/(1024**2)
df_allmetricday['total_upload']=df_allmetricday['total_upload']/(1024**2)
df_allmetricday['date']=pd.to_datetime(df_allmetricday['date'])
#print(df_allmetricday)

df_allmetricday['date1'] = df_allmetricday['date'].astype(str)
df_allmetricday['_id'] = df_allmetricday['date1']+df_allmetricday['icao_code']
del df_allmetricday['date1']
#print(df_allmetricday)

#Total count of users daily
#Sum of download,upload daily
#Average utilization daily
df_allmetrichour=pd.DataFrame(df_merge.groupby(['date','icao_code','hour'],as_index=False).agg({'macaddress':('count'),'usage_minutes':('sum'),'dwnld_KB':('sum'),'upld_KB':('sum')}))
df_allmetrichour.rename(columns = {'macaddress':'total_unique_users','usage_minutes':'total_used_minutes'},inplace=True)
df_allmetrichour['avg_utilization_min'] = df_allmetrichour['total_used_minutes'] / df_allmetrichour['total_unique_users']  # / opr
df_allmetrichour.rename(columns = {'dwnld_KB':'total_download','upld_KB':'total_upload'},inplace=True)
df_allmetrichour['total_download']=df_allmetrichour['total_download']/(1024**2)
df_allmetrichour['total_upload']=df_allmetrichour['total_upload']/(1024**2)
df_allmetrichour['date']=pd.to_datetime(df_allmetrichour['date'])
#print(df_allmetrichour)

df_allmetrichour['date1'] = df_allmetrichour['date'].astype(str)
df_allmetrichour['hour1'] = df_allmetrichour['hour'].astype(str)
df_allmetrichour['_id'] = df_allmetrichour['date1']+df_allmetrichour['icao_code']+df_allmetrichour['hour1']
del df_allmetrichour['date1'],df_allmetrichour['hour1']
#print(df_allmetrichour)

# top3 utilization
top3util=pd.DataFrame(df_merge.groupby(['date','icao_code','hour'],as_index=False).agg({'macaddress':('count'),'usage_minutes':('sum')}))
top3util.rename(columns = {'macaddress':'total_unique_users','usage_minutes':'total_used_minutes'},inplace=True)
top3util['avg_utilization_min'] = top3util['total_used_minutes'] / top3util['total_unique_users']
top3util['rank']=top3util.groupby(['date','icao_code'])['avg_utilization_min'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
del top3util['total_unique_users'], top3util['total_used_minutes']
top3util['date'] = pd.to_datetime(top3util['date'])
top3util['date'] = pd.to_datetime(top3util['date'].dt.date)
#print(top3util)

top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
#print(top3util)

dict_wifiday=pd.DataFrame.to_dict(df_allmetricday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_wifiday']
collectionInfo = db.api_wifiday
ids=[data.pop("_id") for data in dict_wifiday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_wifiday)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_wifihour=pd.DataFrame.to_dict(df_allmetrichour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_wifihour']
collectionInfo = db.api_wifihour
ids=[data.pop("_id") for data in dict_wifihour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_wifihour)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_wifitop3utilization']
collectionInfo = db.api_wifitop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)