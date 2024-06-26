from fastapi import APIRouter, HTTPException, Request
from routes.jwt_token import  Depends, get_user_by, datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from models.models import Shipment_input
from database.database import shipment_data
from fastapi.templating import Jinja2Templates 


route = APIRouter()
html = Jinja2Templates(directory="Html")
route.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")


@route.get("/Newshipment")
def shipment(request : Request):
    return html.TemplateResponse("newshipment.html", {"request" : request})

@route.post("/Newshipment")
def new_data(request : Request, shipment : Shipment_input, current_user:str = Depends(get_user_by)):
   
    try :
        #checking if the length of shipment number is equal to 7
        if not len(str(shipment.Shipment_Number)) == 7 :
            raise HTTPException(status_code=400, detail="Shipment_Number must be 7 Characters")
        
        #checking all values are filled or not?
        if any(value == "" for value in shipment.dict().values()):
            raise HTTPException(status_code=400, detail="Please fill all values")
        
        existing_data = shipment_data.find_one({"Shipment_Number" : shipment.Shipment_Number })
       
        if existing_data:
            raise HTTPException(status_code=400, detail="Shipment_Number already used")
        
        # Validate expected_delivery date format and presence
        Expected_delivery_date_str = shipment.Expected_Delivery_Date
        if not Expected_delivery_date_str:
            raise HTTPException(status_code=400, detail="Expected delivery date is required")
        
        if current_user :
            Shipment = {
                "Username":current_user["Username"],
                "Shipment_Number": shipment.Shipment_Number,
                "Route_Details":shipment.Route_Details,
                "Device":shipment.Device,
                "PO_Number":shipment.PO_Number,
                "NDC_Number":shipment.NDC_Number,
                "Serial_no_Goods":shipment.Container_Number,
                "Container_Number":shipment.Container_Number,
                "Goods_Type":shipment.Goods_Type,
                "Expected_Delivery_Date":shipment.Expected_Delivery_Date,
                "Delivery_Number":shipment.Delivery_Number,
                "Batch_id":shipment.Batch_id,
                "Comment":shipment.Comment
            }

           
        shipment_data.insert_one(Shipment)
        return JSONResponse(content={"message" : "Shipment Created Successfully"}, status_code=200)
    except HTTPException as error:
        return JSONResponse(content={"message" : error.detail}, status_code=error.status_code)
    except Exception as x:
        return JSONResponse(content={"message" : x}, status_code=500)

       