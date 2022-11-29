import os
import easygui
from debug import logger

video_cameras = []
dvrs = {
    "Name": [],
    "Model": [],
    "Firmware": [],
    "MCU": []
}


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


def parse_host(line):
    hostname = ""
    if line.__contains__('hostname'):
        temp_list = line.split(":", 5)
        var = temp_list.pop()
        formatted_var = format_string(var)
        hostname = f"{formatted_var}"
    return hostname


def parse_fw(line):
    firmware = ""
    model = ""
    if line.__contains__('DVR Firmware'):
        temp_list = line.split(":", 5)
        var = temp_list.pop()
        formatted_var = format_string(var)
        firmware = f"{formatted_var}"
        if "TITAN" in firmware:
            model = "Zeus Titan"
        elif "ZEUSHD16" in firmware:
            model = "Zeus Platinum"
    return firmware, model


def parse_mcu(line):
    mcu = ""
    if line.__contains__('MCU version'):
        temp_list = line.split(":", 6)
        var = temp_list.pop()
        formatted_var = format_string(var)
        mcu = f"{formatted_var}"
    return mcu


def update_dictionary(file, hostname, model, firmware, mcu):
    if len(hostname) < 1:
        dvrs.update({"Name": file})
        dvrs.update({"Model": model})
        dvrs.update({"firmware": firmware})
        dvrs.update({"MCU": mcu})
    #  print(f"{dvrs}")
    elif len(hostname) > 0:
        dvrs.update({"Name": hostname})
        dvrs.update({"Model": model})
        dvrs.update({"firmware": firmware})
        dvrs.update({"MCU": mcu})
    #  print(f"{dvrs}")


def filter_log(lines):
    for line in lines:
        hostname = parse_host(line)
        firmware, model = parse_fw(line)
        mcu = parse_mcu(line)
    log.info(f"----DVR DEMOGRAPHICS----")
    log.info(f"DVR NAME: {hostname}")
    log.info(f"DVR MODEL: {model}")
    log.info(f"FIRMWARE VERSION: {firmware}")
    log.info(f"MCU VERSION: {mcu}")
    print(f"{hostname, model, firmware, mcu}")
    return hostname, model, firmware, mcu


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
    file_list = scan()
    for file in file_list:
        log.info(f"COPYING LINES FROM LOGFILE TO LIST")
        lines = get_lines(file)
        log.info(f"LINES COPIED")
        log.info(f"PARSING LINES")
        hostname, model, firmware, mcu = filter_log(lines)
        update_dictionary(file, hostname, model, firmware, mcu)
    input("PRESS ENTER TWICE (x2) TO QUIT PROGRAM...")
    logger.end_log(log)
