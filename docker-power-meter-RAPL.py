import sys
import getopt
import pyRAPL
import docker

# Create a power-meter based using https://pypi.org/project/pyRAPL/
## This code is not tested in any way except to see that it fails in OSX
## and should be expected to not work anywhere.


def run_and_measure_container(container_name, image, command):
    pyRAPL.setup()
    meter = pyRAPL.Measurement('container')
    container = docker_client.containers.create(image,
                    command,
                    name=container_name,
                    detach=True,
                    tty=False,
                    ports={},
                    volumes={})
    meter.begin()
    print("start container: {}".format(container_name))
    container.start()
    container.wait()
    meter.end()
    container.stop()
    container.remove()

def main():
    getopt_args = sys.argv[1:]
    command = ""
    try:
        opts, args = getopt.getopt(getopt_args, "hi:c:", ["help", "image=", "command="])
    except getopt.GetoptError:
        print('docker-power-meter-RAPL.py -i <image> -c <command>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('docker-power-meter-RAPL.py -i <image> -c <command>')
            sys.exit()
        elif opt in ("-i", "--image"):
            image = arg
        elif opt in ("-c", "--command"):
            command = arg
    run_and_measure_container("rapl_test_container", image, command)

if __name__ == "__main__":
    main()