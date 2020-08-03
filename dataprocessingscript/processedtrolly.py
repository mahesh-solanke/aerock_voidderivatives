import pandas as pd
from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawmap = db.trolleymap
rawasens=db.trolleyasensor
rawssens=db.trolleyssensor
#print ("total docs in collection:", rawmap.count_documents( {} ))
#print ("total docs in collection:", rawasens.count_documents( {} ))
#print ("total docs in collection:", rawssens.count_documents( {} ))

# make an API call to the MongoDB server using a Collection object
mongodocs_map = list(rawmap.find())
mongodocs_asen = list(rawasens.find())
mongodocs_ssen= list(rawssens.find())

series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))
series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

# create an empty DataFrame obj for storing Series objects
df_map = pd.DataFrame(columns=[])
df_asen = pd.DataFrame(columns=[])
df_ssen = pd.DataFrame(columns=[])

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

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_asen ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_asen = df_asen.append( series_obj )

# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_ssen ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_ssen = df_ssen.append( series_obj )

del df_asen['_id']
del df_ssen['_id']
del df_map['_id']
'''print(df_asen)
print(df_ssen)
print(df_map)
'''

df_asen['ainuse'] = (df_asen['x'] !=0) & (df_asen['y'] !=0) & (df_asen['z'] !=0)
df_asen['ainuse'] = df_asen['ainuse'].astype(int)
df_ssen['sinuse'] = (df_ssen['svalue']) > 7
df_ssen['sinuse'] = df_ssen['sinuse'].astype(int)
df1=pd.merge(df_map, df_asen)
df2=pd.merge(df1, df_ssen)

pd.DataFrame(df2[['datetime','icao_code','deviceid','asensorid','x','y','z','ssensorid','svalue','ainuse', 'sinuse']])

df2['datetime'] = pd.to_datetime(df2['datetime'])
df2['hour'] = df2['datetime'].dt.hour
df2['date']=df2['datetime'].dt.date
df2['result'] = df2['sinuse'].astype(bool) | df2['ainuse'].astype(bool)
df2['result'] = df2['result'].astype(int) 

df2.loc[df2['result'] == 1 , 'used_trolly'] = 1
df2.loc[df2['result'] == 0 , 'used_trolly'] = 0
df2.loc[df2['result'] == 0, 'unused_trolly'] = 1
df2.loc[df2['result'] == 1, 'unused_trolly'] = 0

df_calchour=pd.DataFrame(df2.groupby(['date','icao_code','hour'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
df_calchour['total_count']= df_calchour['used_trolly']+ df_calchour['unused_trolly']
df_calchour.rename(columns = {'used_trolly':'count_used','unused_trolly':'count_unused'},inplace=True)
df_calchour['pct_utilization']= (df_calchour['count_used'] / df_calchour['total_count'])*100
df_calchour['date']=pd.to_datetime(df_calchour['date'])
#print(df_calchour)

df_calchour['date1'] = df_calchour['date'].astype(str)
df_calchour['hour1'] = df_calchour['hour'].astype(str)
df_calchour['_id'] = df_calchour['date1']+df_calchour['icao_code']+df_calchour['hour1']
del df_calchour['date1'],df_calchour['hour1']
#print(df_calchour)

df_calcday=pd.DataFrame(df2.groupby(['date','icao_code'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
df_calcday['total_count']= df_calcday['used_trolly']+ df_calcday['unused_trolly']
df_calcday.rename(columns = {'used_trolly':'count_used','unused_trolly':'count_unused'},inplace=True)
df_calcday['pct_utilization']= (df_calcday['count_used'] / df_calcday['total_count'])*100
df_calcday['date']=pd.to_datetime(df_calcday['date'])
#print(df_calcday)

df_calcday['date1'] = df_calcday['date'].astype(str)
df_calcday['_id'] = df_calcday['date1']+df_calcday['icao_code']
del df_calcday['date1']
#print(df_calcday)

# top3 utilization
top3util=pd.DataFrame(df2.groupby(['date','icao_code','hour'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
top3util['total_count']= top3util['used_trolly']+ top3util['unused_trolly']
top3util.rename(columns = {'used_trolly':'count_used','unused_trolly':'count_unused'},inplace=True)
top3util['pct_utilization']= (top3util['count_used'] / top3util['total_count'])*100
top3util['rank']=top3util.groupby(['date','icao_code'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
del top3util['count_used'], top3util['count_unused'],top3util['total_count'] 
top3util['date']=pd.to_datetime(top3util['date'])
#print(top3util)

top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
#print(top3util)

dict_trolleyday=pd.DataFrame.to_dict(df_calcday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_trolleycalcday']
collectionInfo = db.api_trolleycalcday
ids=[data.pop("_id") for data in dict_trolleyday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_trolleyday)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_trolleyhour=pd.DataFrame.to_dict(df_calchour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_trolleycalchour']
collectionInfo = db.api_trolleycalchour
ids=[data.pop("_id") for data in dict_trolleyhour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_trolleyhour)]
response = collectionInfo.bulk_write(operations)  
print(response)

dict_top3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_trolleytop3utilization']
collectionInfo = db.api_trolleytop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)