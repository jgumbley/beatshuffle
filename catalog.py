from persist import Mix
from persist import add_mix
import os
import shelve
import random
import shutil 

def process_existing_structure(existing_path):
    list_of_files_to_process = []
    for directory in os.walk(existing_path):
        directory_path = directory[0]
        directory_files = directory[2]
        #
        for path_part in os.path.split(directory_path):
            last_path_part = path_part
        for file in directory_files:
            file_ext = file[-4:]
            if file_ext.lower() in '.mp3':
                list_of_files_to_process.append(
                        (directory_path + '\\' +  file, last_path_part)
                        )
    return list_of_files_to_process

def get_random_hash():
    hash = hex(random.getrandbits(128))[2:-1] 
    if len(hash) == 32:
        return hash
    else:
        return get_random_hash()


def move_file_to_store(current_loc, store, hash):
    shutil.copy(current_loc, store + hash + ".mp3")

# IN
mp3_files = "C:\\Users\\Steve\\Music\\mixes"

# OUT
tnz_store = "c:\\Users\\Steve\\Python\\tnz\\tnz_store\\"

# main method
if __name__=="__main__":
    mixes = []
    for item in process_existing_structure(mp3_files):
        mix = Mix(get_random_hash())
        mix.add_tag(item[1])
        move_file_to_store(item[0], tnz_store, mix.hash)
        add_mix(mix)
