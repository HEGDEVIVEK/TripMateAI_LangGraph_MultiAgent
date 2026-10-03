import os
import requests

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("bro it is working")

llm_model = init_chat_model("gpt-5-nano")

class llm_schema(BaseModel):
    dep_iata: str | None = Field(
        description="Departure airport code: exactly 3 uppercase letters, such as BLR. Return null if missing or ambiguous.",
        pattern=r"^[A-Z]{3}$"
    )

    arr_iata: str | None = Field(
        description="Arrival airport code: exactly 3 uppercase letters, such as DEL. Return null if missing or ambiguous.",
        pattern=r"^[A-Z]{3}$"
    )

    limit: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum flight records to return. Use 3 if unspecified."
    )

llm_with_structure = llm_model.with_structured_output(llm_schema)

def aviationStack_tool(question:str):

    api_key = os.getenv("AVIATIONSTACK_API_KEY")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the departure airport, arrival airport, and limit."
        "Convert unambiguous city names to airport IATA codes."
        "Return null for missing or ambiguous airports."
        "Use a limit of 3 unless specified; keep it between 1 and 10."),
        ("human", "{question}"),
    ])

    chain = prompt | llm_with_structure
    parametrs = chain.invoke({"question" : question})

    params = {
        "access_key" : api_key,
        "dep_iata" : parametrs.dep_iata,
        "arr_iata" : parametrs.arr_iata,
        "limit" : parametrs.limit
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
    
    



    


