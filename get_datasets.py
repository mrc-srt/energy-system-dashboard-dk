import pandas as pd
import numpy as np
import requests
import json
import requests
import json
import datetime as dt
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
import csv


def get_mimer_data(from_dt: dt.datetime, to_dt: dt.datetime):
    base_url = "https://mimer.svk.se/PrimaryRegulation/DownloadText"
    parameters = {
        "periodFrom": from_dt.strftime("%Y-%m-%d"),
        "periodTo": to_dt.strftime("%Y-%m-%d"),
    }
    response = requests.get(base_url, params=parameters)
    content = response.content
    as_string = content.decode()
    as_csv = csv.StringIO(as_string)
    as_dataframe = pd.read_csv(as_csv, sep=";", decimal=",")
    as_dataframe.drop(as_dataframe.columns[[-1, -2]], axis=1, inplace=True)
    as_dataframe.drop(as_dataframe.tail(1).index,
                      inplace=True)  # drop last n rows
    as_dataframe.Period = pd.to_datetime(as_dataframe.Period)
    as_dataframe = as_dataframe.set_index('Period')

    as_dataframe.rename(columns={'FCR-N Pris (EUR/MW)': 'FCR_N_PriceEUR',
                       'FCR-D upp Pris (EUR/MW)': 'FCR_D_UpPriceEUR',
                       'FCR-D ned Pris (EUR/MW)': 'FCR_D_DownPriceEUR'}, inplace=True)

    # Fill NaN
    values = {"FCR_D_DownPriceEUR": 0}
    as_dataframe.fillna(value=values, inplace=True)
    return as_dataframe


def data_request(dataset, date_begin, date_end, price_area=0):
    """
    Function extract the Spot Prices data between 2 dates from energidataservice and format
    it as a pandas dataframe

    dataset:   The name of the FCR market zone in energinet database, e.g.
    "elspotprices","fcrreservesdk1" or "fcrreservesdk2"
    date_begin:     A date with the following format "2018-12-31"
    date_end:       A date with the following format "2018-12-31"

    call: spots = data_request("elspotprices", "2022-01-01", "2022-12-01", "DK2")
    """

    # SQL query send to energidataservice API
    if (type(price_area)) == str:
        price_area = ('{{"PriceArea":"{}"}}').format(price_area)
        query = {"start": date_begin, "end": date_end,
            "filter": price_area, "sort": "HourUTC asc"}
    else:
        query = {"start": date_begin, "end": date_end, "sort": "HourUTC asc"}

    print(query)
    # sendUrl
    requestUrl = "http://api.energidataservice.dk/dataset/" + dataset
    print(requestUrl)

    # extraction
    response_json = requests.get(requestUrl, params=query).json()

    # formating the data
    response_df = pd.json_normalize(response_json["records"])

    response_df.HourDK = pd.to_datetime(response_df.HourDK, format="%Y-%m-%dT%H")
    response_df.HourUTC = pd.to_datetime(response_df.HourUTC, format="%Y-%m-%dT%H")
    # response_df.set_index(pd.DatetimeIndex(response_df["HourDK"]),inplace=True) #set the time as index
    return response_df
    # return(response_df.drop(["_id", "_full_text","HourDK"], axis=1)[:-1])# drop the last lane as it is 00:00 the following day



def get_co2_data(from_dt, to_dt, hourly_resample=True):
    """
    Get CO2 data in a specified time interval.

    Ex:
    from_dt = datetime(2018, 1, 1)
    to_dt = datetime(2022, 10, 1)
    df_co2 = get_co2_data(from_dt, to_dt)
    """
    months_delta = (pd.to_datetime(to_dt).to_period('M') -
                    pd.to_datetime(from_dt).to_period('M')).n
    df_co2 = pd.DataFrame()
    for i in range(months_delta):

        from_dt_temp = from_dt + relativedelta(months=i)
        to_dt_temp = from_dt + relativedelta(months=i+1)

        headers_els = {'content-type': 'application/json'}

        query_els = """{  co2emis(
        
        where: {PriceArea: {_eq: "DK2"}, Minutes5DK: {_gte: "%s-%s-01T00:00:00"}, _and: {Minutes5UTC: {_lte: "%s-%s-02T00:00:00"}}}
        order_by: {Minutes5DK: asc})
        {
        CO2Emission
        PriceArea
        Minutes5UTC 
        }
        }
        """ % (from_dt_temp.year, from_dt_temp.month, to_dt_temp.year, to_dt_temp.month)

        request_els = requests.post('https://data-api.energidataservice.dk/v1/graphql',
                                    json={'query': query_els}, headers=headers_els)
        els_json = request_els.json()
        df_temp = pd.DataFrame(els_json['data']['co2emis'])

        df_temp['Minutes5UTC'] = pd.to_datetime(df_temp.Minutes5UTC)
        df_temp['Minutes5UTC'] = df_temp['Minutes5UTC'].dt.tz_localize(None)
        df_temp = df_temp.set_index('Minutes5UTC')

        df_co2 = df_co2.combine_first(df_temp)

    if (hourly_resample == True):
        df_co2 = df_co2.resample('1H').mean()

    return df_co2
