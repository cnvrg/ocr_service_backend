import os
import yaml
import json
import time
from functools import wraps
from typing import List
from multiprocessing import Pool, TimeoutError, cpu_count
from rest_client_base import OcrRestClient
import numpy as np
import glob
import random

def get_result(log):
    user_time = []

    with open(log) as f:
        f = f.readlines()

    for line in f:
        if "time" in line:
            second = line.split(":",1)[1]
            user_time_second = float(second)
            user_time.append(user_time_second)

    print("user_time", user_time)
    mean = np.mean(user_time)
    print("user_time_mean", "%.6f" % mean)
    std = np.std(user_time)
    print("user_time_std", "%.6f" % std)

    return mean, std

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        with open("sequence_time.txt", "a") as myfile:
            myfile.write("sequence time:"+str(total_time)+"\n")
        return result

    return timeit_wrapper

def timeit1(func):
    @wraps(func)
    def timeit1_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        with open("parallel_time.txt", "a") as myfile:
            myfile.write("parallel time:"+str(total_time)+"\n")
        return result

    return timeit1_wrapper

@timeit
def bench_sequence(
    client_func: OcrRestClient.get_infrance_fileUpload_jsonResults,
    fileList: List[str],
    rounds: int,
):

    for round_run in range(rounds):
        for file in fileList:
            client_func(file)


@timeit1
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
    try:
        os.remove("sequence_time.txt")
    except OSError:
        pass
    
    try:
        os.remove("parallel_time.txt")
    except OSError:
        pass
    
    user_worker_pool_bench: bool = True
    use_sequence_bench: bool = True
    
    #files = []
    #for filename in glob.iglob('/cnvrg/*'):
    #    files.append(os.path.abspath(filename))
    #random.shuffle(files)
    #print("===File List===", files)
    files = ["/cnvrg/Data+science.pdf", "/cnvrg/economics.pdf"]
    ocr_network = {
        "remote_service_address": os.environ.get("OCR_SERVICE_ADDRESS"),
        "remote_service_port": 40051,
    }
    ocr_client_object = OcrRestClient(**ocr_network)

    # normal tests
    if use_sequence_bench:
        for i in range(8):
            bench_sequence(ocr_client_object.get_infrance_fileUpload_jsonResults, files, 1)

    # worker pool test:
    if user_worker_pool_bench:
        largeFileList = [*files, *files, *files, *files]
        for i in range(2):
            bench_worker_pool(
                ocr_client_object.get_infrance_fileUpload_jsonResults, files, 1, 4
            )
            random.shuffle(files)
    try:
        os.remove("sequence_parallel_result.txt")
    except OSError:
        pass

    print()
    print("---sequence result:")
    sequence_mean, sequence_std = get_result("sequence_time.txt")
    print("---parallel result:")
    parallel_mean, parallel_std = get_result("parallel_time.txt")

    with open("sequence_parallel_result.txt", "a") as myfile:
        myfile.write("sequence time mean:"+str(sequence_mean)+"\n")
        myfile.write("sequence time std:"+str(sequence_std)+"\n")
        myfile.write("parallel time mean:"+str(parallel_mean)+"\n")
        myfile.write("parallel sequence time std:"+str(parallel_std)+"\n")


if __name__ == "__main__":
    bench_main()
