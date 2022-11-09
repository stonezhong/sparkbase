#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
from mordor import prepare_for_docker, AppEnv

def on_stage(app_env):
    context = app_env.get_config("_deployment.json")
    context.update({
        "jupyterhub": app_env.get_config("jupyterhub.json"),
        "spark": app_env.get_config("spark.json"),
        "google_oauth": app_env.get_config("google_oauth.json"),
        "app_env": app_env
    })
    prepare_for_docker(app_env.app_name, context)

    os.makedirs(os.path.join(app_env.data_dir, "db"), exist_ok=True)
    os.makedirs(os.path.join(app_env.data_dir, "state"), exist_ok=True)

    os.chmod(os.path.join(app_env.data_dir, "state"), 0O777)

def main():
    parser = argparse.ArgumentParser(
        description='Dispatch Tool'
    )
    parser.add_argument(
        "action", type=str, help="Specify action",
        choices=['on_stage', 'build', 'up'],
        nargs=1
    )
    args = parser.parse_args()
    action = args.action[0]

    app_env = AppEnv("jupyterhub")

    if action == "on_stage":
        on_stage(app_env)
    elif action == "up":
        os.chdir(os.path.join(app_env.data_dir, "docker"))
        os.system("docker compose up -d")
    elif action == "build":
        os.chdir(os.path.join(app_env.data_dir, "docker"))
        os.system("docker compose build")

if __name__ == '__main__':
    main()
