from pathlib import Path
import logging

def create_log_file(tmp_path,sensor, suffix):
    fp = tmp_path + "/" + sensor + "_" + suffix
    if not Path(fp).is_file():
        f = open(fp,"w+")
        f.write("0")
    f = open(fp,"r")
    fd = f.read()
    logging.debug("File " + sensor + "_" + suffix + " created")
    return fp

def FileContent(file):
    f = open(file,"r")
    fd = f.read()
    logging.debug("File Data (" + file + "): " + fd )
    return int(fd)

def WriteData(file,value):
    f = open(file,"w")        
    f.write(str(value))