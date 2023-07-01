# Python imports
from collections import defaultdict

# FastAPI imports
from typing import Union
from fastapi import  FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# CORS
from fastapi.middleware.cors import CORSMiddleware

### Project files import
import Database as d
from Constants import *

# Initialization
app = FastAPI(docs_url="/docs", redoc_url=None)

# CORS
origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:*"
        ]

app.add_middleware(
        CORSMiddleware, 
        allow_origins = origins,
        allow_credentials= True,
        allow_methods= ["*"],
        allow_headers= ["*"],
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                {"Detail": "Invalid request", "Errors": reformatted_message}
                ),
            )


d.init_data()

responses = {
        500 : {"description": "Internal server error", "content": {"application/json" : {"schema": ErrorResponseModel.schema()}}},
        }

@app.get( '/countries',
        summary="Gets a list of all countries",
        description="Get a list of all countries",
        response_model = Union[Countries,ErrorResponseModel],
        responses={ **responses,
                   200 : {"description": "List containing all countries"},
                },
        )
def get_countries(response: Response):
    res = d.get_countries()
    if "Error" in res:
        response.status_code = res["Error"].value

    return d.get_countries()

@app.get(
        "/country/{country_name}",
        summary="Gets data from a country",
        description="Gets data of all years for the country with name **country_name**",
        response_model = Union[CountryDataPerModel, ErrorResponseModel],
        responses={
            **responses,
            200: {"description": "Data related to the country **country_name**"},
            404: {"description": "The country name **country_name** parameter has not been found on the database.", "content": {"application/json": {"schema": ErrorResponseModel.schema()}}},
            }
        )
def get_data_from_country(country_name: str, response: Response):
    res = d.get_data_from_country(country_name)
    if "Error" in res:
        response.status_code = res["Error"].value
    return res

@app.get(
        '/country/{country_name}/year/{year}',
        summary="Gets data from an specific country for an specific year",
        description="Gets data from the country with name **country_name** for an specific year **year**",
        response_model = Union[CountryDataPerModel, ErrorResponseModel],
        responses={
            **responses,
            200: {"description": "Data related to the country **country_name** for the year **year**"},
            404: {"description": "The country name **country_name** parameter or year **year** has not been found on the database.","content": {"application/json": {"schema": ErrorResponseModel.schema()}}},
            }
        )
def get_data_from_country_year(country_name: str, year: int, response: Response):
    res = d.get_data_from_country_year(country_name, year)
    if "Error" in res:
        response.status_code = res["Error"].value
    return res 

@app.get(
        '/year/{year}',
        summary="Gets all countries data during an specific year",
        description="Gets data of an specific year **year** for all the countries",
        response_model = Union[CountryDataPerModel, ErrorResponseModel],
        responses={
            **responses,
            200: {"description": "Data related to the year **year** for all countries"},
            404: {"description": "The year **year** parameter has not been found on the database.", "content": {"application/json": {"schema": ErrorResponseModel.schema()}}},
            }
        )
def get_data_from_countries(year: int, response: Response):
    res = d.get_data_from_year(year)
    if "Error" in res:
        print(res)
        response.status_code = res["Error"].value
    return res

@app.get(
        '/internet-users/{year}',
        summary="Gets total amount of internet users of all countries per year",
        description="Get the total amount of registered internet users from all contries in an specific year **year**",
        response_model = Union[CountryDataPerModel, ErrorResponseModel],
        responses={
            **responses,
            200: {"description": "Total internet users related to the year **year**"},
            404: {"description": "The year **year** parameter has not been found on the database.", "content": {"application/json": {"schema": ErrorResponseModel.schema()}}},
            }
        )
def get_total_internet_users_per_year(year: int, response: Response):

    res = d.get_total_internet_users_per_year(year)
    if "Error" in res:
        print(res)
        response.status_code = res["Error"].value

    return res
