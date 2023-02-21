
#!/usr/bin/env python3

import argparse
import subprocess
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find average runtime and std variance (95%)')
    parser.add_argument('log_file', help='time log file')
    args = parser.parse_args()
    
    user_time = []

    with open(args.log_file) as f:
        f = f.readlines()

    for line in f:
        if "real" in line:
            line = line.split("\t",1)[1]
            line = line.split("\n",1)[0]
            minute = line.split("m",1)[0]
            second = line.split("m",1)[1].split("s",1)[0]
            user_time_second = float(minute) * 60 + float(second) 
            user_time.append(user_time_second)

    print("user_time", user_time)
    mean = np.mean(user_time)
    print("user_time_mean", "%.6f" % mean)
    std = np.std(user_time)
    print("user_time_std", "%.6f" % std)

