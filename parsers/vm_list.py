import os

def list_vms():
  try:
    files = os.listdir('/dev/vmm')
  except FileNotFoundError:
    return []
  return files
