from collections import namedtuple
import re

Lease = namedtuple('Lease', ('timestamp', 'mac', 'ip', 'hostname'))

lease_regexp = re.compile(r'(\d*) ([\w\d\:]*) ([\d\.]*) (\w*)')

def parse_lease(lines):
  for line in lines:
    parsed = re.match(lease_regexp, line)
    yield Lease(*parsed.groups())

def list_leases():
  lines = open('/var/db/dnsmasq.leases').readlines()
  yield from parse_lease(lines)
