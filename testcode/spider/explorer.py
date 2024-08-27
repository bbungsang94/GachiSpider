import logging
from utils.logging import init_logging
from task.explorer import GraphExplorer


def main():
    init_logging(logging.INFO, "Gachi-Spider.log")
    exp = GraphExplorer(["https://www.hankookchon.com/news"])
    exp.step()

if __name__ == "__main__":
    main()