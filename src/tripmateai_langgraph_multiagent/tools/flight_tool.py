import os
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def aviationStack_tool(dep_iata:str, arr_iata:str, limit:int):

    """Fetch flight records using departure and arrival IATA codes and a result limit."""
    
    api_key = os.getenv("AVIATIONSTACK_API_KEY")

    params = {
        "access_key" : api_key,
        "dep_iata" : dep_iata,
        "arr_iata" : arr_iata,
        "limit" : limit
    }

    response = requests.get("http://api.aviationstack.com/v1/flights", params=params)
    response = response.json()

    result = []

    for item in response.get("data", []):
        departure = item.get("departure", {})
        arrival = item.get("arrival", {})
        airline = item.get("airline", {})
        flight = item.get("flight", {})
        
        flight_details = {
            "airline" : airline.get("name"),
            "flight_number" : flight.get("number"),
            "departure_airport" : departure.get("airport"),
            "arrival_airport" : arrival.get("airport"),
            "scheduled_departure" : departure.get("scheduled"),
            "scheduled_arrival" : arrival.get("scheduled"),
            "flight_status" : item.get("flight_status"),  
        }
        
        result.append(flight_details)

    return result
    
    



    


