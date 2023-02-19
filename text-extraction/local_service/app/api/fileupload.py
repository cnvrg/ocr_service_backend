from pathlib import Path
from predict import predict
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import ORJSONResponse, FileResponse
from starlette.background import BackgroundTasks
from local_service.app.api.models import InferenceResults, InferenceIn, InferenceOut
from inference.predict import predict
from typing import BinaryIO, List
from datetime import datetime
import coloredlogs, logging
import shutil
import json

import os


class FileUploadLogger:
    
    def __init__(self):
        self.fileUploadlogs = logging.getLogger(__name__)
        coloredlogs.install(level=logging.DEBUG, logger=self.fileUploadlogs)

        self.fileUploadlogs.setLevel(logging.DEBUG)

        logfile = logging.FileHandler(filename=self.get_logfile_path("ocr_rest_service.log"))
        logfile.setLevel(logging.DEBUG)
        logformat = logging.Formatter(fmt="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
        logfile.setFormatter(logformat)
        self.fileUploadlogs.addHandler(logfile)

        logstream = logging.StreamHandler()
        #logstream.setLevel(logging.INFO)
        logstream.setLevel(logging.DEBUG)
        logstream.setFormatter(logformat)
        self.fileUploadlogs.addHandler(logstream)
    
    def getLogger(self):
        return self.fileUploadlogs
    
    def get_logfile_path(self, logfile_name:str) -> str:
        logdir: str = os.path.dirname(os.path.abspath(__file__))
        file_name: str =  f"{logdir}/../../logs/{logfile_name}"
        filep = Path(file_name)
        # Create the file if not present 
        #filep.touch(exist_ok=True)
        filep.touch()
        return file_name

router = APIRouter(prefix="/ocr",
                   responses={404: {
                       "description": "File not found"
                   }})

routerLoger = FileUploadLogger()

def makeLocalWorkingDir(prefix="upload", wdir="/tmp") -> str:
    """local helper function for makring local directory"""
    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    dir_name = f"{wdir}/{prefix}-{timestamp}"

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    return dir_name

def saveFileLocally(wireFile: UploadFile) -> str:
    localFile = f"{makeLocalWorkingDir()}/{wireFile.filename}"
    routerLoger.getLogger().debug(f"Saving {wireFile.filename} to {localFile=}")
    with open(localFile, "wb+") as saveFile:
        shutil.copyfileobj(wireFile.file, saveFile)
    
    return localFile

def savePredictionResults(results: dict, name_prefix='text') -> str:
    json_pred = json.dumps(results, indent=4)

    ##fileUploadlogs.debug(f"{json_pred=}")
    results_dir = makeLocalWorkingDir(prefix="ocrResults", wdir="/tmp")
    results_file = f"{results_dir}/{name_prefix}_results.json"

    with open(results_file, "w") as rf:
        rf.write(json_pred)    
    
    return results_file

def cleanup_files(file_path:str):
    dir_name = os.path.dirname(file_path)
    shutil.rmtree(dir_name)
    
@router.post('/extract', response_class=ORJSONResponse)
async def handle_file_upload_1(file: UploadFile):
    """ base prediction endpoint handler, return results as json text"""
    working_filename_name = saveFileLocally(file)
        
    data = dict(pdf= [working_filename_name])
    prediction = predict(data)    

    cleanup_files(working_filename_name)

    routerLoger.getLogger().info(f"{working_filename_name }Text extraction completed! returning results")
    return prediction

@router.post('/extract/file', response_class=FileResponse)
async def handle_file_upload_2(file: UploadFile):
    """ base prediction endpoint handler, return results file"""
    working_filename_name = saveFileLocally(file)
        
    data = dict(pdf= [working_filename_name])
    prediction = predict(data)    

    resultsFile = savePredictionResults(prediction, file.filename.split('.')[0])

    cleanup_files(working_filename_name)

    routerLoger.getLogger().debug(f'{resultsFile}')

    BackgroundTasks.add_task(cleanup_files, resultsFile)
    return resultsFile

@router.post('/extract/files', response_class=FileResponse)
async def handle_file_upload_3(files: List[UploadFile]):
    """ base prediction endpoint handler for multifile upload. """
    
    file_names = [saveFileLocally(fitem) for fitem in files ]
    routerLoger.getLogger().info(f"{file_names}")
    data = dict(pdf= file_names)
    prediction = predict(data)    

    cleanup_files(file_names[0]) 

    resultsFile = savePredictionResults(prediction)

    routerLoger.getLogger().debug(f'{resultsFile}')
    
    BackgroundTasks.add_task(cleanup_files, resultsFile)
    return resultsFile
