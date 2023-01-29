import sqlite3
import yaml
import multiprocessing
import os
import argparse
from chain_watcher import ChainWatcher
from slack_sdk import WebhookClient
from prometheus_client import start_http_server, multiprocess, CollectorRegistry
import logging
from pathlib import Path
import shutil


def init_db(db_conn):
    cur = db_conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS chains(chain_id TEXT PRIMARY KEY, upgrade_height int)"
    )


def get_config(config_file):
    config = yaml.safe_load(config_file)
    return config

def configure_prometheus():
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = "/tmp/upgrade_watcher_prom"
    upgrade_prom_path = Path("/tmp/upgrade_watcher_prom")
    if upgrade_prom_path.exists():
        shutil.rmtree(upgrade_prom_path)
    upgrade_prom_path.mkdir(parents=True, exist_ok=True)

    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    start_http_server(8000, registry=registry)

def start_monitors(config):
    queue = []

    for chain_id in config["chains"].keys():
        watcher = ChainWatcher(config, chain_id)
        queue.append(multiprocessing.Process(target=watcher.monitor, daemon=True))

    for process in queue:
        process.start()

    for process in queue:
        process.join()

def configure_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config-file",
        help="Path to config file",
        type=argparse.FileType("r"),
        default="config.yaml",
    )

    return parser

def main():
    configure_prometheus()

    parser = configure_parser()
    args = parser.parse_args()

    config = get_config(args.config_file)
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s:%(message)s"
    )

    db_conn = sqlite3.connect(config["db_path"])
    init_db(db_conn)
    db_conn.close()

    start_monitors(config)


if __name__ == "__main__":
    main()
