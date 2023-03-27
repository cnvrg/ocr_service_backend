import os
import yaml
import json
import time
from functools import wraps
from typing import List
from multiprocessing import Pool, TimeoutError, cpu_count
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
    client_func: OcrRestClient.get_infrance_fileUpload_jsonResults,
    fileList: List[str],
    rounds: int,
):

    for round_run in range(rounds):
        for file in fileList:
            client_func(file)


@timeit
def bench_worker_pool(
    client_func: OcrRestClient.get_infrance_fileUpload_jsonResults,
    fileList: List[str],
    rounds: int,
    pool_size: int,
):
    sizes = [pool_size, cpu_count(), len(fileList)]
    pool_size_actual = min(sizes)
    # _trim_len = len(fileList) % pool_size_actual

    pool_sweep_counts = len(fileList) // pool_size_actual

    start, end = 0, pool_size_actual

    for _run_count in range(rounds):
        start, end = 0, pool_size_actual
        # print(f"{pool_size_actual=} {pool_sweep_counts=} {start=} {end=}")
        for _sw_count in range(pool_sweep_counts):
            with Pool(processes=pool_size_actual) as pool:
                # print(f"{_run_count=} {_sw_count=} {fileList[start:end]=} ")
                pool.map(client_func, fileList[start:end])
                end += pool_size_actual
                start += pool_size_actual


def bench_main():
    user_worker_pool_bench: bool = False
    use_sequence_bench: bool = True
    files = ["/cnvrg/Data+science.pdf", "/cnvrg/economics.pdf"]
    ocr_network = {
        "remote_service_address": os.environ.get("OCR_SERVICE_ADDRESS"),
        "remote_service_port": 40051,
    }
    ocr_client_object = OcrRestClient(**ocr_network)

    # normal tests
    if use_sequence_bench:
        bench_sequence(ocr_client_object.get_infrance_fileUpload_jsonResults, files, 4)

    # worker pool test:
    if user_worker_pool_bench:
        largeFileList = [*files, *files, *files, *files]
        bench_worker_pool(
            ocr_client_object.get_infrance_fileUpload_jsonResults, largeFileList, 1, 4
        )


if __name__ == "__main__":
    bench_main()
