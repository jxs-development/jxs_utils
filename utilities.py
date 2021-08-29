import os
from functools import reduce


def check_flag_is_writable(full_flag: str):
    path = full_flag.split()[-1]
    path = path[0:path.rfind('/')]
    # print(path)
    os.makedirs(path, exist_ok=True)


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
    max_len = -1
    for flag in flags:
        len_of_list_of_flags = len(flags[flag])
        if max_len < len_of_list_of_flags:
            max_len = len_of_list_of_flags
    list_of_flags_combinations = []
    for i in range(max_len):
        flags_combinations = ''
        for flag in flags:
            len_of_list_of_flags = len(flags[flag])
            flags_combinations = flags_combinations + flag + " " + flags[flag][i % len_of_list_of_flags] + " "
        list_of_flags_combinations.append(flags_combinations)
    return list_of_flags_combinations


def get_original_images_paths_dict(rootdir="image_dataset"):
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


def get_input_files_paths_list(rootdir="image_dataset"):
    folder = []
    original_images_paths = []
    for i in os.walk(rootdir):
        folder.append(i)
    for address, dirs, files in folder:
        for file in files:
            original_images_paths.append(address + '/' + file)

    return original_images_paths


def get_encoded_image_list(encoded_prefix):
    original_images_paths_list = get_input_files_paths_list()
    images_path_encoded_list = []
    for original_image_path in original_images_paths_list:
        format_index_start = original_image_path.find("\\", original_image_path.find("\\"))
        format_index_end = original_image_path.find("\\",
                                                    original_image_path.find("\\", original_image_path.find("\\") + 2))
        format = original_image_path[format_index_start + 1:format_index_end]
        extension_dot_index = original_image_path.rfind('.')
        images_path_encoded = encoded_prefix + format + original_image_path[
                                                        format_index_end:extension_dot_index] + '.jxs'
        images_path_encoded_list.append(images_path_encoded)
    return images_path_encoded_list


def encoder_paths_generator_dict(encoded_prefix):  # todo copy code in get_encoded_image_list refactor
    encoder_paths_dict = {}
    tmp_dir = "tpm"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    original_images_paths_list = get_input_files_paths_list()
    for original_image_path in original_images_paths_list:
        format_index_start = original_image_path.find("\\", original_image_path.find("\\"))
        format_index_end = original_image_path.find("\\",
                                                    original_image_path.find("\\", original_image_path.find("\\") + 2))
        format = original_image_path[format_index_start + 1:format_index_end]
        if format not in encoder_paths_dict:
            encoder_paths_dict[format] = []
        extension_dot_index = original_image_path.rfind('.')
        images_path_encoded = encoded_prefix + format + original_image_path[
                                                        format_index_end:extension_dot_index] + '.jxs'
        encoder_paths_dict[format].append(original_image_path + " " + images_path_encoded)
    return encoder_paths_dict


def encoder_paths_generator_dict_reference():
    reference_encoded_prefix = 'tmp/reference_encoded/'
    return encoder_paths_generator_dict(reference_encoded_prefix)


def encoder_paths_generator_dict_to_check():
    reference_encoded_prefix = 'tmp/to_check_encoded/'
    return encoder_paths_generator_dict(reference_encoded_prefix)


def encoder_ppm_full_flag_generator(is_reference, path_list, param_flags):  # todo config bin path
    if is_reference:
        encoder_full_flag_prefix = "./reference_bin/jxs_encoder "
    else:
        encoder_full_flag_prefix = "./to_check_bin/jxs_encoder "
    full_flags = []
    for path in path_list:
        for params in param_flags:
            full_flags.append(encoder_full_flag_prefix + params + path)
    return full_flags


encode_full_flag_generators = {
    "ppm": encoder_ppm_full_flag_generator
}


def encoder_full_args_generator():
    full_flags = {}
    path_list_reference = encoder_paths_generator_dict_reference()
    path_list_to_check = encoder_paths_generator_dict_to_check()
    param_flags = encoder_param_flag_generator()
    for extension in encode_full_flag_generators:
        full_flags[extension] = {
            "reference": encode_full_flag_generators[extension](True, path_list_reference[extension], param_flags),
            "to_check": encode_full_flag_generators[extension](False, path_list_to_check[extension], param_flags)
        }
    return full_flags


def decoder_full_args_generator():
    full_flags = {}
    full_flags["to_check"] = []
    full_flags["reference"] = []
    params_bin = parse_non_range_config("config/bin.config")
    decoder_full_args_prefix_reference = "./reference_bin/jxs_decoder "
    decoder_full_args_prefix_to_check = params_bin["decoder_to_check"] + " "
    bitstream_paths = get_input_files_paths_list("bitstream_dataset")
    for bitstream_path in bitstream_paths:
        full_flags["reference"].append(decoder_full_args_prefix_reference + bitstream_path + " tmp/reference.ppm")
        full_flags["to_check"].append(decoder_full_args_prefix_to_check + bitstream_path + " tmp/to_check.ppm")
    return full_flags


