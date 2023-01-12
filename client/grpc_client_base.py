""" grpc base client class """
from datetime import datetime
from typing import List
from dataclasses import dataclass, field, asdict, replace
import grpc
import local_service.local_grpc.ocrservice_pb2 as ocrservice_pb2
import local_service.local_grpc.ocrservice_pb2_grpc as ocrservice_pb2_grpc
import local_service.local_grpc.s3connect_pb2 as s3connect_pb2
import local_service.local_grpc.s3connect_pb2_grpc as s3connect_pb2_grpc
from base_logger import BaseClient


class s3_grpc_client(BaseClient):
    def __init__(
        self,
        endpoint=None,
        command=None,
        bucketname=None,
        download_dir=None,
        prefix=None,
        file=None,
        key_id=None,
        secret_key=None,
        remote_service_address=None,
        remote_service_port=None,
    ):

        super().__init__(remote_service_address, remote_service_port)
        self.locallogger.debug("s3_client called")
        self.endpoint = endpoint if endpoint is not None else "http://s3.amazonaws.com"
        self.command = command if command is not None else "download"
        self.localdir = download_dir if download_dir is not None else "/cnvrg"
        self.bucketname = bucketname

        self.prefix = prefix
        self.file = file

        self.key_id = key_id
        self.secret_key = secret_key

        ## Update remote service address and port if provided.
        if remote_service_address is not None:
            self.remote_service_address = remote_service_address
        if remote_service_port is not None:
            self.remote_service_port = remote_service_port

        self.remote_endpoint_address = (
            f"{self.remote_service_address}:{self.remote_service_port}"
        )

        self.locallogger.info(f"{self.endpoint=}")
        self.locallogger.info(f"{self.command=}")
        self.locallogger.info(f"{self.bucketname=}")
        self.locallogger.info(f"{self.localdir=}")
        self.locallogger.info(f"{self.prefix=}")
        self.locallogger.info(f"{self.file=}")
        self.locallogger.info(f"{self.key_id=}")

    def build_S3regquest_msg(self):
        req: s3connect_pb2.S3request = s3connect_pb2.S3request()
        req.args.endpoint = self.endpoint
        req.args.command = self.command
        req.args.bucketname = self.bucketname
        req.args.localdir = self.localdir
        req.args.prefix = self.prefix

        req.env.aws_access_key_id = self.key_id
        req.env.aws_secret_access_key = self.secret_key

        return req

    def download_to_location(self, stub: s3connect_pb2_grpc.s3connectStub):
        """Request download from S3 to be placed in shared location 'localdir'"""

        res = stub.DownloadFilesToLocation(self.build_S3regquest_msg())

        self.locallogger.info(res)

    def download_files(self, stub: s3connect_pb2_grpc.s3connectStub):
        """Request download from S3 and accept these files via server stream"""

        file_path = self.makeLocalWorkingDir(prefix="s3Download", wdir="tmp")
        files: List[str] = []
        for res in stub.GetFiles(self.build_S3regquest_msg()):
            if res.filename:
                self.locallogger.info(f"{res.filename=}")
                filename = f"{file_path}/{res.filename}"
                files.append(filename)
            else:
                with open(filename, "ab") as rf:
                    rf.write(res.data)

        self.locallogger.info(f"Received: {files}")

    def download_to_shared(self):
        """request files to be download to shared location"""
        with grpc.insecure_channel(self.remote_endpoint_address) as channel:
            stub = s3connect_pb2_grpc.s3connectStub(channel)
            self.locallogger.info("---downloading files to shared location---")
            self.download_to_location(stub)

    def download_to_stream(self):
        """request downloaded files to be streamed back to client"""
        with grpc.insecure_channel(self.remote_endpoint_address) as channel:
            stub = s3connect_pb2_grpc.s3connectStub(channel)
            self.locallogger.info("---streamming requested files---")
            self.download_files(stub)


class OcrGrpcClient(BaseClient):
    def __init__(self, remote_service_address, remote_service_port):
        super().__init__(remote_service_address, remote_service_port)
        self.remote_endpoint_address = (
            f"{self.remote_service_address}:{self.remote_service_port}"
        )

    def get_inference_results_s3(
        self, s3_args: dict, stub: ocrservice_pb2_grpc.ocrserviceStub
    ):
        """request inference on an S3 files"""
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        ## Build OCR request message

        req: ocrservice_pb2.S3request = ocrservice_pb2.S3request()
        req.args.endpoint = s3_args["endpoint"]
        req.args.command = s3_args["command"]
        req.args.bucketname = s3_args["bucketname"]
        req.args.localdir = s3_args["download_dir"]
        req.args.prefix = s3_args["prefix"]

        ocrreq = ocrservice_pb2.OCRrequestInference()
        ocrreq.s3Info.CopyFrom(req)

        self.locallogger.info(
            "----------send request for S3 files inference------------"
        )
        for seq in stub.ProcessInfra(ocrreq):

            with open(results_file, "ab") as rf:
                rf.write(seq.data)

        self.locallogger.info(
            f"-----------received: {results_file} -------------------"
        )
        return results_file

    def get_inference_results_httplink(
        self, httplinks: List[str], stub: ocrservice_pb2_grpc.ocrserviceStub
    ):
        """Request inference on public http downloadable files"""
        # http_files = [
        #    "https://libhub-readme.s3.us-west-2.amazonaws.com/pdf_extraction_data/Data+science.pdf",
        #    "https://libhub-readme.s3.us-west-2.amazonaws.com/pdf_extraction_data/economics.pdf",
        # ]

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"
        ## Build proto request message ##
        ocrreq = ocrservice_pb2.OCRrequestInference()
        ocrreq.httplink.extend(httplinks)

        self.locallogger.info(
            "----------send request for httpLink files inference------------"
        )
        for seq in stub.ProcessInfra(ocrreq):

            with open(results_file, "ab") as rf:
                rf.write(seq.data)

        self.locallogger.info(
            f"-----------received: {results_file} -------------------"
        )

        return results_file

    def get_inference_results_shared(
        self, shared_files: List[str], stub: ocrservice_pb2_grpc.ocrserviceStub
    ):
        """Request inference on files already present on shared volume"""

        # shared_files = [
        #    "/cnvrg/Datascience.pdf",
        #    "/cnvrg/economics.pdf",
        # ]

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"

        ## Build proto request message ##
        ocrreq = ocrservice_pb2.OCRrequestInference()
        ocrreq.filename.extend(shared_files)

        self.locallogger.info(
            "----------send request for shared files inference------------"
        )
        for seq in stub.ProcessInfra(ocrreq):

            with open(results_file, "ab") as rf:
                rf.write(seq.data)

        self.locallogger.info(
            f"-----------received: {results_file} -------------------"
        )
        return results_file

    def upload_files_iter(self, files: List[str]):
        """iterator helper function for uploading files to server directly"""

        segment_size = 1024
        for file in files:
            file_name_no_path = file.split("/")[-1]
            # send file name first
            self.locallogger.info(f"uploading {file=}, {file_name_no_path=}")
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

    def get_inference_results_uploadFiles(
        self, files: List[str], stub: ocrservice_pb2_grpc.ocrserviceStub
    ):

        """Request inference on files uploaded directly by this client"""

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        results_file = f"results-{timestamp}.json"

        # files = [
        #    "/cnvrg/Datascience.pdf",
        #    "/cnvrg/economics.pdf",
        # ]

        self.locallogger.info("----------upload files and get response ------------")
        for seq in stub.ProcessUpload(self.upload_files_iter(files=files)):

            with open(results_file, "ab") as rf:
                rf.write(seq.data)

        self.locallogger.info(
            f"-----------received: {results_file} -------------------"
        )
        return results_file

    def process_S3_files(self, s3_args: dict):
        """handle S3 files inference request"""

        with grpc.insecure_channel(self.remote_endpoint_address) as channel:
            stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
            self.locallogger.info(
                "-------------- requesting s3 files for inference --------------"
            )
            results_file = self.get_inference_results_s3(s3_args, stub)

        return results_file

    def process_http_files(self, httplinks: List[str]):
        """handle http files inference request"""

        with grpc.insecure_channel(self.remote_endpoint_address) as channel:
            stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
            self.locallogger.info(
                "-----------sending files as http link --------------"
            )
            results_file = self.get_inference_results_httplink(httplinks, stub)

        return results_file

    def process_uploaded_files(self, files: List[str]):
        """handle direct file upload for inference request"""

        with grpc.insecure_channel(self.remote_endpoint_address) as channel:
            stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
            self.locallogger.info(
                "------------upload files for inference  --------------"
            )
            results_file = self.get_inference_results_uploadFiles(files, stub)

        return results_file

    def process_shared_files(self, files: List[str]):
        """handle shared files inference request"""

        with grpc.insecure_channel(self.remote_endpoint_address) as channel:
            stub = ocrservice_pb2_grpc.ocrserviceStub(channel)
            self.locallogger.info(
                "------------upload files for inference  --------------"
            )
            results_file = self.get_inference_results_shared(files, stub)

        return results_file
