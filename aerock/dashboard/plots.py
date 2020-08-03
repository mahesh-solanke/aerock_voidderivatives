import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
#import chart_studio.plotly as py
import pandas as pd
from pymongo import MongoClient

#logger = logging.getLogger(__name__)
client = MongoClient('mongodb+srv://sih2020:sih2020@sih2020.l990z.mongodb.net/<dbname>?retryWrites=true&w=majority')
db_name = 'reportsDB'
db = client[db_name]

def landing(date,aid):
    abc = 'Landing Page'
    return abc
