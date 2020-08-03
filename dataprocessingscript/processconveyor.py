import pandas as pd
from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.conveyorraw
#print ("total docs in collection:", rawdata.count_documents( {} ))

# make an API call to the MongoDB server using a Collection object
mongodocs_conveyor = list(rawdata.find())
series_obj = pd.Series({"a key":"a value"})
#print ("series_obj:", type(series_obj))
series_obj = pd.Series( {"one":"index"} )
series_obj.index = [ "one" ]
#print ("index:", series_obj.index)

# create an empty DataFrame obj for storing Series objects
df_conveyor = pd.DataFrame(columns=[])
# iterate over the list of MongoDB dict documents
for num, doc in enumerate( mongodocs_conveyor ):
    # convert ObjectId() to str
    doc["_id"] = str(doc["_id"])
    # get document _id from dict
    doc_id = doc["_id"]
    # create a Series obj from the MongoDB dict
    series_obj = pd.Series( doc, name=doc_id )
    # append the MongoDB Series obj to the DataFrame obj
    df_conveyor = df_conveyor.append( series_obj )

del df_conveyor['_id']
df_conveyor['stimedate'] = pd.to_datetime(df_conveyor['stimedate'])
df_conveyor['date'] = pd.to_datetime(df_conveyor['stimedate'].dt.date)
df_conveyor['etimedate'] = pd.to_datetime(df_conveyor['etimedate'])
df_conveyor['hour'] = df_conveyor['stimedate'].dt.hour
df_conveyor['usage_minutes']= ((df_conveyor['etimedate']-df_conveyor['stimedate']).dt.seconds)/60
#print(df_conveyor)

# Average time of all conveyor belt at each airport daily
m1avgday=pd.DataFrame(df_conveyor.groupby(['date','icao_code'],as_index=False).agg({'usage_minutes':('sum'),'cb_id':('count')}))
m1avgday['avg_opr_allconveyorbelts_min']=m1avgday['usage_minutes']/m1avgday['cb_id']
del m1avgday['cb_id'],m1avgday['usage_minutes']
m1avgday['date'] = pd.to_datetime(m1avgday['date'])

m1avgday['date1'] = m1avgday['date'].astype(str)
m1avgday['_id'] = m1avgday['date1']+m1avgday['icao_code']
del m1avgday['date1']
print(m1avgday)

# to MongoDB
dict_conveyoravgday=pd.DataFrame.to_dict(m1avgday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_cbavgday']
collectionInfo = db.api_cbavgday
ids=[data.pop("_id") for data in dict_conveyoravgday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyoravgday)]
response = collectionInfo.bulk_write(operations)  
print(response)

# Average time of all conveyor belt each airport hourly
m1avghour=pd.DataFrame(df_conveyor.groupby(['date','icao_code','hour'],as_index=False).agg({'usage_minutes':('sum'),'cb_id':('count')}))
m1avghour['avg_opr_allconveyorbelts_min']=m1avghour['usage_minutes']/m1avghour['cb_id']
del m1avghour['cb_id'],m1avghour['usage_minutes']
m1avghour['date'] = pd.to_datetime(m1avghour['date'])

m1avghour['date1'] = m1avghour['date'].astype(str)
m1avghour['hour1'] = m1avghour['hour'].astype(str)
m1avghour['_id'] = m1avghour['date1']+m1avghour['icao_code']+m1avghour['hour1']
del m1avghour['date1'],m1avghour['hour1']
print(m1avghour)

# to MongoDB
dict_conveyoravghour=pd.DataFrame.to_dict(m1avghour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_cbavghour']
collectionInfo = db.api_cbavghour
ids=[data.pop("_id") for data in dict_conveyoravghour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyoravghour)]
response = collectionInfo.bulk_write(operations)  
print(response)

#percent utilization of each conveyor belt at each airport daily
m2perutilday=pd.DataFrame(df_conveyor.groupby(['date','icao_code','cb_id'],as_index=False).agg({'usage_minutes':('sum')}))
m2perutilday['pct_opr_allconveyorbelts']=(m2perutilday['usage_minutes']/(24*60))*100
m2perutilday['date'] = pd.to_datetime(m2perutilday['date'])
del m2perutilday['usage_minutes']

m2perutilday['date1'] = m2perutilday['date'].astype(str)
m2perutilday['_id'] = m2perutilday['date1']+m2perutilday['icao_code']
del m2perutilday['date1']
print(m2perutilday)

# to MongoDB
dict_conveyorperutilday=pd.DataFrame.to_dict(m2perutilday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_cbperutilday']
collectionInfo = db.api_cbperutilday
ids=[data.pop("_id") for data in dict_conveyorperutilday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyorperutilday)]
response = collectionInfo.bulk_write(operations)  
print(response)

#percent utilization of each conveyor belt at each airport hourly
m2perutilhour=pd.DataFrame(df_conveyor.groupby(['date','icao_code','hour','cb_id'],as_index=False).agg({'usage_minutes':('sum')}))
m2perutilhour['pct_opr_allconveyorbelts']=(m2perutilhour['usage_minutes']/60)*100
m2perutilhour['date'] = pd.to_datetime(m2perutilhour['date'])
del m2perutilhour['usage_minutes']
#m2perutilhour=m2perutilhour.rename(columns={"cboprtime": "pct_opr_eachconveyorbelt"})

m2perutilhour['date1'] = m2perutilhour['date'].astype(str)
m2perutilhour['hour1'] = m2perutilhour['hour'].astype(str)
m2perutilhour['_id'] = m2perutilhour['date1']+m2perutilhour['icao_code']+m2perutilhour['hour1']
del m2perutilhour['date1'],m2perutilhour['hour1']
print(m2perutilhour)

# to MongoDB
dict_conveyorperutilhour=pd.DataFrame.to_dict(m2perutilhour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_cbperutilhour']
collectionInfo = db.api_cbperutilhour
ids=[data.pop("_id") for data in dict_conveyorperutilhour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyorperutilhour)]
response = collectionInfo.bulk_write(operations)  
print(response)

top3util=pd.DataFrame(df_conveyor.groupby(['date','icao_code','hour'],as_index=False).agg({'usage_minutes':('sum'),'cb_id':('count')}))
top3util['avg_opr_allconveyorbelts_min']=top3util['usage_minutes']/top3util['cb_id']
del top3util['cb_id'],top3util['usage_minutes']
top3util['rank']=top3util.groupby(['date','icao_code'])['avg_opr_allconveyorbelts_min'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')

top3util['date1'] = top3util['date'].astype(str)
top3util['hour1'] = top3util['hour'].astype(str)
top3util['_id'] = top3util['date1']+top3util['icao_code']+top3util['hour1']
del top3util['date1'],top3util['hour1']
print(top3util)

# to MongoDB
dict_conveyortop3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['onlyfordemo']
collection_currency = db['api_cbtop3util']
collectionInfo = db.api_cbtop3util
ids=[data.pop("_id") for data in dict_conveyortop3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyortop3util)]
response = collectionInfo.bulk_write(operations)  
print(response)