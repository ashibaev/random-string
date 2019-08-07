import argparse
import importlib
import sys


def get_running_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("app")
    return parser.parse_args().app


def main():
    module = importlib.import_module(get_running_app())
    module.main()


if __name__ == '__main__':
    main()
