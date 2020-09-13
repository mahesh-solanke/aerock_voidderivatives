import pandas as pd
import psycopg2
from pymongo import MongoClient

engine=psycopg2.connect(host ='localhost', dbname='aerock', user='postgres', password='sih2020', port='5432')
df_threshold=pd.read_sql_query('SELECT dt.id, sensor_type, sensor_threshold, threshold_value_high, capacity, airfac_id, threshold_value_low, icao_code, af.fac_id FROM public.dashboard_threshold as dt join dashboard_airportfacility as af on dt.airfac_id=af.id join dashboard_airport as da on af.air_id=da.id where af.fac_id=6;',con=engine)
#df_threshold

# build a new client instance of MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawmap = db.trolleymap
rawasens=db.ntrolleyasensor
rawssens=db.ntrolleyssensor
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
#print(df_asen)
#print(df_ssen)
#print(df_map)


df1=pd.merge(df_map, df_asen)
df2=pd.merge(df1, df_ssen)
df2['ainuse'] = (df2['x'] !=0) & (df2['y'] !=0) & (df2['z'] !=0)
df2['ainuse'] = df2['ainuse'].astype(int)
df_mergethresh=pd.merge(df2, df_threshold[["sensor_threshold", "threshold_value_high", "threshold_value_low", "icao_code"]], on="icao_code", how="left")
#df_mergethresh.head(1)

df_mergethresh['sinuse'] = (df_mergethresh['svalue']) > df_mergethresh['sensor_threshold']
df_mergethresh['sinuse'] = df_mergethresh['sinuse'].astype(int)
#df_mergethresh.to_excel('df_mergethresh.xlsx')

del df_mergethresh['atype'],df_mergethresh['stype']
#df_mergethresh.head(1)

df_mergethresh['datetime'] = pd.to_datetime(df_mergethresh['datetime'])
df_mergethresh['date'] = df_mergethresh['datetime'].dt.strftime('%Y-%m-%d')
df_mergethresh['hour'] = df_mergethresh['datetime'].dt.hour
#print(df_mergethresh)
#df_mergethresh.to_excel('df_mergethresh.xlsx')

df_mergethresh['result'] = df_mergethresh['sinuse'].astype(bool) | df_mergethresh['ainuse'].astype(bool)
df_mergethresh['result'] = df_mergethresh['result'].astype(int) 
#df_mergethresh.to_excel('df_mergethresh.xlsx')

df_mergethresh.loc[df_mergethresh['result'] == 1 , 'used_trolly'] = 1
df_mergethresh.loc[df_mergethresh['result'] == 0 , 'used_trolly'] = 0
df_mergethresh.loc[df_mergethresh['result'] == 0, 'unused_trolly'] = 1
df_mergethresh.loc[df_mergethresh['result'] == 1, 'unused_trolly'] = 0
#df_mergethresh.to_excel('df_mergethresh.xlsx')

df_calchour=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','hour'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
df_calchour['total_count']= df_calchour['used_trolly']+ df_calchour['unused_trolly']
df_calchour.rename(columns = {'used_trolly':'count_used','unused_trolly':'count_unused'},inplace=True)
df_calchour['pct_utilization']= (df_calchour['count_used'] / df_calchour['total_count'])*100
df_calchour['date']=pd.to_datetime(df_calchour['date'])
df_calchour['date'] = df_calchour['date'].dt.strftime('%Y-%m-%d')
#print(df_calchour)
#df_calchour.to_excel('df_calchour.xlsx')
df_calchour['date1'] = df_calchour['date'].astype(str)
df_calchour['hour1'] = df_calchour['hour'].astype(str)
df_calchour['_id'] = df_calchour['date1']+df_calchour['icao_code']+df_calchour['hour1']
del df_calchour['date1'],df_calchour['hour1']
#df_calchour

df_calcday=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
df_calcday['total_count']= df_calcday['used_trolly']+ df_calcday['unused_trolly']
df_calcday.rename(columns = {'used_trolly':'count_used','unused_trolly':'count_unused'},inplace=True)
df_calcday['pct_utilization']= (df_calcday['count_used'] / df_calcday['total_count'])*100
df_calcday['date']=pd.to_datetime(df_calcday['date'])
df_calcday['date'] = df_calcday['date'].dt.strftime('%Y-%m-%d')
#print(df_calcday)
#df_calcday.to_excel('df_calcday.xlsx')
df_calcday['date1'] = df_calcday['date'].astype(str)
df_calcday['_id'] = df_calcday['date1']+df_calcday['icao_code']
del df_calcday['date1']
#df_calcday

# top3 utilization
top3util=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
top3util['total_count']= top3util['used_trolly']+ top3util['unused_trolly']
top3util.rename(columns = {'used_trolly':'count_used','unused_trolly':'count_unused'},inplace=True)
top3util['pct_utilization']= (top3util['count_used'] / top3util['total_count'])*100
top3util['rank']=top3util.groupby(['date','icao_code'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<2')
del top3util['count_used'], top3util['count_unused'],top3util['total_count'] 
top3util['rank']=top3util.groupby(['date'])['pct_utilization'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date'] = pd.to_datetime(top3util['date'])
top3util['date'] = top3util['date'].dt.strftime('%Y-%m-%d')
top3util.insert(1, 'newid', range(0, 0 + len(top3util)))
#print(top3util)
top3util['date1'] = top3util['date'].astype(str)
top3util['newid'] = top3util['newid'].astype(str)
top3util['_id'] = top3util['date1']+top3util['newid']
del top3util['date1'],top3util['newid']
#print(top3util)

dict_trolleyday=pd.DataFrame.to_dict(df_calcday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
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
db=client['aerockdb']
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
db=client['aerockdb']
collection_currency = db['api_trolleytop3utilization']
collectionInfo = db.api_trolleytop3utilization
ids=[data.pop("_id") for data in dict_top3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_top3util)]
response = collectionInfo.bulk_write(operations)  
print(response)

df_runningdata = pd.DataFrame(df_mergethresh[['icao_code','deviceid','datetime','used_trolly','unused_trolly','threshold_value_high','threshold_value_low']])
df_runningdata['date']= df_runningdata['datetime'].dt.date
df_hold=pd.DataFrame(df_runningdata.groupby(['icao_code','date','datetime','threshold_value_high','threshold_value_low'],as_index=False).agg({'used_trolly':('sum'),'unused_trolly':('sum')}))
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
            cumsum_inuse = cumsum_inuse + row.used_trolly
            cumsum_notinuse = cumsum_notinuse+row.unused_trolly
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
df_excporg['facility']='Trolley'
df_excporg['deviceid']=''
df_excporg['areaid']=''
del df_excporg['used_trolly'],df_excporg['unused_trolly'],df_excporg['cumsum_inuse'],df_excporg['cumsum_notinuse'],df_excporg['date']
df_excporg['_id'] = df_excporg['icao_code']+df_excporg['facility']+df_excporg['event_time'].astype(str)
#print(df_excporg)
import datetime as dt
df_excporg['event_time']=(df_excporg['event_time'] - dt.datetime(1970,1,1)).dt.total_seconds()
#df_excporg
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