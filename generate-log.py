#coding=utf-8
import logging
import logging.handlers
import time

logger = logging.getLogger("logger")

handler1 = logging.StreamHandler()
#handler2 = logging.FileHandler(filename="/var/log/generated/test.log")

logger.setLevel(logging.DEBUG)
handler1.setLevel(logging.DEBUG)
#handler2.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler1.setFormatter(formatter)
#handler2.setFormatter(formatter)

logger.addHandler(handler1)
#logger.addHandler(handler2)


logfile = './log.json'
f = open(logfile, "r")
if f.mode == "r":
    logs = f.read()

if __name__ == "__main__":
    i = 0
    while True:
        logger.debug(logs)
        time.sleep(2)
    