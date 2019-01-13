import time
import signal
import sys
import docker

global server_container
VOLUME = "manager"

if __name__ == '__main__':
    print("Start at: %s" % time.ctime())

    try:
        client = docker.DockerClient(base_url="unix://var/run/docker.sock")

        print("Docker ok" if client.ping() else "Docker ping error")
    except:
        print("Docker socket error")
        client = docker.from_env()

    try:
        client.volumes.create(name=VOLUME)
        print(f"Created <{VOLUME}> shared volume")
    except Exception as e:
        print(f"Can't create <{VOLUME}> volume", e)

    try:
        server_container = client.containers.run(
            "menangen/asyncio",
            name="server",
            # ports={"8000/tcp": 8000},
            volumes=[f"{VOLUME}:/tmp"],
            tty=True,
            auto_remove=True,
            detach=True)
        server_container.getLog = lambda: server_container.logs().decode("UTF-8")

        print("Is created", server_container)

        client_container = client.containers.run(
            "menangen/asyncio",
            command="python client.py",
            name="client",
            # ports={"8000/tcp": 8000},
            volumes=[f"{VOLUME}:/tmp"],
            tty=True,
            auto_remove=True,
            detach=True)
        client_container.getLog = lambda: client_container.logs().decode("UTF-8")

        print("Is created", client_container)

        time.sleep(1)
        print("Server Logs: ", server_container.getLog())
        print("Client Logs: ", client_container.getLog())

        time.sleep(5)
        print("Logs: ", server_container.getLog())
        print("Client Logs: ", client_container.getLog())

        print("waiting CTRL-C or SIGTERM...")

    except Exception as e:
        print("Can't start container with app", e)

    def end(signum, frame):
        try:
            print("---------------------------------------")
            print("Try to remove containers")
            server_container.stop()
            print("Server container stoped")
            client_container.stop()
            print("Client container stoped")

            print(f"Removing unused volume: {VOLUME}")
            time.sleep(1)

            removed = client.volumes.prune()
            print("Removed Volumes:", removed)

        except Exception as e:
            print("Can't remove container", e)

        finally:
            sys.exit(0)

    signal.signal(signal.SIGINT, end)
    signal.signal(signal.SIGTERM, end)

    time.sleep(10800)
