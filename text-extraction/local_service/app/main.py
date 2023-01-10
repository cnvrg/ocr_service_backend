""" Define the endpoint for this service """
from fastapi import FastAPI
from local_service.app.api import inference, fileupload
description = """
Text-extraction from pdf files
"""
app_info = {'service': "ocr", 'status': 'ready'}

app = FastAPI(
    title="OCR service",
    description=description,
    version="0.1.0",
    contact={
        "name": "suppot person",
        "url": "http://support.blueprint.com/contact/",
        "email": "support@blueprint.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
#app.include_router(inference.router)
app.include_router(fileupload.router)

@app.get("/")
async def home():
    """ return app status """
    return {'ocr': 'ready'}
