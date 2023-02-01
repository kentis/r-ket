import json
import sys
import getopt
from dateutil import parser
import fileinput
from naive_power_model import energy_from_cpu, energy_from_memory_use, energy_from_disk_use, energy_from_network_use

def analyse_log(log_file):
    # print("analyse_log: {}".format(log_file))
    total_cpu_time = 0
    total_memory_usage = 0
    max_memory_use = 0
    num_memory_samples = 0
    total_time = 0
    with fileinput.input(log_file, mode='r') as f:
        #lines = f.readlines()
        ## parse json lines to object
        for line in f:
            json_object = json.loads(line)
            if 'Id' in json_object:
                # this is the summary object
                started_at = parser.parse(json_object['State']['StartedAt'])
                finished_at = parser.parse(json_object['State']['FinishedAt'])
                print("Total time: {}   -- Started: {}  Finished: {}".format(finished_at - started_at, started_at, finished_at))
            else:
                if('usage' in json_object['memory_stats']):
                    if(json_object['memory_stats']['usage'] > 0):
                        total_memory_usage += json_object['memory_stats']['usage']
                        if(json_object['memory_stats']['usage'] > max_memory_use):
                            max_memory_use = json_object['memory_stats']['usage']
                        num_memory_samples += 1
                if(json_object['cpu_stats']['cpu_usage']['total_usage'] > total_cpu_time):
                    total_cpu_time = json_object['cpu_stats']['cpu_usage']['total_usage']
    
    cpu_power = energy_from_cpu(total_cpu_time/ 1000000000)
    memory_power = energy_from_memory_use(max_memory_use / 1_000_000_000, (finished_at - started_at).total_seconds() )

    print("total cpu time: {}s  mean memory use: {}".format(total_cpu_time / 1000000000, total_memory_usage/num_memory_samples))
    print("real time: {}s".format((finished_at - started_at).total_seconds()))
    print("max memory use: {}GB".format(max_memory_use/1_000_000_000))
    print("cpu power: {}J / {}KWh".format(cpu_power, cpu_power / 3600000))
    print("memory power: {}J / {}KWh".format(memory_power, memory_power / 3600000))
    print("total power: {}J / {}KWh".format(cpu_power + memory_power, (cpu_power + memory_power) / 3600000))

def main():
    getopt_args = sys.argv[1:]
    file = "-" #sys.stdin.buffer
    try:
        opts, args = getopt.getopt(getopt_args, "hi:", ["help", "input=",])
    except getopt.GetoptError:
        print('docker-power-analyser.py -i input-file')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('docker-power-meter.py -i <image> -c <command>')
            sys.exit()
        elif opt in ("-i", "--input"):
            file = arg
    analyse_log(file)

if __name__ == "__main__":
    main()