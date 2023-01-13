import unittest
import os, yaml, json
import coloredlogs, logging
from yaml.loader import SafeLoader
import json
import rest_client_base
import redis

clientlogs = logging.getLogger(__name__)
coloredlogs.install(level=logging.DEBUG, logger=clientlogs)


def redis_connect():
    # simple redis test
    redis_address = os.environ.get("REDIS_DEPLOYMENT_SERVICE_HOST")
    if not redis_address:
        clientlogs.error("Missing redis address (REDIS_DEPLOYMENT_SERVICE_HOST)")
        return None

    redis_port = os.environ.get("REDIS_DEPLOYMENT_SERVICE_PORT")
    if not redis_port:
        clientlogs.error("Missing redis port (REDIS_DEPLOYMENT_SERVICE_PORT)")
        return None

    try:
        con = redis.Redis(redis_address, port=redis_port)
        con_status = con.ping()
        if con_status:
            clientlogs.info("Success: connected to redis")
            return con
        else:
            clientlogs.error("Could not connect to redis")
            con.close()
            return None
    except Exception as e:
        print(f"Exception {e}")

def read_test_cfg_info(cfg_file: str) -> dict():
    test_cfg = {}
    with open(cfg_file) as c_info_file:
        test_cfg = yaml.load(c_info_file, Loader=SafeLoader)
    return test_cfg


def read_json_file(json_file_name: str):
    with open(json_file_name) as jf:
        data = json.load(jf)
    return data

def save_json_to_redis(json_file_name: str):
    con = redis_connect()
    if con:
        json_data = read_json_file(json_file_name)
        con.set(json_file_name, str(json_data))
        clientlogs.info(f"json data is stored in redis, file: {json_file_name}")
        clientlogs.info(f"querying redis for key={json_file_name}")
        redis_result = con.get(json_file_name)
        clientlogs.info(f"result={redis_result}")
        con.close()

class test_ocr_client(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cfg_path = os.path.dirname(os.path.abspath(__file__))
        cfg_file = f"{cfg_path}/ocr_client_test_config.yaml"
        json_validation_file = f"{cfg_path}/results_validation.json"

        ## Read configurations
        test_cfg = read_test_cfg_info(cfg_file)
        cls.validation_results = read_json_file(json_file_name=json_validation_file)
        print(type(cls.validation_results))
        # cls.validation_results_as_dict = json.loads(cls.validation_results)

        ## save cfg to tester
        # print(f"{type(test_cfg)=}")
        clientlogs.debug(f"{test_cfg=}")
        cls.s3_cfg: dict = test_cfg["ocr_client_cfg"]["s3_info"]
        clientlogs.debug(test_cfg["ocr_client_cfg"]["s3_info"])
        cls.httplinks = test_cfg["ocr_client_cfg"]["httplinks"]
        cls.files = test_cfg["ocr_client_cfg"]["files"]
        cls.service_network: dict = test_cfg["ocr_client_cfg"]["service_network_rest"]

        cls.service_network["remote_service_address"] = os.environ.get(
            "OCR_SERVICE_ADDRESS"
        )

        cls.ocr_client_obj = rest_client_base.OcrRestClient(**cls.service_network)

    @unittest.skip(" running one test at time ")
    def test_text_extraction_uploadfile_json(self):
        """Request OCR service to process files located in shared file system"""
        filename = self.files[0]
        clientlogs.info(f"uploading {filename}")
        results = self.ocr_client_obj.get_inference_fileUpload_jsonResults(filename)

        clientlogs.debug(results)

        # Validation steps
        results_as_dict = json.loads(results)
        filename_stripped = filename.split("/")[-1]
        self.assertEqual(
            self.validation_results[filename_stripped],
            results_as_dict[filename_stripped],
        )

    @unittest.skip(" running one test at time ")
    def test_text_extraction_uploadfile_file(self):
        """bidirectional stream: upload pdf files to OCR service for processing"""
        filename = self.files[1]
        clientlogs.info(f"uploading {filename}")
        results = self.ocr_client_obj.get_inference_fileUpload(filename)

        clientlogs.debug(results)

        # Validation steps
        actual_results = read_json_file(results)
        filename_stripped = filename.split("/")[-1]
        self.assertEqual(
            self.validation_results[filename_stripped],
            actual_results[filename_stripped],
        )

    # @unittest.skip(" running one test at time ")
    def test_text_extraction_manyFilesUpload(self):
        """bidirectional stream: upload many pdf files to OCR service for processing"""

        clientlogs.info(f"uploading {self.files}")
        results = self.ocr_client_obj.get_inference_manyFilesUpload(self.files)
        clientlogs.debug(results)

        # Validation steps
        actual_results = read_json_file(results)

        # redis (for testing)
        save_json_to_redis(results)

        self.assertEqual(self.validation_results, actual_results)


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