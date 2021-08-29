import utils


def parse_jxs_picture(file):
    index = 0
    parsed, index = utils.parse_pic_header(file, index)
    return parsed


def main():
    file =  open("stream.jxs","rb")
    print(parse_jxs_picture(file))

if __name__ == '__main__':
    main()