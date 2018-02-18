import re
import collections

KV_REGEXP = re.compile(r'(\w*)(?:\s)(.*)')

KeyValue = collections.namedtuple('KeyValue', ('key', 'value',))

def parse_stats(contents):
    for line in contents.splitlines():
        match = re.match(KV_REGEXP, line)
        if match:
            yield KeyValue(*match.groups())
