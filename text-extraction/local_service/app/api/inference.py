from predict import predict
from fastapi import APIRouter
from local_service.app.api.models import InferenceResults, InferenceIn, InferenceOut
from inference.predict import predict

router = APIRouter(prefix="/extract",
                   responses={404: {
                       "description": "File not found"
                   }})

@router.post('/', response_model=InferenceOut)
async def get_predict(payload: InferenceIn):
    """ base prediction endpoint handler"""
    data = dict(pdf=payload.remote_files)
    prediction = predict(data)    
    
    response_dict = {'json_extract_results': prediction} 
    infr_results = InferenceResults(**response_dict)
    return InferenceOut(info=payload, results=infr_results)