import utilities
import subprocess


def decode(args):
    print(args)
    subprocess.run(args)


def main():
    full_decoder_args = utilities.decoder_full_args_generator()
    total_test = True
    for index in range(len(full_decoder_args["reference"])):
        decode(full_decoder_args["reference"][index])
        decode(full_decoder_args["to_check"][index])
        test = utilities.file_cmp("tmp/reference.ppm","tmp/to_check.ppm")
        if test:
            print("OK")
        else:
            total_test = False
    print(total_test)



if __name__ == '__main__':
    main()
