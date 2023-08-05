from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import gammu

# Define the FastAPI app
app = FastAPI()

# Initialize the gammu state machine
sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()

# SMS database
sms_db = []

# SMS response class
class SmsResponse(BaseModel):
    plate_number: str
    car_brand: str
    color: str
    model_year: int
    taxes_paid: bool
    first_day_in_traffic: str
    car_owner: str
    car_owner_residence: str

# SMS class
class Sms(BaseModel):
    number: str
    text: str

# Status class
class Status(BaseModel):
    status: str

# Receive SMS
@app.get("/receivesms", response_model=List[SmsResponse])
async def receive_sms():
    # Get all SMS from the gammu state machine
    sms_list = sm.GetSMS()

    # Create a list to store the parsed SMS
    parsed_sms = []

    # Loop through all SMS
    for sms in sms_list:
        # Get the SMS text
        text = sms['Text']

        # Split the text into components
        components = text.split(',')

        # Create an SmsResponse object from the components
        response = SmsResponse(
            plate_number=components[0],
            car_brand=components[2],
            color=components[3],
            model_year=int(components[4]),
            taxes_paid=components[5] == 'ITRAFIK',
            first_day_in_traffic=components[6],
            car_owner=components[7],
            car_owner_residence=components[8]
        )

        # Add the parsed SMS to the list
        parsed_sms.append(response)

    # Return the list of parsed SMS
    return parsed_sms

# Send SMS
@app.post("/sendsms")
async def send_sms(sms: Sms):
    # Create the SMS data
    sms_data = {
        'Text': sms.text,
        'SMSC': {'Location': 1},
        'Number': sms.number,
    }

    # Send the SMS
    sm.SendSMS(sms_data)

# Service status
@app.get("/status", response_model=Status)
async def status():
    # Check if the gammu state machine is initialized
    if sm.IsConnected():
        # Return the service status
        return Status(status="The service is up and running")
    else:
        return Status(status="The service is not running")
