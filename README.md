# services-api
The REST API responsible for enabling shops to manage their services offerings and users to search them

## Running locally ##

1 - To run this API locally you should first create a python virtual environment with:

```
$ python3.7 -m venv venv
```

2 - And then enter it:

```
$ source venv/bin/activate
```

3 - Now you can install the project's dependencies:

```
$ pip install -r requirements.txt
```

4 - Fill the .env file with the environment variables and theirs values; the variables you'll need are in the .env-example file; Export them using:

```
$ export $(cat .env | xargs)
```

5 - Finally, start the application:

```
$ python3.7 -m services.app
```

# Use cases and endpoints #

## Search ##
`GET /search?service_name=<blank, partial or exact name>` 

*Responses*

`200 OK`

Returns list of services matching the query (If blank, returns all services on DB)

```JSON
[
    {
        "_id": "5f9d6594448854f39b13d386",
        "service_name": "Banho",
        "available_in": [
            {
                "petshop_username": "petxuser123",
                "petshop_name": "PetX Centro"
            },
            {
                "petshop_username": "petxuser456",
                "petshop_name": "PetX Osasco"
            },
            {
                "petshop_username": "petxuser789",
                "petshop_name": "PetX Diadema"
            }
        ]
    },
    {
        "_id": "5f9d66d36dd2f5650c0fb8f8",
        "service_name": "Exame de sangue",
        "available_in": [
            {
                "petshop_username": "petxuser123",
                "petshop_name": "PetX Centro"
            }
        ]
    },
    {
        "_id": "5f9d66f26dd2f5650c0fb8f9",
        "service_name": "Vacina contra raiva",
        "available_in": [
            {
                "petshop_username": "petxuser456",
                "petshop_name": "PetX Osasco"
            }
        ]
    }
]
```

`403 Forbidden`

Returns forbidden code if search contains special characters like {} that could be used for attacking the database

```JSON
Invalid service name
```

`404 Not found`

Returns not found code if search doesn't match any services on DB

```JSON
Service not found
```

## Service Creation ##
`POST /manage`

*Request body:*
Form data
```
service_name: "Banho"
```

*Responses:*

`200 OK`

Returns newly created service's id

```JSON
"5f9d6594448854f39b13d386"
```

`403 Forbidden`

Returns forbidden code if name sent by the user contains invalid characters (anything that is not a letter or blank space) 

```JSON
Invalid service name
```

`409 Conflict`

Returns conflict code if service already exists

```JSON
Service already exists
```

## Petshop Addition ##
`PUT /manage`

*Request body:*
Form data
```
petshop_name: "PetX Osasco"
petshop_username: "petxuser456"
service_id: "5f9d6594448854f39b13d386"
```

*Responses:*

`200 OK`

Returns updated service object

```JSON
{
    "_id": "5f9d6594448854f39b13d386",
    "available_in": [
        {
            "petshop_name": "PetX Osasco",
            "petshop_username": "petxuser456"
        }
    ],
    "service_name": "Banho"
}
```

`409 Conflict`

Returns conflict code if service doesn't exist

```JSON
No such object in collection
```

## Petshop Removal ##
`DELETE /manage?petshop_username="petshop_username"&service_id="5f9d6594448854f39b13d386"`

*Responses:*

`200 OK`

Returns updated service object (without the sender in the available_in list)

```JSON
{
    "_id": "5f9d6594448854f39b13d386",
    "available_in": [
        {
            "petshop_name": "PetX Osasco",
            "petshop_username": "petxuser456"
        }
    ],
    "service_name": "Banho"
}
```

`205 Reset Content`

If the "available_in" list becomes empty after the request's processing it means no other petshops provide that service and it is completely deleted from the database

```JSON
No other providers, service deleted.
```

`409 Conflict`

Returns conflict code if service doesn't exist

```JSON
No such object in collection
```
