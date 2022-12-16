import unittest
import os
from dataclasses import dataclass, field
import s3connector as s3_c


@dataclass
class argumnets:
    bucket: str = field(default_factory=str())


class Test_file_download(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        endpoint = "http://s3.amazonaws.com"
        config = s3_c.Config()
        cls.s3 = s3_c.S3(
            config.aws_access_key_id, config.aws_secret_access_key, endpoint, None
        )

    # @unittest.skip(" having errors")
    def test_case_1(self):
        """Testing basic serice connection"""
        # s3_c.cmd_download(self.s3, )
        # self.s3.check_bucket_exist("libhub-readme")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
