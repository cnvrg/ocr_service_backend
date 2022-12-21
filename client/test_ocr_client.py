import unittest
import os
import yaml
from yaml.loader import SafeLoader
import json
import grpc_client_base


def read_test_cfg_info(cfg_file: str) -> dict():

    test_cfg = {}
    with open(cfg_file) as c_info_file:
        test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
    return test_cfg


def read_json_file(json_file_name: str):
    with open(json_file_name) as jf:
        data = json.load(jf)
    return data


    

class test_ocr_client(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = f"{cfg_path}/ocr_client_test_config.yaml"
        json_validation_file = f"{cfg_path}/results_validation.json"

        ## Read configurations
        test_cfg = read_test_cfg_info(cfg_file)
        cls.validation_results = read_json_file(json_file_name=json_validation_file)

        ## save cfg to tester
        # print(f"{type(test_cfg)=}")
        print(f"{test_cfg=}")
        cls.s3_cfg: dict = test_cfg["ocr_client_cfg"]["s3_info"]
        print(test_cfg["ocr_client_cfg"]["s3_info"])
        cls.s3_client_obj = grpc_client_base.s3_grpc_client(**cls.s3_cfg)
        cls.httplinks = test_cfg["ocr_client_cfg"]["httplinks"]
        cls.files = test_cfg["ocr_client_cfg"]["files"]
        cls.service_network: dict = test_cfg["ocr_client_cfg"]["service_network"]
        
        cls.service_network['remote_service_address'] = os.environ.get('OCR_SERVICE_ADDRESS')

        cls.ocr_client_obj = grpc_client_base.ocr_grpc_client(**cls.service_network)

    @unittest.skip(" running one test at time ")
    def test_ocr_s3_processing(self):
        """request OCR service to download S3 pdf and process them"""
        actual_results_file = self.ocr_client_obj.process_S3_files(self.s3_cfg)

        actual_results = read_json_file(actual_results_file)

        self.assertEqual(self.validation_results, actual_results)

    @unittest.skip(" running one test at time ")
    def test_ocr_httplinks_processing(self):
        """request OCR service to download puplic pdf from httplink and process them"""
        actual_results_file = self.ocr_client_obj.process_http_files(self.httplinks)

        actual_results = read_json_file(actual_results_file)

        self.assertEqual(self.validation_results, actual_results)

    @unittest.skip(" running one test at time ")
    def test_ocr_shared_files_processing(self):
        """Request OCR service to process files located in shared file system"""

        actual_results_file = self.ocr_client_obj.process_shared_files(self.files)

        actual_results = read_json_file(actual_results_file)

        self.assertEqual(self.validation_results, actual_results)

    # @unittest.skip(" running one test at time ")
    def test_uploaded_files(self):
        """bidirectional stream: upload pdf files to OCR service for processing"""
        actual_results_file = self.ocr_client_obj.process_uploaded_files(self.files)

        actual_results = read_json_file(actual_results_file)

        self.assertEqual(self.validation_results, actual_results)


if __name__ == "__main__":
    unittest.main()
