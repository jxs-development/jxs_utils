import utilities
import subprocess
import statistics


def decode(args):
    print(args)
    out = subprocess.run(args)
    return out.returncode


def main():
    times = []
    tets_len = 100
    for i in range(100):
        times.append(
            # decode("..\jxs_cpp\cmake-build-release\jxs_decoder.exe bitstream_dataset/3840x2160/3.jxs tmp/3.ppm"))
            # decode("..\jxs_cpp\cmake-build-release\jxs_decoder.exe bitstream_dataset/1920x1080/3.jxs tmp/3.ppm"))
            decode("D:\dmitrienkomy\cpp\jxs\jxs cpp ref\jxs_cpp\out\\build\\x64-Release\jxs_decoder.exe bitstream_dataset/1920x1080/3.jxs tmp/3.ppm"))
    mean = sum(times) / tets_len
    stdev = statistics.stdev(times)
    print(f"mean {mean} \t stddev {stdev}")


if __name__ == '__main__':
    main()
