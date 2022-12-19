""" ocr client rpc calls """
from concurrent import futures
from datetime import datetime
import logging
from typing import List

import grpc
import ocrservice_pb2
import ocrservice_pb2_grpc


def get_inference_results_s3(stub: ocrservice_pb2_grpc.ocrserviceStub):
    """request inference on an S3 files"""
    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    results_file = f"results-{timestamp}.json"

    ## Build S3 request message
    s3req = ocrservice_pb2.S3request()
    s3req.args.endpoint = "http://s3.amazonaws.com"
    s3req.args.command = "download"
    s3req.args.bucketname = "libhub-readme"
    s3req.args.localdir = "/cnvrg"
    s3req.args.prefix = "pdf_extraction_data/"

    s3req.env.aws_access_key_id = "some__ID__ID"
    s3req.env.aws_secret_access_key = "some_secret_secret"

    ## Build OCR request message
    ocrreq = ocrservice_pb2.OCRrequestInference()
    ocrreq.s3Info.CopyFrom(s3req)

    print("----------send request for S3 files inference------------")
    for seq in stub.ProcessInfra(ocrreq):

        with open(results_file, "ab") as rf:
            rf.write(seq.data)

    print(f"-----------received: {results_file} -------------------")


def get_inference_results_httplink(stub: ocrservice_pb2_grpc.ocrserviceStub):
    """Request inference on public http downloadable files"""
    http_files = [
        "https://libhub-readme.s3.us-west-2.amazonaws.com/pdf_extraction_data/Data+science.pdf",
        "https://libhub-readme.s3.us-west-2.amazonaws.com/pdf_extraction_data/economics.pdf",
    ]

    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    results_file = f"results-{timestamp}.json"

    ## Build proto request message ##
    ocrreq = ocrservice_pb2.OCRrequestInference()
    ocrreq.httplink.extend(http_files)

    print("----------send request for httpLink files inference------------")
    for seq in stub.ProcessInfra(ocrreq):

        with open(results_file, "ab") as rf:
            rf.write(seq.data)

    print(f"-----------received: {results_file} -------------------")


def get_inference_results_shared(stub: ocrservice_pb2_grpc.ocrserviceStub):
    """Request inference on files already present on shared volume"""

    shared_files = [
        "/cnvrg/Datascience.pdf",
        "/cnvrg/economics.pdf",
    ]

    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    results_file = f"results-{timestamp}.json"

    ## Build proto request message ##
    ocrreq = ocrservice_pb2.OCRrequestInference()
    ocrreq.filename.extend(shared_files)

    print("----------send request for shared files inference------------")
    for seq in stub.ProcessInfra(ocrreq):

        with open(results_file, "ab") as rf:
            rf.write(seq.data)

    print(f"-----------received: {results_file} -------------------")


def upload_files_iter(files: List[str]):
    """iterator helper function for uploading files to server directly"""

    segment_size = 1024
    for file in files:
        file_name_no_path = file.split("/")[-1]
        # send file name first
        print(f"uploading {file=}, {file_name_no_path=}")
        yield ocrservice_pb2.OCRuploadFiles(filename=file_name_no_path)
        # Then stream the file it self
        with open(file, mode="rb") as fs:
            streaming_on = True
            while streaming_on:
                segment = fs.read(segment_size)
                if segment:
                    entry_request = ocrservice_pb2.OCRuploadFiles(data=segment)
                    yield entry_request
                else:
                    streaming_on = False
    return


def get_inference_results_uploadFiles(stub: ocrservice_pb2_grpc.ocrserviceStub):
    """Request inference on files uploaded directly by this client"""

    timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    results_file = f"results-{timestamp}.json"

    files = [
        "/cnvrg/Datascience.pdf",
        "/cnvrg/economics.pdf",
    ]

    print("----------upload files and get response ------------")
    for seq in stub.ProcessUpload(upload_files_iter(files=files)):

        with open(results_file, "ab") as rf:
            rf.write(seq.data)

    print(f"-----------received: {results_file} -------------------")


def process_S3_files():
    """handle S3 files inference request"""

    with grpc.insecure_channel("localhost:50052") as channel:
        stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
        print("-------------- requesting s3 files for inference --------------")
        get_inference_results_s3(stub)


def process_http_files():
    """handle http files inference request"""

    with grpc.insecure_channel("localhost:50052") as channel:
        stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
        print("-----------sending files as http link --------------")
        get_inference_results_httplink(stub)


def process_uploaded_files():
    """handle S3 direct file upload for inference request"""

    with grpc.insecure_channel("localhost:50052") as channel:
        stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
        print("------------upload files for inference  --------------")
        get_inference_results_uploadFiles(stub)


def process_shared_files():
    """handle shared files inference request"""

    with grpc.insecure_channel("localhost:50052") as channel:
        stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
        print("------------upload files for inference  --------------")
        get_inference_results_shared(stub)


if __name__ == "__main__":
    logging.basicConfig()
    process_S3_files()
