import struct

import numpy as np

from cratonapi.datacontainers import WellCurve


def parse(message: bytes) -> np.ndarray:
    if len(message) < 16:
        raise RuntimeError("Incomplete message!")
    signature = message[0:4].decode("utf-8")
    if signature != "WSPM":
        raise RuntimeError("Incorrect signature!")
    size, operation, request, uid = struct.unpack("<IHHI", message[4:16])
    if operation != 3 or request != 3:
        raise RuntimeError("Incorrect operation or request codes!")
    if len(message) - 8 != size:
        raise RuntimeError("Incomplete message!")
    curves_count = struct.unpack("<I", message[16:20])[0]
    curve_list = np.empty(curves_count, WellCurve)
    offset = 0
    for curve_num in range(curves_count):
        curve_type, curve_name_symbols_count = struct.unpack(
            "<BH", message[20 + offset : 23 + offset]
        )
        curve_name_bytes = message[23 + offset : 23 + offset + curve_name_symbols_count]
        offset += curve_name_symbols_count
        curve_name = curve_name_bytes.decode("cp1251")
        points_count = struct.unpack("<I", message[23 + offset : 27 + offset])[0]
        point_values = np.empty(points_count)
        point_depths = np.empty(points_count)
        for point in range(points_count):
            point_value, point_depth = struct.unpack(
                "<dd", message[27 + offset : 43 + offset]
            )
            point_values[point] = point_value
            point_depths[point] = point_depth
            offset += 16
        offset += 7
        curve_list[curve_num] = WellCurve(
            curve_type, curve_name, point_values, point_depths
        )
    return curve_list
