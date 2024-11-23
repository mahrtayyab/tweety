"""
Credit : https://github.com/iSarabjitDhiman/TweeterPy/tree/master/tweeterpy/tid
"""

import re
import bs4
import math
import time
import random
import base64
import hashlib
import httpx
from functools import reduce
from typing import Union, List
from .utils import float_to_hex, is_odd, base64_encode

ON_DEMAND_FILE_REGEX = re.compile(
    r"""['|\"]{1}ondemand\.s['|\"]{1}:\s*['|\"]{1}([\w]*)['|\"]{1}""", flags=(re.VERBOSE | re.MULTILINE))
INDICES_REGEX = re.compile(
    r"""(\(\w{1}\[(\d{1,2})\],\s*16\))+""", flags=(re.VERBOSE | re.MULTILINE))


def interpolate(from_list: List[Union[float, int]], to_list: List[Union[float, int]], f: Union[float, int]):
    if len(from_list) != len(to_list):
        raise Exception(f"Mismatched interpolation arguments {from_list}: {to_list}")
    out = []
    for i in range(len(from_list)):
        out.append(interpolate_num(from_list[i], to_list[i], f))
    return out


def interpolate_num(from_val: List[Union[float, int]], to_val: List[Union[float, int]], f: Union[float, int]):
    if all([isinstance(number, (int, float)) for number in [from_val, to_val]]):
        return from_val * (1 - f) + to_val * f

    if all([isinstance(number, bool) for number in [from_val, to_val]]):
        return from_val if f < 0.5 else to_val


def convert_rotation_to_matrix(rotation: Union[float, int]):
    rad = math.radians(rotation)
    return [math.cos(rad), -math.sin(rad), math.sin(rad), math.cos(rad)]


def convertRotationToMatrix(degrees: Union[float, int]):
    radians = degrees * math.pi / 180
    """
    [cos(r), -sin(r), 0]
    [sin(r), cos(r), 0]

    in this order:
    [cos(r), sin(r), -sin(r), cos(r), 0, 0]
    """
    cos = math.cos(radians)
    sin = math.sin(radians)
    return [cos, sin, -sin, cos, 0, 0]


class Cubic:
    def __init__(self, curves: List[Union[float, int]]):
        self.curves = curves

    def get_value(self, _time: Union[float, int]):
        start_gradient = end_gradient = start = mid = 0.0
        end = 1.0

        if _time <= 0.0:
            if self.curves[0] > 0.0:
                start_gradient = self.curves[1] / self.curves[0]
            elif self.curves[1] == 0.0 and self.curves[2] > 0.0:
                start_gradient = self.curves[3] / self.curves[2]
            return start_gradient * _time

        if _time >= 1.0:
            if self.curves[2] < 1.0:
                end_gradient = (self.curves[3] - 1.0) / (self.curves[2] - 1.0)
            elif self.curves[2] == 1.0 and self.curves[0] < 1.0:
                end_gradient = (self.curves[1] - 1.0) / (self.curves[0] - 1.0)
            return 1.0 + end_gradient * (_time - 1.0)

        while start < end:
            mid = (start + end) / 2
            x_est = self.calculate(self.curves[0], self.curves[2], mid)
            if abs(_time - x_est) < 0.00001:
                return self.calculate(self.curves[1], self.curves[3], mid)
            if x_est < _time:
                start = mid
            else:
                end = mid
        return self.calculate(self.curves[1], self.curves[3], mid)

    @staticmethod
    def calculate(a, b, m):
        return 3.0 * a * (1 - m) * (1 - m) * m + 3.0 * b * (1 - m) * m * m + m * m * m


class TransactionGenerator:
    DEFAULT_KEYWORD = "obfiowerehiring"
    ADDITIONAL_RANDOM_NUMBER = 3
    DEFAULT_ROW_INDEX = None
    DEFAULT_KEY_BYTES_INDICES = None

    def __init__(self, home_page_html: Union[bs4.BeautifulSoup, httpx.Response]):

        self.home_page_html = self.validate_response(home_page_html)
        self.DEFAULT_ROW_INDEX, self.DEFAULT_KEY_BYTES_INDICES = self.get_indices(self.home_page_html)
        self.key = self.get_key(response=self.home_page_html)
        self.key_bytes = self.get_key_bytes(key=self.key)
        self.animation_key = self.get_animation_key(key_bytes=self.key_bytes, response=self.home_page_html)

    def get_indices(self, home_page_html=None):
        key_byte_indices = []
        response = self.validate_response(home_page_html) or self.home_page_html
        on_demand_file = ON_DEMAND_FILE_REGEX.search(str(response))
        if on_demand_file:
            on_demand_file_url = f"https://abs.twimg.com/responsive-web/client-web/ondemand.s.{on_demand_file.group(1)}a.js"
            on_demand_file_response = httpx.get(on_demand_file_url)
            key_byte_indices_match = INDICES_REGEX.finditer(
                str(on_demand_file_response.text))
            for item in key_byte_indices_match:
                key_byte_indices.append(item.group(2))
        if not key_byte_indices:
            raise Exception("Couldn't get animation key indices")
        key_byte_indices = list(map(int, key_byte_indices))
        return key_byte_indices[0], key_byte_indices[1:]

    def validate_response(self, response: Union[bs4.BeautifulSoup, httpx.Response]):
        if not isinstance(response, (bs4.BeautifulSoup, httpx.Response)):
            raise Exception("invalid response")
        return response if isinstance(response, bs4.BeautifulSoup) else bs4.BeautifulSoup(response.content, 'lxml')

    def get_key(self, response=None):
        response = self.validate_response(response) or self.home_page_html
        element = response.select_one("[name='twitter-site-verification']")
        if not element:
            raise Exception("Couldn't get twitter site verification code")
        return element.get("content")

    def get_key_bytes(self, key: str):
        return list(base64.b64decode(bytes(key, 'utf-8')))

    def get_frames(self, response=None):
        response = self.validate_response(response) or self.home_page_html
        return response.select("[id^='loading-x-anim']")

    def get_2d_array(self, key_bytes: List[Union[float, int]], response, frames: bs4.ResultSet = None):
        if not frames:
            frames = self.get_frames(response)
        return [[int(x) for x in re.sub(r"[^\d]+", " ", item).strip().split()] for item in list(list(frames[key_bytes[5] % 4].children)[0].children)[1].get("d")[9:].split("C")]

    def solve(self, value, min_val, max_val, rounding: bool):
        result = value * (max_val-min_val) / 255 + min_val
        return math.floor(result) if rounding else round(result, 2)

    def animate(self, frames, target_time):
        from_color = [float(item) for item in [*frames[:3], 1]]
        to_color = [float(item) for item in [*frames[3:6], 1]]
        from_rotation = [0.0]
        to_rotation = [self.solve(float(frames[6]), 60.0, 360.0, True)]
        frames = frames[7:]
        curves = [self.solve(float(item), is_odd(counter), 1.0, False)
                  for counter, item in enumerate(frames)]
        cubic = Cubic(curves)
        val = cubic.get_value(target_time)
        color = interpolate(from_color, to_color, val)
        color = [value if value > 0 else 0 for value in color]
        rotation = interpolate(from_rotation, to_rotation, val)
        matrix = convert_rotation_to_matrix(rotation[0])
        str_arr = [format(round(value), 'x') for value in color[:-1]]
        for value in matrix:
            rounded = round(value, 2)
            if rounded < 0:
                rounded = -rounded
            hex_value = float_to_hex(rounded)
            str_arr.append(f"0{hex_value}".lower() if hex_value.startswith(
                ".") else hex_value if hex_value else '0')
        str_arr.extend(["0", "0"])
        animation_key = re.sub(r"[.-]", "", "".join(str_arr))
        return animation_key

    def get_animation_key(self, key_bytes, response):
        total_time = 4096
        row_index = key_bytes[self.DEFAULT_ROW_INDEX] % 16
        frame_time = reduce(lambda num1, num2: num1*num2,
                            [key_bytes[index] % 16 for index in self.DEFAULT_KEY_BYTES_INDICES])
        arr = self.get_2d_array(key_bytes, response)
        frame_row = arr[row_index]

        target_time = float(frame_time) / total_time
        animation_key = self.animate(frame_row, target_time)
        return animation_key

    def generate_transaction_id(self, method: str, path: str, response=None, key=None, animation_key=None, time_now=None):
        try:
            time_now = time_now or math.floor(
                (time.time() * 1000 - 1682924400 * 1000) / 1000)
            time_now_bytes = [(time_now >> (i * 8)) & 0xFF for i in range(4)]
            key = key or self.key or self.get_key(response)
            key_bytes = self.get_key_bytes(key)
            animation_key = animation_key or self.animation_key or self.get_animation_key(
                key_bytes, response)
            hash_val = hashlib.sha256(
                f"{method}!{path}!{time_now}{self.DEFAULT_KEYWORD}{animation_key}".encode()).digest()
            hash_bytes = list(hash_val)
            random_num = random.randint(0, 255)
            bytes_arr = [*key_bytes, *time_now_bytes, *
                         hash_bytes[:16], self.ADDITIONAL_RANDOM_NUMBER]
            out = bytearray(
                [random_num, *[item ^ random_num for item in bytes_arr]])
            return base64_encode(out).strip("=")
        except Exception as error:
            raise Exception(f"Couldn't generate transaction ID.\n{error}")


if __name__ == "__main__":
    pass
