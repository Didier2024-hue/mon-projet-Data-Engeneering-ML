import platform
import os
import socket
import subprocess
import psutil

def get_os_info():
    return platform.platform()

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return f"Hostname: {hostname}, IP Address: {ip_address}"

def get_hardware_info():
    cpu = platform.processor()
    memory = psutil.virtual_memory()
    return f"CPU: {cpu}, Total Memory: {memory.total / (1024 ** 3):.2f} GB"

##def get_environment_variables():
##    return dict(os.environ)

def get_running_docker_containers():
    try:
        containers = subprocess.check_output(["docker", "ps"]).decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        containers = "No Docker containers running or Docker is not installed"
    return containers

def get_docker_version():
    try:
        docker_version = subprocess.check_output(["docker", "--version"]).decode("utf-8").strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        docker_version = "Docker is not installed"
    return docker_version

def get_docker_images():
    try:
        images = subprocess.check_output(["docker", "images"]).decode("utf-8")
    except (subprocess.CalledProcessError, FileNotFoundError):
        images = "No Docker images found or Docker is not installed"
    return images

def get_postgresql_version():
    try:
        psql_version = subprocess.check_output(["psql", "--version"]).decode("utf-8").strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        psql_version = "PostgreSQL is not installed"
    return psql_version

def main():
    info = {
        "OS Information": get_os_info(),
        "Network Information": get_network_info(),
        "Hardware Information": get_hardware_info(),
        "Running Docker Containers": get_running_docker_containers(),
        "Docker Images": get_docker_images(),
        ##"Environment Variables": get_environment_variables(),
        "Docker Version": get_docker_version(),
        "PostgreSQL Version": get_postgresql_version(),
    }
    for key, value in info.items():
        print(f"=== {key} ===")
        print(value)
        print()

if __name__ == "__main__":
    main()

