import re
import subprocess

TAP_REGEXP=re.compile(r"^tap(\d*)\:")
UP_REGEXP=re.compile(r"<.*UP.*>")

def all_tap_lines():
    lines = subprocess.check_output(['ifconfig']).decode('utf8').split('\n')
    yield from (line for line in lines if re.match(TAP_REGEXP, line))

def all_taps():
    for tap in all_tap_lines():
        tap_split = tap.split(':')
        yield (tap_split[0], re.search(UP_REGEXP, tap) is not None,)

def tap_choices(taps):
    for (tap_if, is_up) in taps:
        tap_name = tap_if
        if is_up:
            tap_name = "{} - UP".format(tap_name)
        yield (tap_if, tap_name,)
