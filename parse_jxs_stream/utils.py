reference_markers = {
    "XS_MARKER_SOC": 0xff10.to_bytes(2, byteorder="big"),
    "XS_MARKER_CAP": 0xff50.to_bytes(2, byteorder="big"),
    "XS_MARKER_PIH": 0xff12.to_bytes(2, byteorder="big"),

}


def field_description(name: str, data: bytes):  # todo type return
    description = {"name": name, "bytes": data}
    return description


def read_from_file(file, index, byte_count):  # todo type return
    data = file.read(byte_count)
    index += byte_count
    return data, index


def check_marker(name, value):  # todo type return
    if not value == reference_markers[name]:
        raise ValueError("wrong", name)


def parse_pic_header(file, index):  # todo type return
    parsed = {}
    # read start markers
    XS_MARKER_SOC, index = read_from_file(file, index, 2)  # read XS_MARKER_SOC
    check_marker("XS_MARKER_SOC", XS_MARKER_SOC)
    parsed[index] = field_description("XS_MARKER_SOC", XS_MARKER_SOC)
    XS_MARKER_CAP, index = read_from_file(file, index, 2)  # read XS_MARKER_CAP
    check_marker("XS_MARKER_CAP", XS_MARKER_CAP)
    parsed[index] = field_description("XS_MARKER_CAP", XS_MARKER_CAP)
    len_of_cap, index = read_from_file(file, index, 2)  # read len_of_cap
    parsed[index] = field_description("len_of_cap", len_of_cap)
    # reference code presupposes len_of_cap = 2
    # read picture header
    XS_MARKER_PIH, index = read_from_file(file, index, 2)  # read XS_MARKER_PIH
    check_marker("XS_MARKER_PIH", XS_MARKER_PIH)
    parsed[index] = field_description("XS_MARKER_PIH", XS_MARKER_PIH)
    return parsed, index
