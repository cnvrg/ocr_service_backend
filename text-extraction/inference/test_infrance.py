import unittest
import os
import json
from predict import predict


class TestInfra(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # cls.data = dict(pdf=["/cnvrg/Datascience.pdf", "/cnvrg/economics.pdf"])
        cls.data = dict(
            pdf=[
                "/tmp/httpDownload-12-15-2022-18-47-25/Datascience.pdf",
                "/tmp/httpDownload-12-15-2022-18-47-25/economics.pdf",
                # "/cnvrg/economics.pdf",
            ]
        )

        # cls.data = dict(pdf=["/cnvrg/economics.pdf"])

    # @unittest.skip(" having errors")
    def test_basic_infra(self):
        """Testing basic predict call"""
        prediction = predict(self.data)
        print(json.dumps(prediction, indent=4))
        # json.dump(prediction)
        self.assertTrue(True)

    @unittest.skip(" NOT NEEDED FOR NOW")
    def test_filename_cleanup(self):
        print(self.data)
        for file in self.data["pdf"]:
            f = file.split("/")[-1]
            fclean = "".join(x for x in f if x == "." or x.isalnum())
            print(f" {file=} {f=} {fclean=} ")


if __name__ == "__main__":
    unittest.main()
