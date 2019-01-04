import time
import signal
import sys
import docker

global container

if __name__ == '__main__':
    print("Start at: %s" % time.ctime())

    try:
        client = docker.DockerClient(base_url="unix://var/run/docker.sock")

        print("Docker ok" if client.ping() else "Docker ping error")
    except:
        print("Docker socket error")
        client = docker.from_env()

    try:
        container = client.containers.run(
            "menangen/travel-django-app",
            name="web",
            ports={"8000/tcp": 8000},
            auto_remove=True,
            detach=True)

        time.sleep(3)
        print(container.logs().decode("UTF-8"))
    except Exception as e:
        print("Can't start container with app", e)

    def end(signum, frame):
        try:
            print("Try to remove web container")
            container.stop()
            print("Child container is Removed")

        except Exception as e:
            print("Can't remove container", e)

        finally:
            sys.exit(0)

    signal.signal(signal.SIGINT, end)
    signal.signal(signal.SIGTERM, end)

    time.sleep(10800)
