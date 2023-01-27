import getopt
import sys
import threading
from time import sleep
import docker
docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def print_stats_stream(stream,out_stream):
    for line in stream:
        out_stream.write(line)
        
def create_docker_contatiner(container_name, image, command, out_stream):
    container = docker_client.containers.create(image,
                    command,
                    name=container_name,
                    detach=True,
                    tty=False,
                    ports={},
                    volumes={})
    statsStream = container.stats(stream=True, decode=False)
    # print("start thread")
    threading.Thread(target=print_stats_stream, args=(statsStream,out_stream,)).start()
    # print("start container: {}".format(container_name))
    s = container.start()
    w = container.wait()
    # print(s)
    # print(w)
    # sleep(5)
    container.stop()
    container.remove()
    statsStream.close()    

    
    

# entrypoint method
def main():
    getopt_args = sys.argv[1:]
    command = ""
    out_stream = sys.stdout.buffer
    try:
        opts, args = getopt.getopt(getopt_args, "hi:c:o:", ["help", "image=", "command=", "output="])
    except getopt.GetoptError:
        print('docker-power-meter.py -i <image> -c <command>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('docker-power-meter.py -i <image> -c <command>')
            sys.exit()
        elif opt in ("-i", "--image"):
            image = arg
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-o", "--output"):
            out_stream = open(arg, 'wb')
    create_docker_contatiner("test_container", image, command, out_stream)


if __name__ == "__main__":
    main()