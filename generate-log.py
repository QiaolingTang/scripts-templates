#coding=utf-8
import logging
import logging.handlers
import time
from datetime import datetime

logger = logging.getLogger("logger")

handler1 = logging.StreamHandler()
#handler2 = logging.FileHandler(filename="/var/log/generated/test.log")

logger.setLevel(logging.INFO)
handler1.setLevel(logging.INFO)
#handler2.setLevel(logging.INFO)

#formatter = logging.Formatter("time=%(asctime)s level=%(levelname)s msg=%(message)s")
formatter = logging.Formatter("%(message)s")
handler1.setFormatter(formatter)
#handler2.setFormatter(formatter)

logger.addHandler(handler1)
#logger.addHandler(handler2)


logfile = '/etc/generate-log/json.example'
f = open(logfile, "r")
if f.mode == "r":
    logs = f.read()

#logs = '{"message": "MERGE_JSON_LOG=true", "testcase": "logging-test", "level": "info"," Layer1": "layer1 0", "layer2": {"name":"Layer2 1", "tips":"decide by PRESERVE_JSON_LOG"}, "StringNumber":"10", "Number": 10,"foo.bar":"dotstring","{foobar}":"bracestring","[foobar]":"bracket string", "foo:bar":"colonstring", "empty1":"", "empty2":{}}'
if __name__ == "__main__":
    i = 0
    while True:
        logger.info("{\"time\": \"%s\", "+logs+"}", datetime.utcnow())
        time.sleep(0.5)
