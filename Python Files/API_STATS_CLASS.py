import requests
import pandas as pd
from forex_python.converter import CurrencyRates #CurrencyRates is a class which produces exchange rates

class AccessAPI:


    @staticmethod  
    def accessStockData(link):
        response = requests.get(link)
        nested_dict = response.json()
        time_series_dict = nested_dict.get('Time Series (Daily)', {})
        df = pd.DataFrame.from_dict(time_series_dict, orient='index')  #this initalises the attribute, df
        keys = ['1. open', '2. high', '3. low', '4. close']
        for key in keys:
            df[key] = pd.to_numeric(df[key])
        return df 
    
    @staticmethod
    def getMean(df):    #return an array
        keys = ['1. open', '2. high', '3. low', '4. close']
        list_of_averages = []
        for key in keys:
            list_of_averages.append(df[key].mean().round(2))
        return list_of_averages
    
    @staticmethod
    def getMedian(df): #returns array
        keys = ['1. open', '2. high', '3. low', '4. close']
        list_of_medians = []
        for key in keys:
            list_of_medians.append(df[key].median().round(2))
        return list_of_medians
    
    @staticmethod
    def getMode(df): #returns array
        keys = ['1. open', '2. high', '3. low', '4. close']
        list_of_modes = []
        for key in keys:
            list_of_modes.append(df[key].mode().round(2))
        return list_of_modes

    @staticmethod
    def calc_Volatility(df): #returns array
        keys = ['1. open', '2. high', '3. low', '4. close']
        list_of_var = []
        for key in keys:
            list_of_var.append(df[key].var().round(2))
        return list_of_var