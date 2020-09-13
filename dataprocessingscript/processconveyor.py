import pandas as pd
import psycopg2
from pymongo import MongoClient
engine=psycopg2.connect(host ='localhost', dbname='aerock', user='postgres', password='sih2020', port='5432')

df_threshold=pd.read_sql_query('SELECT dt.id, sensor_type, sensor_threshold, threshold_value_high, capacity, airfac_id, threshold_value_low, icao_code, af.fac_id FROM public.dashboard_threshold as dt join dashboard_airportfacility as af on dt.airfac_id=af.id join dashboard_airport as da on af.air_id=da.id where af.fac_id=2;',con=engine)
#df_threshold

# build a new client instance of MongoClient
mongo_client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")

# create new database and collection objects
db = mongo_client.rawdata
rawdata = db.nconveyorbelt
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
#df_conveyor

df_mergethresh=pd.merge(df_conveyor, df_threshold[["threshold_value_high", "threshold_value_low", "icao_code"]], on="icao_code", how="left")
#df_mergethresh.to_excel('df_mergethresh.xlsx')
#df_mergethresh.head(1)

df_mergethresh['stimedate'] = pd.to_datetime(df_mergethresh['stimedate'])
df_mergethresh['date'] = df_mergethresh['stimedate'].dt.strftime('%Y-%m-%d')
df_mergethresh['etimedate'] = pd.to_datetime(df_mergethresh['etimedate'])
df_mergethresh['hour'] = df_mergethresh['stimedate'].dt.hour
#df_mergethresh.head(1)

df_mergethresh['usage_minutes']= ((df_mergethresh['etimedate']-df_mergethresh['stimedate']).dt.seconds)/60
#df_mergethresh.head(1)

# Average time of all conveyor belt at each airport daily
m1avgday=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'usage_minutes':('sum'),'cb_id':('count')}))
m1avgday['avg_opr_allconveyorbelts_min']=m1avgday['usage_minutes']/m1avgday['cb_id']
del m1avgday['cb_id'],m1avgday['usage_minutes']
m1avgday['date'] = pd.to_datetime(m1avgday['date'])
m1avgday['date'] = m1avgday['date'].dt.strftime('%Y-%m-%d')
m1avgday['date1'] = m1avgday['date'].astype(str)
m1avgday['_id'] = m1avgday['date1']+m1avgday['icao_code']
del m1avgday['date1']
#print(m1avgday)

dict_conveyoravgday=pd.DataFrame.to_dict(m1avgday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_cbavgday']
collectionInfo = db.api_cbavgday
ids=[data.pop("_id") for data in dict_conveyoravgday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyoravgday)]
response = collectionInfo.bulk_write(operations)  
print(response)

# Average time of all conveyor belt each airport hourly
m1avghour=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','hour'],as_index=False).agg({'usage_minutes':('sum'),'cb_id':('count')}))
m1avghour['avg_opr_allconveyorbelts_min']=m1avghour['usage_minutes']/m1avghour['cb_id']
del m1avghour['cb_id'],m1avghour['usage_minutes']
m1avghour['date'] = pd.to_datetime(m1avghour['date'])
m1avghour['date'] = m1avghour['date'].dt.strftime('%Y-%m-%d')
m1avghour['date1'] = m1avghour['date'].astype(str)
m1avghour['hour1'] = m1avghour['hour'].astype(str)
m1avghour['_id'] = m1avghour['date1']+m1avghour['icao_code']+m1avghour['hour1']
del m1avghour['date1'],m1avghour['hour1']
#print(m1avghour)

dict_conveyoravghour=pd.DataFrame.to_dict(m1avghour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_cbavghour']
collectionInfo = db.api_cbavghour
ids=[data.pop("_id") for data in dict_conveyoravghour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyoravghour)]
response = collectionInfo.bulk_write(operations)  
print(response)

#percent utilization of each conveyor belt at each airport daily
m2perutilday=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','cb_id'],as_index=False).agg({'usage_minutes':('sum')}))
m2perutilday['pct_opr_allconveyorbelts']=(m2perutilday['usage_minutes']/(24*60))*100
m2perutilday['date'] = pd.to_datetime(m2perutilday['date'])
m2perutilday['date'] = m2perutilday['date'].dt.strftime('%Y-%m-%d')
del m2perutilday['usage_minutes']
m2perutilday['date1'] = m2perutilday['date'].astype(str)
m2perutilday['_id'] = m2perutilday['date1']+m2perutilday['icao_code']+m2perutilday['cb_id']
del m2perutilday['date1']
#print(m2perutilday)
#m2perutilday.to_excel('m2perutilday.xlsx')

dict_conveyorperutilday=pd.DataFrame.to_dict(m2perutilday, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_cbperutilday']
collectionInfo = db.api_cbperutilday
ids=[data.pop("_id") for data in dict_conveyorperutilday]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyorperutilday)]
response = collectionInfo.bulk_write(operations)  
print(response)

#percent utilization of each conveyor belt at each airport hourly
m2perutilhour=pd.DataFrame(df_mergethresh.groupby(['date','icao_code','hour','cb_id'],as_index=False).agg({'usage_minutes':('sum')}))
m2perutilhour['pct_opr_allconveyorbelts']=(m2perutilhour['usage_minutes']/60)*100
m2perutilhour['date'] = pd.to_datetime(m2perutilhour['date'])
m2perutilhour['date'] = m2perutilhour['date'].dt.strftime('%Y-%m-%d')
del m2perutilhour['usage_minutes']
m2perutilhour['date1'] = m2perutilhour['date'].astype(str)
m2perutilhour['hour1'] = m2perutilhour['hour'].astype(str)
m2perutilhour['_id'] = m2perutilhour['date1']+m2perutilhour['icao_code']+m2perutilhour['cb_id']+m2perutilhour['hour1']
del m2perutilhour['date1'],m2perutilhour['hour1']
#print(m2perutilhour)

dict_conveyorperutilhour=pd.DataFrame.to_dict(m2perutilhour, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_cbperutilhour']
collectionInfo = db.api_cbperutilhour
ids=[data.pop("_id") for data in dict_conveyorperutilhour]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyorperutilhour)]
response = collectionInfo.bulk_write(operations)  
print(response)

top3util=pd.DataFrame(df_mergethresh.groupby(['date','icao_code'],as_index=False).agg({'usage_minutes':('sum'),'cb_id':('count')}))
top3util['avg_opr_allconveyorbelts_min']=top3util['usage_minutes']/top3util['cb_id']
del top3util['cb_id'],top3util['usage_minutes']
top3util['rank']=top3util.groupby(['date','icao_code'])['avg_opr_allconveyorbelts_min'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<2')
top3util['rank']=top3util.groupby(['date'])['avg_opr_allconveyorbelts_min'].rank(method='first',ascending=False)
top3util=top3util.sort_values(['date','icao_code']).query('rank<4')
top3util['date'] = pd.to_datetime(top3util['date'])
top3util['date'] = top3util['date'].dt.strftime('%Y-%m-%d')
top3util.insert(1, 'newid', range(0, 0 + len(top3util)))
top3util['date1'] = top3util['date'].astype(str)
top3util['newid'] = top3util['newid'].astype(str)
top3util['_id'] = top3util['date1']+top3util['newid']
del top3util['date1'],top3util['newid']
#print(top3util)

dict_conveyortop3util=pd.DataFrame.to_dict(top3util, orient='records')
import json
from pymongo import MongoClient
from pymongo import UpdateOne
client = MongoClient("mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority")
db=client['aerockdb']
collection_currency = db['api_cbtop3util']
collectionInfo = db.api_cbtop3util
ids=[data.pop("_id") for data in dict_conveyortop3util]
operations=[UpdateOne({"_id":idn},{'$set':data},upsert=True) for idn ,data in zip(ids,dict_conveyortop3util)]
response = collectionInfo.bulk_write(operations)  
print(response)

df_runningdata = pd.DataFrame(df_mergethresh[['icao_code','stimedate','cb_id','usage_minutes','threshold_value_high','threshold_value_low']])
df_runningdata['date']= df_runningdata['stimedate'].dt.date
df_runningdata['threshold_value_high']= df_runningdata['threshold_value_high'] * 60 
df_runningdata['threshold_value_low']= df_runningdata['threshold_value_low'] * 60 
df_hold=pd.DataFrame(df_runningdata.groupby(['icao_code','cb_id','date','stimedate','threshold_value_high','threshold_value_low'],as_index=False).agg({'usage_minutes':('sum')}))
#df_hold.to_excel("hold.xlsx")
#df_hold.head(1)

df_demoalert = pd.DataFrame(columns=[])
uniqueicao=list(df_hold['icao_code'].unique())
for i in uniqueicao: 
    df_air = pd.DataFrame(columns=[])
    df_air=df_hold[df_hold.icao_code==i]
    
    uniquecbid=list(df_air['cb_id'].unique())
    for m in uniquecbid: 
        df_cb = pd.DataFrame(columns=[])
        df_cb=df_air[df_air.cb_id==m]

        uniquedate=list(df_cb['date'].unique())
        for l in uniquedate:    
            df_date = pd.DataFrame(columns=[])
            df_date=df_cb[df_cb.date==l]

            ls_usage_minutes = []
            cumsum_usage_minutes = 0
            last_reset = 0
            for _, row in df_date.iterrows():
                cumsum_usage_minutes = cumsum_usage_minutes + row.usage_minutes
                ls_usage_minutes.append(cumsum_usage_minutes)
                if cumsum_usage_minutes >= row.threshold_value_high: #and cumsum_inuse > 0.2*last_reset:
                    last_reset = cumsum_usage_minutes
                    cumsum_usage_minutes = 0

            df_date['cumsum_usage_minutes']=ls_usage_minutes
            df_demoalert = df_demoalert.append(df_date)
            #df_demoalert.to_excel('df_demoalert.xlsx')        

df_demoalert.loc[df_demoalert['cumsum_usage_minutes'] <= df_demoalert['threshold_value_low'], 'state'] = 'ORANGE'
df_demoalert.loc[df_demoalert['cumsum_usage_minutes'] >= df_demoalert['threshold_value_high'] , 'state'] = 'RED'
#df_demoalert.to_excel('state.xlsx')
df_excporg = pd.DataFrame(columns=[])
df_excpred = pd.DataFrame(columns=[])
df_excporg = df_demoalert[df_demoalert['state']=='ORANGE']
df_excpred = df_demoalert[df_demoalert['state']=='RED']
df_excporg=df_excporg.append(df_excpred, ignore_index=True)
df_excporg=df_excporg.rename(columns={'cumsum_usage_minutes':'actual_value','cb_id':'deviceid','stimedate': 'event_time','threshold_value_high':'high_threshold','threshold_value_low':'low_threshold'})
df_excporg['facility']='Conveyor Belt'
df_excporg['areaid']=''
del df_excporg['usage_minutes'],df_excporg['date']
df_excporg['_id'] = df_excporg['icao_code']+df_excporg['facility']+df_excporg['deviceid']+df_excporg['event_time'].astype(str)

import datetime as dt
df_excporg['event_time']=(df_excporg['event_time'] - dt.datetime(1970,1,1)).dt.total_seconds()
#print(df_excporg)
#df_excporg.to_excel('afterallopr.xlsx')
#print(df_excporg.head(5))

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