from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from classes.classes import DialogflowPOST
from functions.DialogflowFunctions import capitalHumanoFunc

app = FastAPI(title="Ralken-SuperAki", version="0.1.0")


## POST method to capture Dialogflow fulfillment request 
## These are being read to get information for paratemers and such
## JSON structure are as shown in txt document "DialogflowJSONStructure.txt"
## Data classes are being retrieve as responseID and queryResult as per Dialogflow call

## Webhook for SuperAki's Human Resources
@app.post('/webhook-capital-humano', description="Webhook para capital humano")
async def webhook(request: Request):
    request_data = await request.json()
    webhook_request = DialogflowPOST(**request_data)
    
    response_data = await capitalHumanoFunc(webhook_request.responseId, webhook_request.queryResult)
    
    return JSONResponse(content=response_data)
    
## Webhook for SuperAki's customer service    
@app.post('/webhook-servicio-cliente', description="Webhook para servicio al cliente")
async def webhook(request: Request):
    request_data = await request.json()
    webhook_request = DialogflowPOST(**request_data)