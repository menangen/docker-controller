import time
import docker

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

try:
    time.sleep(120)
    container.stop()
except Exception as e:
    print("Can't remove container", e)
