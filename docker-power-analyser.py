import json
import sys
import getopt

def analyse_log(log_file):
    # print("analyse_log: {}".format(log_file))
    total_cpu_time = 0
    total_memory_usage = 0
    num_memory_samples = 0
    with open(log_file, 'r') as f:
        lines = f.readlines()
        ## parse json lines to object
        for line in lines:
            json_object = json.loads(line)
            if('usage' in json_object['memory_stats']):
                if(json_object['memory_stats']['usage'] > 0):
                    total_memory_usage += json_object['memory_stats']['usage']
                    num_memory_samples += 1
            if(json_object['cpu_stats']['cpu_usage']['total_usage'] > total_cpu_time):
                total_cpu_time = json_object['cpu_stats']['cpu_usage']['total_usage']
    
    print("total cpu time: {}s  mean memory use: {}".format(total_cpu_time / 1000000000, total_memory_usage/num_memory_samples))


def main():
    getopt_args = sys.argv[1:]
    file = ""
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