import os
from functools import reduce


def file_cmp(file1_path: str, file2_path: str):
    file_is_identical = False
    file1 = open(file1_path, "rb")
    file2 = open(file2_path, "rb")
    byte1 = file1.read(1)
    byte2 = file2.read(1)
    while byte1 and byte2:
        if byte1 != byte2:
            break
        byte1 = file1.read(1)
        byte2 = file2.read(1)
        if not byte1 and not byte2:
            file_is_identical = True
            break
    return file_is_identical


def parse_non_range_config(name: str): 
    config = {}
    file = open(name, 'r')
    lines = file.readlines()
    for line in lines:
        name, attribute = line.split()
        config[name] = attribute
    return config


def parse_range_config(name: str):
    config = {}
    file = open(name, 'r')
    lines = file.readlines()
    for line in lines:
        params = line.split()
        config[params[0]] = params[1:]
    return config


def encoder_param_flag_generator():
    flags = parse_range_config("config\encoder_params_range.config")
    key_max_len_of_list_flags = ''
    max_len = -1
    for flag in flags:
        len_of_list_of_flags = len(flags[flag])
        if max_len < len_of_list_of_flags:
            key_max_len_of_list_flags = flag
            max_len = len_of_list_of_flags
    list_of_flags_combinations = []
    for i in range(max_len):
        flags_combinations = ''
        for flag in flags:
            len_of_list_of_flags = len(flags[flag])
            flags_combinations = flags_combinations + flag + " " + flags[flag][i % len_of_list_of_flags] + " "
        list_of_flags_combinations.append(flags_combinations)
    return list_of_flags_combinations

def get_original_images_dirs():
    dir = {}
    rootdir = "image_dataset/"
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir

def encoder_paths_generator():
    pass

def encoder_ppm_full_flag_generator():
    flags = []
    param_flag = encoder_param_flag_generator()


# print(parse_range_config("config\encoder_params_range.config"))
# print(encoder_param_flag_generator())
print(get_original_images_dirs())
