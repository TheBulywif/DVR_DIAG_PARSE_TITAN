import os
import easygui
from debug import logger

video_cameras = []



def select_folder():
    log.info(f"PROMPTING USER FOR FOLDER LOCATION")
    path = easygui.diropenbox("Select DVRLog Folder", "Select DVRLog Folder")
    log.debug(f"FOLDER SELECTED: {path}")
    return path


def format_string(string):
    var = string
    while True:
        if var[-1] == "*":
            var = var[:-1]
            var = var.strip()
        else:
            break
    return var


def format_camera(line):
    var = line
    while True:
        if var[-1] == ".":
            var = var[:-19]
            var = var.strip()
        else:
            break
    return var


def scan():
    dvr_log_list = []
    folder = select_folder()
    log.info(f"**** SCANNING {folder} FOR LOGS ****")
    for root, dirs, files in os.walk(folder, topdown=False):
        if root.__contains__('TDVideo'):
            for name in files:
                if name.startswith("dvrlog"):
                    dvrlog = os.path.join(root, name)
                    if dvr_log_list.__contains__(dvrlog):
                        pass
                    else:
                        dvr_log_list.append(dvrlog)
    log.info(f"**** SCAN COMPLETE ****")
    log.info(f"**** LOGS FOUND: {len(dvr_log_list)} ****\n")
    return dvr_log_list


def read_log(file):
    lines = []
    count = 0
    with open(file, 'r') as dvrlog:
        while True:
            count += 1
            line = dvrlog.readline()
            if len(line) > 1:
                lines.append(f"Line {count} L{len(line)}: {line.strip()}")
            elif len(line) <= 1:
                pass
            if not line:
                break
    return lines


def filter_log(lines):
    hostname = ""
    model = ""
    firmware = ""
    mcu = ""
    io_error = 0
    watchdog_error = 0
    for line in lines:
        if line.__contains__('hostname'):
            temp_list = line.split(":", 5)
            var = temp_list.pop()
            formatted_var = format_string(var)
            hostname = f"{formatted_var}"
        if line.__contains__('DVR Firmware'):
                log.debug(f"LINE CONTAINS FIRMWARE")
                temp_list = line.split(":", 5)
                var = temp_list.pop()
                formatted_var = format_string(var)
                firmware = formatted_var
                log.debug(f"FIRMWARE: {firmware}")
                if "TITAN" in firmware:
                    model = "Zeus Titan"
        if line.__contains__('MCU version'):
            if len(mcu) == 0:
                temp_list = line.split(":", 6)
                var = temp_list.pop()
                formatted_var = format_string(var)
                mcu = f"{formatted_var}"
        if line.__contains__('One or more camera not working, system reset'):
            io_error += 1
        if line.__contains__('Dvr watchdog failed, restarting dvrsvr'):
            watchdog_error += 1
    if model == "Zeus Titan":
        print(f"Hostname: {hostname}")
        print(f"Model: {model}")
        print(f"Firmware: {firmware}")
        print(f"MCU: {mcu}")
        print(f"IO ERROR COUNT: {io_error}")
        print(f"WATCHDOG ERROR COUNT: {watchdog_error}")
    # print(f"Hostname: {hostname} - Model: {model} - Firmware: {firmware} - MCU: {mcu} - IO ERROR COUNT: {io_error}")


def get_lines(file):
    lines = []
    try:
        log.info(f"**** SCANNING {file} ****")
        lines = read_log(file)
        log.info(f"**** SCAN COMPLETE ****")
    except UnicodeDecodeError as e:
        log.error(f"{e} --**** {file} POTENTIALLY CORRUPT - SKIPPING ****--")
    return lines


if __name__ == '__main__':
    log = logger.init_logger()
    logger.start_log(log)
    print(f"----SCANNING FOR LOG FILES----")
    file_list = scan()
    print(f"----{len(file_list)} LOGS FOUND----\n")
    for file in file_list:
        print(f"\n****COPYING LOG FILE****")
        log.info(f"COPYING LINES FROM LOGFILE TO LIST")
        lines = get_lines(file)
        print(f"{file}COPIED")
        log.info(f"LINES COPIED")
        log.info(f"PARSING LINES")
        print(f"****PARSING LINES****")
        filter_log(lines)
        print(f"****PARSE COMPLETE****\n")
    input("PRESS ENTER TWICE (x2) TO QUIT PROGRAM...")
    logger.end_log(log)
