import datetime
import csv
import sys
import random
import os


def get_log(message, log_type='INFO'):
    time_string = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_mess = log_type + ": " + time_string + ' - '+ message
    return log_mess

def write_config(base_path, file_name, config: dict):
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    dir = f"{base_path}/{file_name}"
    try:
        with open(dir, 'w', newline='\n') as f: 
            pointer = csv.writer(f)
            pointer.writerow(config.keys()) 
            pointer.writerow(config.values())
    except:
        return True, f"could not write config {file_name}"
    
    return False, f"write config {file_name} successfully"

def load_config(base_path, file_name):
    config = {}
    dir = f"{base_path}/{file_name}"
    try:
        with open(dir, 'r', newline='\n') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            keys, values = [], []
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    keys = row
                else:
                    values = row
                    break
        
        # load into config
        for k, v in zip(keys, values):
            config[k] = v
    except:
        return True, f"could not load config {file_name}", {}
    
    return False, f"load config {file_name} successfully", config

def bytes_random(rand_seed, length):
    if length == 0:
        return b''
    integer = rand_seed.getrandbits(length * 8)
    result = integer.to_bytes(length, sys.byteorder)
    return result

