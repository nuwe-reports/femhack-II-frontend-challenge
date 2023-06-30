# The International FemHack II 

## Frontend Challenge

Welcome participants to **The Internation FemHack edition II Frontend Challenge**! :computer:

This document describes how to setup the **backend** server created for this challenge.


## Backend

The **Backend** is the server responsible for managing any dynamic content required by the Frontend. In this case, the backend server provides with world-wide data statistics about Internet.
Specifically, it returns information on the number of users subscribers with Internet access for each country from 1980 to 2020.

### Setup backend

The **Backend** can be setup in two different ways.
For both methods the following commands must be run on the commandline

```bash
# First, clone the repository
# It can also be directly downloaded from the GitHub website.
git clone https://github.com/nuwe-reports/femhack-II-frontend

# Then, change directory into the cloned repository
cd femhack-II-frontend/
```

##### Method 1: Docker

This method builds and runs a **Docker** container exposing the backend server on port `8080`.

**Prerequisites**
- `docker` installed. To install docker follow the [guide](https://docs.docker.com/engine/install/) for your Operating System.
> *Tip*: To make sure you have docker installed run `sudo docker run hello-world`. If it shows a *Hello from Docker!* message it has been installed correctly.


**Setup**

To setup the development environment with docker follow the next commands:
```bash
# MUST BE inside the femhack-II-frontend/ repository!!!
# Building the container
docker build . -t fh-backend

# Running the container detached
docker run -p8080:8080 -d fh-backend 
```

##### Method 2: Python3

This methods uses `Python3` directly to run the backend server application.

**Prerequisites**
- `python3` installed.
- `pip` installed.

It is **recommended** to install everything in a python virtual environment. For that, install `virtualenv`

**Setup**

To setup the development environment with python3 follow the next commands:
```bash
# MUST BE inside the femhack-II-frontend/
# Enter the `backend/` directory
cd backend/

# [OPTIONAL] Use a virtualenv
mkdir backend_env/ # Create directory
virtualenv backend_env/ # Set directory as virtual environment
source backend_env/bin/activate # Activate virtual environment
# --------------

# 1. Install the python packages
pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --port 8080 --reload # On port 8080!
```

##### Is it working?
To check if the backend server is up and running go your web browser (Chrome, Firefox, etc) and go to 
`http://localhost:8080/docs` if you see an endpoint documentation you are good to go! :tada:


### Endpoints Guide

There are 5 endpoints available plus the documentation endpoint:

| Method | URL | Description |
| ----- | --------| ------ |
| `GET` | `/docs` | Swagger documentation. Here you can find ALL the endpoints documentation and test it.|
| `GET` | `/countries` | Returns a list with all the countries |
| `GET` | `/country/{country_name}` | Returns data from the **country_name** passed divided by year. |
| `GET` | `/country/{country_name}/year/{year}` | Returns data from the **country_name** of the specificied **year**. |
| `GET` | `/year/{year}` | Returns data from all countries in the specificed **year**. |
| `GET` | `/internet-users/{year}` | Returns total amount of Internet Users in the world in the specified **year**. |

#### `/countries` 

##### Parameters 
None

##### Response
In JSON format 

Returns **200** and the following JSON:
```jsonc
// Example (/countries)
{
    "Message": "An informative message",
    "Countries" : [
        "A",
        "List",
        "Of",
        "Countries",
    ]
}
```
--- 

#### `/country/{country_name}` 

##### Parameters 
**country_name**: The name of the country.

##### Response

In JSON format

Returns **200** if the **country_name** can be found on the database and the following JSON:
```jsonc
// Example with **country_name** Spain (/country/Spain)
{
    "Message": "Data from country `Spain`"
    "Data": {
        "1980": {
            "internet_users_percentatge" : 0, // Percentatge of Internet Users 
            "internet_users_number" : 0  // Number of users with Internet Access on the country
        },
        "1981": {
            "internet_users_percentatge" : 0,
            "internet_users_number" : 0
        },
        (..)
    }
}
```

Returns **404** if the **country_name** can NOT be found on the database and the following JSON:
```jsonc
// Example with country Test (/country/Test)
{
    "Message": "Country Test not found",
    "Data": {}
}
```

---

#### `/country/{country_name}/year/{year}` 

##### Parameters 
**country_name**: The name of the country.
**year**: The year on which extract the information.

##### Response
In JSON format

Returns **200** if the **country_name** and **year** can be found on the database and the following JSON
```jsonc
// Example with country name Spain and year 1997 (/country/Spain/year/1997)
{
    "Message": "Data from Country Spain and Year 1997"
    "Data": {
        "Spain": {
            "internet_users_percentatge" : 2.803319693, // Percentatge of Internet Users 
            "internet_users_number" : 1126375 // Number of users with Internet Access (Spain)
        }
    }
}
```

Returns **404** if the **country_name** or **year** can NOT be found on the database and the following JSON
```jsonc
// Example with country name Test and year 1970 (/country/Test/year/1970)
{
    "Message": "Country Test not found",
    "Data" : {}
}

// Example with country name Spain and year 1970
{
    "Message": "Year 1970 not registered",
    "Data" : {}
}
```

--- 

#### `/year/{year}` 

##### Parameters 
**country_name**: The name of the country.
**year**: The year on which extract the information.

##### Response
In JSON

Returns **200** if the **year** can be found on the database and the following JSON:
```jsonc
// Example with year 1997 (/year/1997) 
{
    "Message": "Data from Year `1997`",
    "Data": {
        "Afghanistan": {
            "internet_users_percentatge": 0,
            "internet_users_number": 0
        },
        "Albania": {
            "internet_users_percentatge": 0,
            "internet_users_number": 0
        },
        // (...)
    }
}
```
Returns **404** if the **year** can NOT be found on the database and the following JSON:
```jsonc
// Example with year 1954 (/year/1954)
{
    "Message": "Year 1954 not registered",
    "Data": {}
}
```

--- 

#### `/internet-users/{year}` 

##### Parameters 
**year**: The year on which extract the information.

##### Response 
In JSON

Returns **200** if the **year** can NOT be found on the database and the following JSON:
```jsonc
// Example with year 1990 (/internet-users/1990)
{
    "Message": "Total Internet users in Year 1990",
    "Data": {
        "Total": 2586707 // Total of Internet users in 1990 worldwide.
    }
}
```

Returns **404** if the **year** can NOT be found on the database and the following JSON:
```jsonc
// Example with **year** 1954 (/internet-users/1954)
{
    "Message": "Year 1954 not registered",
    "Data" : {}
}
```

---
> Created by NUWE with :heart: 
