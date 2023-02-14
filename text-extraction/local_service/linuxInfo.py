#!/usr/bin/python3
""" get basic os from k8 container """
import os
import subprocess
import re
import argparse
from dataclasses import dataclass

@dataclass
class cmd_info:
    """ data class hold cmd info

    """
    name: str= ""
    cmd: str = ""
    regex: str = r""
    
    
class BasicContainerInfo:
    def __init__(self):
        self.cmd_env = os.environ.copy()
        self.cmds = dict (total_mem= cmd_info("MemTotal", "cat /proc/meminfo| grep MemTotal", r"MemTotal:\s+(\d+)") , \
            cpu_count= cmd_info("cpu_count", "lscpu|grep CPU\(s\) | head -1", r"CPU\(s\):\s+(\d+)") , \
            hr_mem_limit_cgroup= cmd_info("hr_memory_limit_cgroup", "cat /sys/fs/cgroup/memory/memory.stat | grep hierarchical_memory_limit", r"hierarchical_memory_limit\s+(\d+)") , \
            cpu_share_cgroup= cmd_info("cpu_share_cgroup", "cat /sys/fs/cgroup/cpu/cpu.shares", r"(\d+)") , \
            )
                
    
    def run_cmd(self, cmd, run_env):
        
        try:
            output=subprocess.check_output(cmd, shell=True, env=run_env)
            
            output = output.decode('utf-8')
            
            return output

        except subprocess.CalledProcessError as e:
            print(f' returned error: {e.returncode}, output: {e.output.decode()}')
            return e.returncode

    def  get_entry_info(self, entry_name):
        cmd_entry = self.cmds[entry_name]
        cmd_out = self.run_cmd(cmd_entry.cmd, self.cmd_env)
        #print(cmd_out)
        results = re.findall(cmd_entry.regex, cmd_out)
        #print(results)
        if len(results) > 0:
            return results[0]
        else:
            return 0
    
    def get_total_memory(self):
        return self.get_entry_info('total_mem')
    
    def get_cpu_count(self):
        return self.get_entry_info('cpu_count')
    
    def get_hr_mem_limit_cgroup(self):
        return self.get_entry_info( 'hr_mem_limit_cgroup')
    
    def get_cpu_share_cgroup(self):
        return self.get_entry_info( 'cpu_share_cgroup')
    
def humansize(size: int , binary: bool = True):
    """ Helper function to convert sizes into human readable format
        size in bytes 
    """

    units_bin = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB' ]
    units_dec = ['Bytes', 'KB', 'MB', 'GB', 'TB' ]
    
    devisor = 1024 if binary else 1000
    units  = units_bin if binary else units_dec
    
    level_size = [pow(devisor, count) for count, value in enumerate(units) ]
    
    level = len(units) - 1 
    
    while level >= 1 and size <= level_size[level]:
        level = level -1
    
    return f"{round(size/level_size[level], 1)} {units[level]}"
        
        
    

def main(args):
    lx_info = BasicContainerInfo()
    
    report = {}
    def human_format_wrapper(val: int, arg_format_str: str):
        binary_format = False if arg_format_str else True
        return humansize(val, binary=binary_format)
        
    if args.info_type == "cpu_count" or args.cpu_count == True:
        report['cpu_count'] = lx_info.get_cpu_count()
        
    if args.info_type == "total_mem" or args.total_mem == True:
        total_mem = lx_info.get_total_memory()
        if args.human:
            report['total_mem'] = human_format_wrapper(val=1024*int(total_mem), arg_format_str=args.natural)
        else:
            report['total_mem'] = total_mem
            
    if args.info_type == "mem_limit" or args.mem_limit == True:
        mem_limit =  lx_info.get_hr_mem_limit_cgroup()
        if args.human:
            report['mem_limit'] = human_format_wrapper(val=int(mem_limit), arg_format_str=args.natural)
        else:
            report['mem_limit'] = mem_limit
            
    if args.info_type == "cpu_share" or args.cpu_share == True:
        cpu_share =  lx_info.get_cpu_share_cgroup()
        report['cpu_share'] = round(float(cpu_share)/1024,2)
    
    if args.no_key:
        for key , val in report.items():
            print(val)
    else:        
        for key , val in report.items():
            print(f"{key}: {val}")

if __name__ == "__main__":

    info_list = ['cpu_count', 'total_mem', 'mem_limit', 'cpu_share']
    a_parser = argparse.ArgumentParser()
    a_parser.add_argument('--info_type',   type=str, help='type of information to be returned', choices=info_list, required=False)
    a_parser.add_argument('--cpu_count',  action='store_true', help='return cpu count', required=False)
    a_parser.add_argument('--total_mem',  action='store_true', help='return total mem in KB', required=False)
    a_parser.add_argument('--cpu_share',  action='store_true', help='return cgroup cpu share count', required=False)
    a_parser.add_argument('--mem_limit',  action='store_true', help='return cgroup hierarchical_memory_limit', required=False)
    a_parser.add_argument('--human',  action='store_true', help='repot sizes in human readable form', required=False)
    a_parser.add_argument('--natural',  action='store_true', help='Do not user binary scalling! use decimal scalling for kb, mb and gb', required=False)
    a_parser.add_argument('--no_key',  action='store_true', help='just print numerical values', required=False)
    args = a_parser.parse_args()
    main(args)