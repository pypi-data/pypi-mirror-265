import contextlib
import socket
import time
from dataclasses import dataclass, asdict
from typing import Callable, Generator

import requests


@dataclass
class CameraSpec:
    """Info to connect to camera."""

    ip: str
    username: str | None
    password: str | None


@dataclass
class Controls:
    """Camera controls."""

    pan: int
    tilt: int
    zoom: int
    focus: int


@dataclass
class Settings:
    """Camera settings."""

    iris: int | None
    shutter: int | None
    gain: int | None
    drc: int | None
    saturation: int | None
    hue: int | None
    brightness: int | None
    contrast: int | None
    sharpness: int | None
    gamma: int | None
    color_temperature: int | None
    noise2d: int | None
    noise3d: int | None


_sockets: dict[str, socket.socket] = {}


@contextlib.contextmanager
def _with_socket(camera: CameraSpec, timeout: float = 0.1) -> Generator[socket.socket, None, None]:
    """Return a context manager that provides a socket connection."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((camera.ip, 5678))
    try:
        yield sock
    finally:
        sock.close()


def _send_command(camera: CameraSpec, command: str, query: bool = False, timeout: float = 0.1) -> bytes:
    """Send a command to the camera."""
    print(f"Sending command {command}")
    with _with_socket(camera, timeout=timeout) as sock:
        if query:
            with contextlib.suppress(socket.timeout):
                sock.recv(1024**2)
        preamble = b"\x81" + (b"\x09" if query else b"\x01")
        terminator = b"\xff"
        sock.sendall(preamble + bytearray.fromhex(command) + terminator)
        with contextlib.suppress(socket.timeout) if not query else contextlib.nullcontext():
            return sock.recv(1024)


def _hex_digits(value: int, digits: int) -> str:
    """Return the hex string representation of a value with a fixed number of digits."""
    str_value = f"{value:0{digits}x}"
    return " ".join(f"0{x}" for x in str_value)


def _mod4(value: int) -> int:
    """Return the value modulo 4 hex digits."""
    if value < 0:
        return (value - 1) + 2**16
    return value


# The minimum and maximum values for each command.
_COMMAND_LIMITS: dict[str, tuple[int, int]] = {
    "pan": (-2447, 2448),  # 14.4 steps per degree
    "tilt": (-430, 1296),  # 14.4 steps per degree
    "zoom": (0, 16384),
    "focus": (0, 8192),
    "iris": (0, 12),
    "shutter": (1, 17),
    "gain": (0, 7),
    "drc": (0, 8),
    "saturation": (0, 14),
    "hue": (0, 14),
    "brightness": (0, 14),
    "contrast": (0, 14),
    "sharpness": (0, 15),
    "gamma": (0, 4),
    "color_temperature": (0, 55),
    "noise2d": (0, 5),
    "noise3d": (0, 8),
}

# Conversion from commands integers to hex byte strings. Some commands can translate into multiple
#   commands strings if we need to enable a specific setting first. For example, before setting focus,
#   we need to enable manual focus mode.
# See the camera's manual at https://www.adorama.com/col/productManuals/PT30XSDIGYG2.pdf
#   and https://ptzoptics.com/wp-content/uploads/2020/11/PTZOptics-VISCA-over-IP-Rev-1_2-8-20.pdf
_PTZ_FUNCTIONS: dict[str, Callable[[int, int], list[str]]] = {
    "pan_tilt": lambda pan, tilt: [f"06 02 18 14 {_hex_digits(_mod4(pan), 4)} {_hex_digits(_mod4(tilt), 4)}"],
    # Set to manual focus mode, unlock focus, set zoom and focus, and lock focus
    "zoom_focus": lambda zoom, focus: [
        "04 38 03",
        "04 68 03",
        f"04 47 {_hex_digits(zoom, 4)} {_hex_digits(focus, 4)}",
        "04 68 02",
    ],
}
_COMMAND_FUNCTIONS: dict[str, Callable[[int], list[str]]] = {
    # Select manual exposure mode before adjusting exposure settings
    "iris": lambda value: ["04 39 03", f"04 4B 00 00 {_hex_digits(value, 2)}"],
    "shutter": lambda value: ["04 39 03", f"04 4A 00 00 {_hex_digits(value, 2)}"],
    "gain": lambda value: ["04 39 03", f"04 0C 00 00 {_hex_digits(value, 2)}"],
    "drc": lambda value: ["04 39 03", f"04 25 00 00 {_hex_digits(value, 2)}"],
    "hue": lambda value: [f"04 4F 00 00 00 {_hex_digits(value, 1)}"],
    "brightness": lambda value: [f"04 A1 00 00 {_hex_digits(value, 2)}"],
    "contrast": lambda value: [f"04 A2 00 00 {_hex_digits(value, 2)}"],
    "sharpness": lambda value: ["04 05 03", f"04 42 00 00 {_hex_digits(value, 2)}"],
    "gamma": lambda value: [f"04 5B {_hex_digits(value, 1)}"],
    # Select color temperature white balance mode before adjusting color temperature
    "color_temperature": lambda value: ["04 35 20", f"04 20 {_hex_digits(value, 2)}"],
    "noise2d": lambda value: ["04 50 03", f"04 53 {_hex_digits(value, 1)}"],
    "noise3d": lambda value: [f"04 54 {_hex_digits(value, 1)}"],
}


def apply_controls(camera: CameraSpec, controls: Controls) -> None:
    """Apply the controls to the camera."""
    for control, value in asdict(controls).items():
        min_value, max_value = _COMMAND_LIMITS[control]
        assert min_value <= value <= max_value, f"{control} value out of range"
    commands = [
        *_PTZ_FUNCTIONS["pan_tilt"](controls.pan, controls.tilt),
        *_PTZ_FUNCTIONS["zoom_focus"](controls.zoom, controls.focus),
    ]
    for command in commands:
        _send_command(camera, command, timeout=2.0)


def _parse_response(response: bytes) -> int:
    digits = [int(x) for x in response]
    if digits[0] > 8:
        digits[0] -= 16
        digits[-1] += 1
    return sum(digit * 16 ** (len(digits) - i - 1) for i, digit in enumerate(digits))


def read_controls(camera: CameraSpec) -> Controls:
    """Read the current state of controls from the camera."""
    pan_tilt_response = _send_command(camera, "06 12", query=True)
    zoom_response = _send_command(camera, "04 47", query=True)
    focus_response = _send_command(camera, "04 48", query=True)

    for resp in (pan_tilt_response, zoom_response, focus_response):
        assert resp[:2] == b"\x90\x50", f"Invalid response {list(resp)}"

    pan = _parse_response(pan_tilt_response[2:6])
    tilt = _parse_response(pan_tilt_response[6:10])
    zoom = _parse_response(zoom_response[2:6])
    focus = _parse_response(focus_response[2:6])

    return Controls(pan=pan, tilt=tilt, zoom=zoom, focus=focus)


def read_autofocus_value(camera: CameraSpec) -> int:
    """Turn the camera into autofocus mode and get the focus value that the camera thinks is in focus."""
    _send_command(camera, "04 68 03")  # Unlock focus
    _send_command(camera, "04 38 02")  # Set to autofocus mode
    time.sleep(5)  # Wait for the camera to focus
    _send_command(camera, "04 38 03")  # Set to manual focus mode
    _send_command(camera, "04 68 02")  # Lock focus

    focus_response = _send_command(camera, "04 48", query=True)
    assert focus_response[:2] == b"\x90\x50", f"Invalid response {list(focus_response)}"
    return _parse_response(focus_response[2:6])


def apply_settings(camera: CameraSpec, settings: Settings) -> None:
    """Apply the settings to the camera."""
    settings_dict: dict[str, int | None] = asdict(settings)
    commands: list[str] = []
    for setting, value in settings_dict.items():
        if value is None:
            continue
        min_value, max_value = _COMMAND_LIMITS[setting]
        assert min_value <= value <= max_value, f"{setting} value out of range"
        if setting in _COMMAND_FUNCTIONS:
            commands.extend(_COMMAND_FUNCTIONS[setting](value))

    for command in commands:
        _send_command(camera, command)

    if settings.saturation is not None:
        requests.get(f"http://{camera.ip}/cgi-bin/param.cgi?post_image_value&saturation/{settings.saturation}")


def fetch_thumbnail(camera: CameraSpec) -> bytes:
    """Fetch the camera thumbnail."""
    requests.get(f"http://{camera.ip}/cgi-bin/snapshot.cgi?post_snapshot_conf&resolution=1920x1080")
    response = requests.get(f"http://{camera.ip}/snapshot.jpg")
    return response.content
