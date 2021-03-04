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


def get_original_images_paths_dict():
    dir = {}
    rootdir = "image_dataset"
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


def get_original_images_paths_list():
    rootdir = "image_dataset"
    folder = []
    original_images_paths = []
    for i in os.walk(rootdir):
        folder.append(i)
    for address, dirs, files in folder:
        for file in files:
            original_images_paths.append(address + '/' + file)

    return original_images_paths


def encoder_paths_generator_dict(encoded_prefix):
    encoder_paths_dict_reference = {}
    tmp_dir = "tpm"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    original_images_paths_list = get_original_images_paths_list()
    for original_image_path in original_images_paths_list:
        format_index_start = original_image_path.find("\\", original_image_path.find("\\"))
        format_index_end = original_image_path.find("\\",
                                                    original_image_path.find("\\", original_image_path.find("\\") + 2))
        format = original_image_path[format_index_start + 1:format_index_end]
        if format not in encoder_paths_dict_reference:
            encoder_paths_dict_reference[format] = []
        extention_dot_index = original_image_path.rfind('.')
        original_images_path_reference_encoded = encoded_prefix + format + original_image_path[
                                                                           format_index_end:extention_dot_index] + '.jxs'
        encoder_paths_dict_reference[format].append(original_image_path + " " + original_images_path_reference_encoded)
    return encoder_paths_dict_reference


def encoder_paths_generator_dict_reference():
    reference_encoded_prefix = 'tmp/reference_encoded/'
    return encoder_paths_generator_dict(reference_encoded_prefix)


def encoder_paths_generator_dict_own():
    reference_encoded_prefix = 'tmp/own_encoded/'
    return encoder_paths_generator_dict(reference_encoded_prefix)


def encoder_ppm_full_flag_generator(path_list, param_flags): #todo
    print("path ref", path_list)
    print("params", param_flags)


full_flag_generators = {
    "ppm": encoder_ppm_full_flag_generator
}


def encoder_full_flag_generator():
    full_flags_reference = {}
    full_flags_own = {}
    for full_flag_generator in full_flag_generators:
        path_list_reference = encoder_paths_generator_dict_reference()
        path_list_own = encoder_paths_generator_dict_reference()
        param_flags = encoder_param_flag_generator()
        full_flags_reference[full_flag_generator] = {
            "reference": full_flag_generators[full_flag_generator](path_list_reference, param_flags),
            "own": full_flag_generators[full_flag_generator](path_list_own, param_flags)
        }

# print(parse_range_config("config\encoder_params_range.config"))
# print(encoder_param_flag_generator())
# print(get_original_images_paths_list())
# print(encoder_paths_generator_dict_reference())
print()
