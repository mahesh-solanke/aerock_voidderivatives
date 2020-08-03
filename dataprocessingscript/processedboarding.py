import pandas as pd
from pymongo import MongoClient
# build a new client instance of MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.boardingraw
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

df1.loc[df1['value'] > 5, 'inuse'] = 1
df1.loc[df1['value'] <= 5, 'inuse'] = 0
df1.loc[df1['value'] <= 5, 'notinuse'] = 1
df1.loc[df1['value'] > 5, 'notinuse'] = 0
#print(df1)

df1['datetime'] = pd.to_datetime(df1['date and time'])
df1['date'] = pd.to_datetime(df1['datetime'].dt.date)
df1['hour'] = df1['datetime'].dt.hour
del df1['date and time']
del df1['datetime']
#print(df1)

top3util=pd.DataFrame(df1.groupby(['date','icao_code','hour'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum'),'seats': ('count')}))
top3util['pct_utilization']=top3util['inuse'] / top3util['seats'] * 100
top3util['rank']=top3util.groupby(['date','icao_code'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date'] = pd.to_datetime(top3util['date'].dt.date)
del top3util['inuse'],top3util['notinuse'],top3util['seats']
#print(top3util)


top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
#print(top3util)

dict_boardingtop3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_boardingtop3util']
collectionInfo = db.api_boardingtop3util
ids=[data.pop("_id") for data in dict_boardingtop3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_boardingtop3util)]
response = collectionInfo.bulk_write(operations)  
print(response)

allmetricday=pd.DataFrame(df1.groupby(['date','icao_code'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum'),'seats': ('count')}))
allmetricday['pct_utilization']=allmetricday['inuse'] / allmetricday['seats'] * 100
allmetricday['date'] = pd.to_datetime(allmetricday['date'].dt.date)
allmetricday=allmetricday.rename(columns={"inuse": "count_used","notinuse":"count_unused","seats":"total_count"})
#print(allmetricday)

allmetricday['date1'] = allmetricday['date'].astype(str)
allmetricday['_id'] = allmetricday['date1']+allmetricday['icao_code']
del allmetricday['date1']
#print(allmetricday)


dict_boardingday=pd.DataFrame.to_dict(allmetricday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_boardingday']
collectionInfo = db.api_boardingday
ids=[data.pop("_id") for data in dict_boardingday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_boardingday)]
response = collectionInfo.bulk_write(operations)  
#print(response)


allmetrichour=pd.DataFrame(df1.groupby(['date','icao_code','hour'],as_index=False).agg({'inuse':('sum'),'notinuse':('sum'),'seats': ('count')}))
allmetrichour['pct_utilization']=allmetrichour['inuse'] / allmetrichour['seats'] * 100
allmetrichour=allmetrichour.rename(columns={"inuse": "count_used","notinuse":"count_unused","seats":"total_count"})
allmetrichour['date'] = pd.to_datetime(allmetrichour['date'].dt.date)
#print(allmetrichour.head())

allmetrichour['date1'] = allmetrichour['date'].astype(str)
allmetrichour['hour1'] = allmetrichour['hour'].astype(str)
allmetrichour['_id'] = allmetrichour['date1']+allmetrichour['icao_code']+allmetrichour['hour1']
del allmetrichour['date1'],allmetrichour['hour1']
#print(allmetrichour.head())


dict_boardinghour=pd.DataFrame.to_dict(allmetrichour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_boardinghour']
collectionInfo = db.api_boardinghour
ids=[data.pop("_id") for data in dict_boardinghour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_boardinghour)]
response = collectionInfo.bulk_write(operations)  
print(response)
