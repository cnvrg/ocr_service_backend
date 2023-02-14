import os
import yaml
import json
import time
from functools import wraps
from typing import List
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor
from rest_client_base import OcrRestClient


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


@timeit
def bench_sequence(
    client_func: OcrRestClient.get_inference_fileUpload_jsonResults,
    fileList: List[str],
    rounds: int,
):

    for round_run in range(rounds):
        for file in fileList:
            client_func(file)


@timeit
def bench_worker_pool(
    client_func: OcrRestClient.get_inference_fileUpload_jsonResults,
    fileList: List[str],
    rounds: int,
    pool_size: int,
):

    for _run_count in range(rounds):
        with ProcessPoolExecutor() as executor:
            executor.map(client_func, fileList)


def bench_main():
    user_worker_pool_bench: bool = True
    use_sequence_bench: bool = False
    files = ["/cnvrg/Data+science.pdf", "/cnvrg/economics.pdf"]
    ocr_network = {
        "remote_service_address": os.environ.get("OCR_SERVICE_ADDRESS"),
        "remote_service_port": 40051,
    }
    ocr_client_object = OcrRestClient(**ocr_network)

    # normal tests
    if use_sequence_bench:
        bench_sequence(ocr_client_object.get_inference_fileUpload_jsonResults, files, 4)

    # worker pool test:
    if user_worker_pool_bench:
        largeFileList = [*files, *files, *files, *files]
        bench_worker_pool(
            ocr_client_object.get_inference_fileUpload_jsonResults, largeFileList, 2, 8
        )


if __name__ == "__main__":
    bench_main()
