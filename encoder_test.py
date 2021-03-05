import utilities
import subprocess


def encode(full_flags):
    for full_flag in full_flags:
        print(full_flag)
        utilities.check_flag_is_writable(full_flag)
        subprocess.run(full_flag)


def main():
    full_flags = utilities.encoder_full_flag_generator()
    for extension in full_flags:
        for type_encoder in full_flags[extension]:
            encode(full_flags[extension][type_encoder])
    reference_encoded_image_list = utilities.get_encoded_image_list("tmp/reference_encoded/")
    to_check_encoded_image_list = utilities.get_encoded_image_list("tmp/to_check_encoded/")
    test_ok = True
    for i in range(len(reference_encoded_image_list)):
        if not utilities.file_cmp(reference_encoded_image_list[i], to_check_encoded_image_list[i]):
            test_ok = False
            break
    if test_ok:
        print("OK")
    else:
        print("BAD on", reference_encoded_image_list[i], to_check_encoded_image_list[i])


if __name__ == "__main__":
    main()
