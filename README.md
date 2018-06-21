# aiobhyve-web
*(_NOTE_: This a project that I used to learn Python 3's asyncio, you REALLY do not want to use it, there are way better projects for this out there)*

This is a basic web interface for FreeBSD's bhyve virtual machines.
It currently supports:
* loading VMs with
  * bhyveload
  * grub-bhyve (command line mode, menus are not yet supported)
  * directly through bhyve
* common settings, such as VNC, boot ROMs, serial consoles, tap devices
* listing DHCP leashes from the locally running dnsmasq

## Disks
The disk images can either be:
* raw *.img files in `/usr/vms`
* zvols (preferably in `dev` `volmode` if you don't want each partition as a separate file)
* isos in `/usr/iso`
There paths are currently hardcoded.

## Caveats:
* tap devices have to be created separately
* have to be ran as root

## TODO
* basically sit down and finish the damn thing
