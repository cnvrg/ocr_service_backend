import unittest
import os
import coloredlogs, logging
import yaml
from yaml.loader import SafeLoader
import json
import requests


clientlogs = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=clientlogs)


def read_test_cfg_info(cfg_file: str) -> dict():

    test_cfg = {}
    with open(cfg_file) as c_info_file:
        test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
    return test_cfg


def read_json_file(json_file_name: str):
    with open(json_file_name) as jf:
        data = json.load(jf)
    return data


class test_ocr_gateway_client(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cfg_path = os.path.dirname(os.path.abspath(__file__))
        # cfg_file = f"{cfg_path}/ocr_client_test_config.yaml"
        # json_validation_file = f"{cfg_path}/results_validation.json"

        ## Read configurations
        # test_cfg = read_test_cfg_info(cfg_file)
        # cls.validation_results = read_json_file(json_file_name=json_validation_file)

        ## save cfg to tester
        # print(f"{type(test_cfg)=}")
        """
        clientlogs.debug(f"{test_cfg=}")
        cls.s3_cfg: dict = test_cfg["ocr_client_cfg"]["s3_info"]
        clientlogs.debug(test_cfg["ocr_client_cfg"]["s3_info"])
        cls.s3_client_obj = grpc_client_base.s3_grpc_client(**cls.s3_cfg)
        cls.httplinks = test_cfg["ocr_client_cfg"]["httplinks"]
        cls.files = test_cfg["ocr_client_cfg"]["files"]
        cls.service_network: dict = test_cfg["ocr_client_cfg"]["service_network"]

        cls.service_network["remote_service_address"] = os.environ.get(
            "OCR_SERVICE_ADDRESS"
        )

        cls.ocr_client_obj = grpc_client_base.ocr_grpc_client(**cls.service_network)
        """

    @unittest.skip(" running one test at time ")
    def test_ocr_REST_sendfile_get_json(self):
        """regest processing pdf file"""

        myurl = "http://172.17.0.3:40051/ocr/extract"
        # files = {"data": ("economics.pdf", open("/cnvrg/economics.pdf", "rb"))}
        files = {"file": (open("/cnvrg/economics.pdf", "rb"))}
        # "filename": "economics.pdf",
        # pyload = json.dumps(files)
        # with open("/cnvrg/economics.pdf", "rb") as pf:
        #    getdata = requests.post(
        #        myurl,
        #        data={"filename": "economics.pdf", "data": pf.read()},
        #        verify=False,
        #    )
        getdata = requests.post(myurl, files=files, stream=True)

        print(getdata.text)

    def test_ocr_REST_sendfile_get_file(self):
        """regest processing pdf file"""

        myurl = "http://172.17.0.3:40051/ocr/extract/file"
        # files = {"data": ("economics.pdf", open("/cnvrg/economics.pdf", "rb"))}
        files = {"file": (open("/cnvrg/economics.pdf", "rb"))}
        # "filename": "economics.pdf",
        # pyload = json.dumps(files)
        # with open("/cnvrg/economics.pdf", "rb") as pf:
        #    getdata = requests.post(
        #        myurl,
        #        data={"filename": "economics.pdf", "data": pf.read()},
        #        verify=False,
        #    )
        getdata = requests.post(myurl, files=files, stream=True)

        print(f"{getdata.text=}")


if __name__ == "__main__":
    clientlogs.setLevel(logging.INFO)

    logformat = logging.Formatter(
        fmt="%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S"
    )

    logstream = logging.StreamHandler()
    logstream.setLevel(logging.INFO)
    logstream.setFormatter(logformat)
    clientlogs.addHandler(logstream)

    unittest.main()
