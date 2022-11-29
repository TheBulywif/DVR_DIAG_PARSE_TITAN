import os
import easygui
from classes import dvr

hostname = ""
firmware = ""
mcu = ""
model = ""
global rcmi, rcms, ksc, qdvr, csnw, ignon, pwroff, vsgnl, vsgnlon
video_cameras = []
dvrs = {
    "Name": [],
    "Model": [],
    "Firmware": [],
    "MCU": []
}


def select_folder():
    path = easygui.diropenbox("Select DVRLog Folder", "Select DVRLog Folder")
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
    print(f"**** SCANNING {folder} FOR LOGS ****")
    for root, dirs, files in os.walk(folder, topdown=False):
        if root.__contains__('TDVideo'):
            for name in files:
                if name.startswith("dvrlog"):
                    log = os.path.join(root, name)
                    if dvr_log_list.__contains__(log):
                        pass
                    else:
                        dvr_log_list.append(log)
    print(f"**** SCAN COMPLETE ****")
    print(f"**** LOGS FOUND: {len(dvr_log_list)} ****\n")
    return dvr_log_list


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

def hostname(line):
    if line.__contains__('hostname'):
        temp_list = line.split(":", 5)
        var = temp_list.pop()
        formatted_var = format_string(var)
        hostname = f"{formatted_var}"
        dvrs.

def firmware(line):
    if line.__contains__('DVR Firmware'):
        temp_list = line.split(":", 5)
        var = temp_list.pop()
        formatted_var = format_string(var)
        firmware = f"{formatted_var}"
        if firmware.__contains__('TITAN'):
            model = "Zeus Titan"
    return firmware


def mcu(line):
    if line.__contains__('MCU version'):
        temp_list = line.split(":", 6)
        var = temp_list.pop()
        formatted_var = format_string(var)
        mcu = f"{formatted_var}"
    return mcu


def recordMode(line):
    if line.__contains__('Record initialized'):
        rcmi += 1


def filter_log(lines):
    for line in lines:
        if line.__contains__('DVR Firmware'):
            temp_list = line.split(":", 5)
            var = temp_list.pop()
            formatted_var = format_string(var)
            firmware = f"{formatted_var}"
            if firmware.__contains__('TITAN'):
                model = "Zeus Titan"
        elif line.__contains__('MCU version'):
            temp_list = line.split(":", 6)
            var = temp_list.pop()
            formatted_var = format_string(var)
            mcu = f"{formatted_var}"
        elif line.__contains__('Record initialized'):
            rcmi += 1
        elif line.__contains__('Recording stopped'):
            rcms += 1
        elif line.__contains__('Kill signal captured'):
            ksc += 1
        elif line.__contains__('shutdown code'):
            qdvr += 1
        elif line.__contains__('One or more camera not working, system reset'):
            csnw += 1
        elif line.__contains__('hostname'):
            temp_list = line.split(":", 5)
            var = temp_list.pop()
            formatted_var = format_string(var)
            hostname = f"{formatted_var}"
        elif line.__contains__('Igniton On'):
            ignon += 1
        elif line.__contains__('Power off'):
            pwroff += 1
        elif line.__contains__('video signal lost'):
            vsgnl += 1
            temp_cam = line.split(":", 6)
            temp_cam = temp_cam.pop()
            # print(f"POPPED LINE: {temp_cam}")
            temp_cam = format_string(temp_cam)
            formatted_var = format_camera(temp_cam)
            # print(f"Camera test: {formatted_var}")
            if video_cameras.__contains__(formatted_var):
                pass
            else:
                video_cameras.append(formatted_var)
        elif line.__contains__('video signal on'):
            vsgnlon += 1
        elif line.__contains__(''):
            pass
    print(f"----DVR DEMOGRAPHICS----")
    print(f"DVR NAME: {hostname}")
    print(f"DVR MODEL: {model}")
    print(f"FIRMWARE VERSION: {firmware}")
    print(f"MCU VERSION: {mcu}")
    print(f"IGNITION ON COUNT: {ignon}")
    print(f"RECORDING INITIALIZED COUNT: {rcmi}")
    print(f"POWER OFF COUNT: {pwroff}")
    print(f"RECORDING STOPPED COUNT: {rcms}")
    print(f"KILL SIGNAL COUNT: {ksc}")
    print(f"DVR SHUTDOWN COUNT: {qdvr}")
    print(f"\n----DVR ERRORS----")
    print(f"VIDEO SIGNAL LOST COUNT: {vsgnl}")
    print(f"VIDEO SIGNAL ON COUNT: {vsgnlon}")
    print(f"VIDEO LOSS WITHOUT RECOVERIES: {abs(vsgnlon - vsgnl)}")
    if vsgnl >= 1:
        print(f"CAMERAS WITH SIGNAL LOSS: ")
        for camera in video_cameras:
            print(f"          {camera}")

    print(f"IO - CAMERA SYSTEM NOT WORKING COUNT: {csnw}")


def parse(dvr_log_list):
    for dvr in dvr_log_list:
        file = dvr
        try:
            print(f"**** SCANNING {file} ****")
            lines = read_log(file)
            print(f"**** SCAN COMPLETE ****")
            print(f"**** PARSING ****\n")
            filter_log(lines)
            print(f"\n**** PARSING COMPLETE ****\n")
        except UnicodeDecodeError as e:
            print(f"{e} --**** POTENTIALLY CORRUPT - REMOVING FROM LIST ****--")
            dvr_log_list.remove(file)
            parse(dvr_log_list)


if __name__ == '__main__':
    file_list = scan()
    parse(file_list)
    input("PRESS ENTER TWICE (x2) TO QUIT PROGRAM...")
