import os
import readline
import time
import subprocess
import shutil
import argparse
from importlib_metadata import version
import yaml
from yaml.loader import SafeLoader
from dataclasses import dataclass, field, asdict, replace


@dataclass
class container_info:
    container_name: str
    container_image: str
    container_cmd: str


class workload_launcher:
    def __init__(self) -> None:
        pass

    def build_launch_cmd(self, container_name, container_image, container_cmd):

        cmd = (
            f"docker run --security-opt seccomp=unconfined  -id --name {container_name}"
        )
        cmd = f"{cmd} -expose=50051 {container_image}"
        cmd = f"{cmd} {container_cmd}"

        return cmd

    def run_cmd(self, cmd, run_env=None):
        run_env = os.environ.copy() if run_env is None else run_env

        """command runner"""
        try:
            output = subprocess.check_output(cmd, shell=True, env=run_env)

            output = output.decode("utf-8")

            return output

        except subprocess.CalledProcessError as e:
            print(f" returned error: {e.returncode}, output: {e.output.decode()}")
            return e.returncode


def main():
    start_client = "bash"

    start_s3_service =                 "bash -c \". /root/ocr_service_backend/s3_connector/local_service/setup_s3_requirements.sh"
    start_s3_service = f"{start_s3_service} && bash  \""
    #start_s3_service = f"{start_s3_service} && bash /root/ocr_service_backend/s3_connector/local_service/start_service.sh \""

    start_ocr_service =                  "bash -c \". /root/ocr_service_backend/text-extraction/local_service/setup_ocr_requirements.sh"
    start_ocr_service = f"{start_ocr_service} && bash  \" "
    #start_ocr_service = f"{start_ocr_service} && bash /root/ocr_service_backend/text-extraction/local_service/start_service.sh \" "

    containers = [
        container_info(
            "client_service_mvp_set1",
            "lamatriz/wlpu:ubuntu_20.04_MVP_Set1",
            start_client,
        ),
        container_info(
            "s3_service_mvp_set1",
            "lamatriz/wlpu:ubuntu_20.04_MVP_Set1",
            start_s3_service,
        ),
        container_info(
            "ocr_service_mvp_set1",
            "lamatriz/wlpu:ubuntu_20.04_MVP_Set1",
            start_ocr_service,
        ),
    ]

    launcher = workload_launcher()

    for cn in containers:
        # print(f"{asdict(cn)=}")
        launch_cmd = launcher.build_launch_cmd(**asdict(cn))
        print(f"{launch_cmd=}")
        output = launcher.run_cmd(launch_cmd)
        print(f"{output=}")


if __name__ == "__main__":
    main()
