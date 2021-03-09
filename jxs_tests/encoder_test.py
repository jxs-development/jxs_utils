import utilities
import subprocess


def encode(full_flags, index):
    print(index)
    utilities.check_flag_is_writable(full_flags[index])
    subprocess.run(full_flags[index])


def main():
    full_flags = utilities.encoder_full_flag_generator()
    total_test = True
    for extension in full_flags:
        for index in range(len(full_flags[extension]["reference"])):
            encode(full_flags[extension]["reference"], index)
            encode(full_flags[extension]["to_check"], index)
            test = utilities.file_cmp(full_flags[extension]["to_check"][index].split()[-1], full_flags[extension]["reference"][index].split()[-1])
            print(full_flags[extension]["to_check"][index].split()[-1], full_flags[extension]["reference"][index].split()[-1],"files")
            if test:
                print("OK")
            else:
                total_test = False
                print("BAD on",full_flags[extension]["to_check"][index].split()[-1], full_flags[extension]["reference"][index].split()[-1])
    print("Total test:", total_test)
    # reference_encoded_image_list = utilities.get_encoded_image_list("tmp/reference_encoded/")
    # to_check_encoded_image_list = utilities.get_encoded_image_list("tmp/to_check_encoded/")
    # test_ok = True
    # for i in range(len(reference_encoded_image_list)):
    #     if not utilities.file_cmp(reference_encoded_image_list[i], to_check_encoded_image_list[i]):
    #         test_ok = False
    #         break
    # if test_ok:
    #     print("OK")
    # else:
    #     print("BAD on", reference_encoded_image_list[i], to_check_encoded_image_list[i])


if __name__ == "__main__":
    main()
