import os
from datetime import datetime
import psutil
import easygui


def select_file():
    path = easygui.fileopenbox()
    return path


def get_timestamp():
    ctime = datetime.now()
    ctime = ctime.strftime("%d/%m/%Y %H:%M:%S")
    return ctime


def read_log(file):
    lines = []
    count = 0
    with open(file, 'r') as log:
        while True:
            count += 1
            line = log.readline()
            if len(line) > 1:
                lines.append(f"Line {count} L{len(line)}: {line.strip()}")
            elif len(line) <= 1:
                pass
            if not line:
                break
    return lines


def parseRecMode(lines):
    var = 0
    for line in lines:
        if line.__contains__('Record initialized'):
            var += 1
    print(f"Enter Record Mode: {var}")
    return f"Enter Record Mode: {var}"


def parseExitRecMode(lines):
    var = 0
    for line in lines:
        if line.__contains__('Recording stopped'):
            var += 1
    print(f"Exit Record Mode: {var}")
    return f"Exit Record Mode: {var}"


def parseKillSignal(lines):
    var = 0
    for line in lines:
        if line.__contains__('Kill signal captured'):
            var += 1
    print(f"Kill Signal: {var}")
    return f"Kill Signal: {var}"


def parseQuitDVR(lines):
    var = 0
    for line in lines:
        if line.__contains__('Quit DVR'):
            var += 1
    print(f"DVR Shutdown: {var}")
    return f"DVR Shutdown: {var}"


def parseFlashFormat(lines):
    var = 0
    for line in lines:
        if line.__contains__('is formated to FAT32 with label:PFATSD'):
            var += 1
    print(f"Flash Storage Formatted: {var}")
    return f"Flash Storage Formatted: {var}"


def parseFileBackup(lines):
    var = 0
    for line in lines:
        if line.__contains__('file back up done'):
            var += 1
    print(f"Transfers Completed: {var}")
    return f"Transfers Completed: {var}"


def parseMCUVersion(lines):
    var = ""
    for line in lines:
        if line.__contains__('MCU version'):
            var = line
    var = var[-30:]
    var = var[:-2]
    print(f"MCU Version: {var}")
    return f"MCU Version: {var}"


def parseDVRFirmware(lines):
    var = ""
    for line in lines:
        if line.__contains__('DVR Firmware'):
            var = line
    var = var[-26:]
    var = var[:-2]
    print(f"Firmware Version: {var}")
    return f"Firmware Version: {var}"


def parseTestHours(lines):
    var = 0
    for line in lines:
        if line.__contains__('Record initialized'):
            var += 1
    print(f"Hours of Recording: {var * .5}")
    return var * .5


def find_dvrlogs():
    dvr_log_list = []
    log_count = 0
    partitions = psutil.disk_partitions()
    dir_count = 0
    for partition in partitions:
        drive = partition.device
        temp_count = 0
        # logger.info('Looking for TDVideo Directory & DVRLogs on: ' + str(drive))
        for root, dirs, files in os.walk(drive, topdown=False):
            temp_count += 1
            if root.__contains__('TDVideo'):
                for name in files:
                    if name.startswith("dvrlog"):
                        log = os.path.join(root, name)
                        if dvr_log_list.__contains__(log):
                            pass
                        else:
                            log_count += 1
                            dvr_log_list.append(log)
        dir_count += temp_count
    return dvr_log_list


def parse(dvr_log_list):
    try:
        for dvr in dvr_log_list:
            file = dvr
            print(f"Checking {file}")
            with open(file) as dvr_log:
                lines = read_log(dvr_log)
                filters = [parseMCUVersion(lines), parseDVRFirmware(lines), parseRecMode(lines), parseExitRecMode(lines),
                           parseKillSignal(lines), parseQuitDVR(lines), parseFlashFormat(lines), parseFileBackup(lines)]
                print(f"")
    except UnicodeDecodeError as e:
        print(f"{e} -- potentially corrupt. Renaming and running parse again.")
        os.rename(file, f"corrupt{file}")
        parse(dvr_log_list)


if __name__ == '__main__':
    print(f"Finding DVRLogs....")
    dvr_log_list = find_dvrlogs()
    print(f"DVRLogs Found:")
    print(dvr_log_list)
    parse(dvr_log_list)
