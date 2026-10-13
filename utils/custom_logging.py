import os

import arrow
from sortedcontainers import SortedDict

from config.settings import Settings, settings


async def log(log_file_name:str, **fields):
    month_dir = arrow.now().format('YYMM')
    day_dir = arrow.now().format('YYMMDD')
    path = os.path.join(
        settings.LOG_PATH,
        month_dir,
        day_dir,
    )

    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, log_file_name)
    log_list=[]

    sorted_fields = SortedDict(fields)

    for key in sorted_fields:
        log_list.append(str(key) + ":" + str(sorted_fields[key]))

    now_tstamp = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    message = "\t".join(log_list)
    message = now_tstamp + "\t" + message.replace("\\n", "").replace("\\r", "").replace(" ","")

    if os.path.isfile(file_path):
        file = open(file_path, "a")
        file.write(message+"\n")
        file.close()
    else:
        file = open(file_path, "w")
        file.write(message+"\n")
        file.close()
