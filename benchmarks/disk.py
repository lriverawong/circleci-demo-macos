#!/usr/bin/env python3

# Based on; https://www.amsys.co.uk/using-command-line-to-benchmark-disks/

import subprocess
import sys

def check_above_threshold(list1, val): 
    return(all(float(x) > float(val) for x in list1))

def main():
    benchmark_value = float("10000")

    print("-- Start disk.py --")
    output_arr_write = []
    output_arr_read = []
    for cycle in range(1,6):
        write_test = subprocess.run("dd if=/dev/zero bs=2048k of=tstfile count=1024 2>&1 | grep sec | awk '{print $1 / 1024 / 1024 / $5}'", shell=True, capture_output=True)
        write_out = float(write_test.stdout)
        output_arr_write.append(write_out)
        print("WRITE - Cycle %s = %s MB/s" % (cycle, write_out))

        purge_test = subprocess.run("sudo purge", shell=True)
        
        read_test = subprocess.run("dd if=tstfile bs=2048k of=/dev/null count=1024 2>&1 | grep sec | awk '{print $1 / 1024 / 1024 / $5 }'", shell=True,capture_output=True)
        read_out = float(read_test.stdout)
        output_arr_read.append(read_out)
        print("READ - Cycle %s = %s MB/s" % (cycle, read_out))
        
        remove_test_file = subprocess.run("rm tstfile", shell=True)
    print("Write speeds (MB/s = %s" % output_arr_write)
    print("Read speeds (MB/s = %s" % output_arr_read)

    # Check to see if within expectations
    if not check_above_threshold(output_arr_write, benchmark_value):
        if not check_above_threshold(output_arr_read, benchmark_value):
            print("WRITE & READ : Speed test fails")
            sys.exit(1)
        print("WRITE : Speed test fail")
        sys.exit(1)
    
    if not check_above_threshold(output_arr_read, benchmark_value):
        print("READ : Speed test fails")
        sys.exit(1)

    print("Speed test pass")
    sys.exit(0)

if __name__ == '__main__':
   main()