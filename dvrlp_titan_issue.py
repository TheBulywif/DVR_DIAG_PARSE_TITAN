import os
import easygui
from past.builtins import raw_input

from debug import logger


fw_types = ["ZEUSTITAN.1.0.22.0729.14", "ZEUSTITAN.1.0.22.0812.15", "ZEUSTITAN.1.0.22.0906.13"]
mcu_types = ["Z16RV1126_A2IRTC_V2.3_2208191530", "Z16RV1126_A2IRTC_V2.0_2207271159"]
camera_names = ["Camera 1", "Camera 2", "Camera 3", "Camera 4", "Camera 5", "Camera 6", "Camera 7", "Camera 8",
                "Camera 9", "Camera 10", "Camera 11", "Camera 12", "Camera 13", "Camera 14", "Camera 15", "Camera 16"]


def select_folder():
    log.info(f"PROMPTING USER FOR FOLDER LOCATION")
    path = easygui.diropenbox("Select DVRLog Folder", "Select DVRLog Folder")
    log.debug(f"FOLDER SELECTED: {path}")
    return path


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
    return dvr_log_list, len(dvr_log_list)


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


def get_lines(file):
    lines = []
    try:
        log.info(f"**** SCANNING {file} ****")
        lines = read_log(file)
        log.info(f"**** SCAN COMPLETE ****")
    except UnicodeDecodeError as e:
        log.error(f"{e} --**** {file} POTENTIALLY CORRUPT - SKIPPING ****--")
    return lines


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


def total_logs(file_list):
    x = len(file_list)
    # print(f"{x} LOGS FOUND")
    return x


def find_titans(file_list):
    titan_list = []
    for file in file_list:
        lines = get_lines(file)
        for line in lines:
            if "ZEUSTITAN" in line:
                titan_list.append(file)
                break
    # print(f"{x} TITANS FOUND")
    return len(titan_list), titan_list


def fw_check(titan_list):
    fw_totals = []
    files = titan_list
    for file in files:
        with open(file, 'r') as file:
            # read all content from a file using read()
            content = file.read()
            # check if string present or not
            for fw_type in fw_types:
                if fw_type in content:
                    fw_totals.append(fw_type)
    for fw_type in fw_types:
        count = fw_totals.count(fw_type)
        print(f"FIRMWARE {fw_type}: {count}")
        count = 0
    #  print(f"{fw_types}")  # DEBUG


#  print(f"{fw_totals}")  # DEBUG


def mcu_check(titan_list):
    mcu_totals = []
    files = titan_list
    for file in files:
        with open(file, 'r') as file:
            # read all content from a file using read()
            dvrlog = file.read()
            # check if string present or not
            for mcu_type in mcu_types:
                if mcu_type in dvrlog:
                    mcu_totals.append(mcu_type)
    for mcu_type in mcu_types:
        count = mcu_totals.count(mcu_type)
        print(f"MCU {mcu_type}: {count}")
        count = 0
    #  print(f"{fw_types}")  # DEBUG


#  print(f"{fw_totals}")  # DEBUG

def check_errors(titan_list):
    cameras = []
    vlost = 0
    io_error = 0
    watchdog_error = 0
    for file in file_list:
        lines = get_lines(file)
        for line in lines:
            if line.__contains__('One or more camera not working, system reset'):
                io_error += 1
            if line.__contains__('Dvr watchdog failed, restarting dvrsvr'):
                watchdog_error += 1
            if line.__contains__('signal lost'):
                vlost += 1
                var = format_string(line)
                # print(f"{var}")  # DEBUG
                var = format_camera(var)
                # (f"{var}")  # DEBUG
                var = var.split(":", 4)
                # print(f"{var}")  # DEBUG
                var = var.pop()
                # print(f"{var}")  # DEBUG
                cameras.append(var)

    print(f"VLOST: {vlost}")
    for camera in camera_names:
        count = cameras.count(camera)
        if count > 0:
            print(f"{camera} FAILURES: {count}")
    print(f"IO ERROR - SYSTEM RESET: {io_error}")
    print(f"WATCHDOG ERROR - RESTART DVRSVR: {watchdog_error}")


if __name__ == '__main__':
    print(f"STARTING PROGRAM")
    log = logger.init_logger()
    logger.start_log(log)
    file_list, log_count = scan()
    titan_count, titan_list = find_titans(file_list)
    print(f"TOTAL LOGS: {log_count}")
    print(f"TOTAL TITANS: {titan_count}")
    fw_check(titan_list)
    mcu_check(titan_list)
    check_errors(titan_list)
    #  print(f"{titan_list}")  # DEBUG
    input(f"PRESS ENTER TWICE (x2) TO QUIT PROGRAM")
    logger.end_log(log)
