#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import os
from mordor import prepare_for_docker, AppEnv


def main():
    parser = argparse.ArgumentParser(
        description='Dispatch Tool'
    )
    parser.add_argument(
        "action", type=str, help="Specify action",
        choices=['on_stage'],
        nargs=1
    )
    args = parser.parse_args()
    action = args.action[0]

    app_env = AppEnv("superset")
    context = app_env.get_config("_deployment.json")
    context.update({
        "superset": app_env.get_config("superset.json"),
        "google_oauth": app_env.get_config("google_oauth.json"),
        "app_env": app_env
    })
    prepare_for_docker("superset", context)

    os.makedirs(os.path.join(app_env.data_dir, "db"), exist_ok=True)
    os.makedirs(os.path.join(app_env.data_dir, "state"), exist_ok=True)

    os.chmod(os.path.join(app_env.data_dir, "state"), 0O777)

if __name__ == '__main__':
    main()
