from .await_process import exec_command, fire_command
import itertools
from enum import Enum

DISK_START = 3

class DiskType(Enum):
    AHCI_DISK = 0
    VIRTIO_DISK = 1
    ISO = 2

class BhyveVm:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.cores = int(kwargs['cores'])
        self.memory =int(kwargs['memory'])
        self.enable_framebuffer = kwargs.get('enable_framebuffer', False)
        self.framebuffer = int(kwargs['framebuffer'])
        self.bios = kwargs['bios']
        self.loader = kwargs['loader']
        self.console = kwargs['console']
        self.vnc_wait = kwargs.get('vnc_wait', False)

        self.hostbridge = kwargs.get('hostbridge', False)
        self.tap = kwargs.get('tap')
        self.serials = kwargs.get('serials', [])
        self.disks = kwargs.get('disks', [])
        self.isos = kwargs.get('isos', [])
        self.hostbridge_type = kwargs.get('hostbridge_type', 'type')

    def __repr__(self):
        return 'BhyveVm' + repr(self.__dict__)

    @staticmethod
    def bios_type_to_path(bios_type):
        if bios_type == 'uefi':
            return '/usr/local/share/uefi-firmware/BHYVE_UEFI.fd'
        else:
            return '/usr/local/share/uefi-firmware/BHYVE_UEFI_CSM.fd'

def create_command(vm):
    params = ['-AHPw', '-s 31:0,lpc']
    params.append('-c {}'.format(vm.cores))
    params.append('-m {}'.format(vm.memory))
    if vm.hostbridge:
        if vm.hostbridge_type == 'amd':
            params.append('-s 0:0,amd_hostbridge')
        else:
            params.append('-s 0:0,hostbridge')
    if vm.enable_framebuffer:
        params.append('-s 20,xhci,tablet')
        if vm.vnc_wait:
            params.append("-s 29:0,fbuf,tcp=127.0.0.1:{},w=1024,h=768".format(vm.framebuffer))
        else:
            params.append("-s 29:0,fbuf,wait,tcp=127.0.0.1:{},w=1024,h=768".format(vm.framebuffer))
    if vm.bios:
        bios = BhyveVm.bios_type_to_path(vm.bios)
        params.append('-l bootrom,{}'.format(bios))
    if vm.tap:
        params.append('-s 2:0,virtio-net,{}'.format(vm.tap))
    if vm.console:
        params.append('-l com1,{}'.format(vm.console))

    drive_iterator = itertools.chain(zip(itertools.repeat(DiskType.VIRTIO_DISK), vm.disks), zip(itertools.repeat(DiskType.ISO), vm.isos))
    for drive_slot, item in enumerate(drive_iterator, DISK_START):
        drive_type, drive_path = item
        if drive_type == DiskType.VIRTIO_DISK:
            params.append('-s {drive_slot}:0,virtio-blk,{drive_path}'.format(drive_slot=drive_slot, drive_path=drive_path))
        elif drive_type == DiskType.ISO:
            params.append('-s {drive_slot}:0,ahci-cd,{drive_path}'.format(drive_slot=drive_slot, drive_path=drive_path))
        elif drive_type == DiskType.AHCI_DISK:
            params.append('-s {drive_slot}:0,ahci-hd,{drive_path}'.format(drive_slot=drive_slot, drive_path=drive_path))

    print(params)
    command = "bhyve {params} {name}".format(
        params = ' '.join(params),
        name = vm.name
    )
    return command

async def run_vm(vm):
    command = create_command(vm)
    await fire_command(command)