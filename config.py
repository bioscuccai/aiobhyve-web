import configparser

CONFIG_FILE='config.ini'

ISO_DIR='/usr/iso'
IMAGE_DIR='/usr/vms'

def get_isos():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    isos_str = config['main']['isos']
    isos = isos_str.split(',')
    return isos

def set_isos(isos):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config['main']['isos'] = ','.join(isos)
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def get_disks():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    disks_str = config['main']['disks']
    disks = disks_str.split(',')
    return disks

def set_disks(disks):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    config['main']['disks'] = ','.join(disks)
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def setup():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    ISO_DIR=config['main']['iso_dir']
    IMAGE_DIR=config['main']['image_dir']

setup()