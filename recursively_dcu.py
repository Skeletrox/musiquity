#!/usr/bin/python

import os
import re
import subprocess

# Brings up dockers with the _component suffix
COMPONENT_SUFFIX = r'.+_component$'

def execute(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def get_dirs(parent_dir = "."):
    return [o for o in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, o))]


def get_component_dirs():
    child_dirs = get_dirs()
    return [c for c in child_dirs if re.match(COMPONENT_SUFFIX, c)]

def bring_docker_up(child_dir, parent_dir="."):
    old_dir = os.getcwd()
    os.chdir("{}/{}".format(parent_dir, child_dir))
    try:
        for line in execute(["docker-compose", "up", "-d"]):
            print(line.strip())    
    except subprocess.CalledProcessError as e:
        print("Bringing docker up for {} failed: {}".format(child_dir, e))
    os.chdir(old_dir)


def main():
    dirs = get_component_dirs()
    for d in dirs:
        print("---{}---".format(d))
        bring_docker_up(d)
        print("-------")


if __name__ == "__main__":
    main()