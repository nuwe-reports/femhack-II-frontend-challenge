import pandas as pd
import numpy as np
from json import loads, dumps, JSONEncoder
from typing import Union
from Constants import HttpErrors

df = pd.DataFrame()

def init_data():
    global df
    df = pd.read_csv('data/internet_users.csv')
    df = df.drop(['Unnamed: 0', 'Cellular Subscription', 'Broadband Subscription'], axis=1)
    df = df.rename(columns={"Internet Users(%)": "internet_users_percentatge", "No. of Internet Users": "internet_users_number"})
    df = df[df["Code"].astype(bytes).str.len() == 3]

def get_countries():
    global df
    if df.empty:
        return {"Message": "Error: df is not initizalized", "Error": HttpErrors.INTERNAL_SERVER_ERROR}

    countries = df[~df["Entity"].duplicated()]["Entity"].values
    countries = countries.tolist()
    if len(countries) < 1:
        return {"Message": "No countries have been found", "Error": HttpErrors.NOT_FOUND}
    return {"Message": "List of countries", "Countries": countries }


def get_data_from_country(country: str):
    global df

    if df.empty:
        return {"Message": "Error: df is not initialized", "Error": HttpErrors.INTERNAL_SERVER_ERROR}

    country_df = df[df["Entity"] == country]

    cdf = country_df.drop(["Entity", "Code"], axis=1).set_index("Year")
    country_list = cdf.values.tolist()
    if len(country_list) < 1:
        return {"Message": "Country {} not found".format(country), "Error": HttpErrors.NOT_FOUND}

    parsed = loads(cdf.to_json(orient="index"))

    return {"Message": "Data from country `{}`".format(country), "Data": parsed}

def get_data_from_year(year: int):
    global df

    if df.empty:
        return {"Message": "Error: df is not initialized", "Error": HttpErrors.INTERNAL_SERVER_ERROR}

    year_df= df[df["Year"] == year]

    ydf = year_df.drop(["Year", "Code"], axis=1).set_index("Entity")

    year_list= ydf.values.tolist()
    if len(year_list) < 1:
        return {"Message": "Year {} not registered".format(year), "Error": HttpErrors.NOT_FOUND}

    parsed = loads(ydf.to_json(orient="index"))

    return {"Message": "Data from Year`{}`".format(year), "Data": parsed}

def get_data_from_country_year(country: str, year: int):
    global df

    if df.empty:
        return {"Message": "Error: df is not initialized", "Error": HttpErrors.INTERNAL_SERVER_ERROR }

    if type(country) != str or type(year) != int:
        return {"Message": "Country must be a string of characters and Year an integer", "Error": HttpErrors.BAD_REQUEST}

    year_df= df[df["Entity"] == country]
    if len(year_df.values.tolist()) < 1:
        return {"Message": "Country {} not found".format(country), "Error": HttpErrors.NOT_FOUND}

    yc_df= year_df[year_df["Year"] == year] 
    if len(yc_df.values.tolist()) < 1:
        return {"Message": "Year {} not registered".format(year), "Error": HttpErrors.NOT_FOUND}

    ycdf = yc_df.drop(["Year", "Code"], axis=1).set_index("Entity").to_json(orient="index")
    parsed = loads(ycdf)

    return {"Message": "Data from Country {} and Year {}".format(country, year), "Data": parsed}


def get_total_internet_users_per_year(year: int):
    global df

    if df.empty:
        return {"Message": "Error: df is not initialized", "Error": HttpErrors.INTERNAL_SERVER_ERROR }

    if type(year) != int:
        return {"Message": "Year must be an integer", "Error": HttpErrors.BAD_REQUEST}

    yc_df= df[df["Year"] == year] 
    if len(yc_df.values.tolist()) < 1:
        return {"Message": "Year {} not registered".format(year), "Error": HttpErrors.NOT_FOUND}

    #ycdf = yc_df.drop(["Year", "Code"], axis=1).set_index("Entity").to_json(orient="index")
    internet_users =  {"Total": int(yc_df["internet_users_number"].sum()) } 

    return {"Message": "Total Internet users in Year {}".format(year), "Data": internet_users}
    

