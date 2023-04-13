
from train import PredictCharges
from usermodel import UsersData
from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
async def predictMedicalCharges(usr: UsersData):
    
    #Make prediction and return response to client
    response = PredictCharges.make_prediction(PredictCharges.prepare_dataset(usr=usr))

    # Return response
    return response