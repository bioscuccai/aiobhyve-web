import asyncio
import asyncio.subprocess

import tempfile
from contextlib import contextmanager
from pathlib import Path
import shlex

@contextmanager
def create_mapping(disks, isos):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        for index, path in enumerate(isos):
            f.write("(cd{}) {}\n".format(index, path))
        for index, path in enumerate(disks):
            f.write("(hd{}) {}\n".format(index, path))
        f.flush()
        yield f

async def run_netbsd(disks, isos):
    pass

async def run_linux(disks, isos):
    pass

async def run_openbsd(disks, isos):
    pass

async def run_command(disks, isos, command, memory, name, root_device, debug=False, preset=None):
    command_w_boot = command + "\nboot\n"
    grub_command = ""
    with create_mapping(disks, isos) as mapping_file:
        grub_command = "bash -c \"echo -e {escaped_command} | grub-bhyve -M {memory} -r {root_device} -m {mapping} {name}\"".format(
            escaped_command=shlex.quote(command_w_boot).replace("\n", r"\n"),
            root_device=root_device,
            memory=memory,
            mapping=mapping_file.name,
            name=name
        )
        print(mapping_file.name)
        print(Path(mapping_file.name).read_text())
        print(grub_command)

        if not debug:
            process = await asyncio.create_subprocess_shell(grub_command)
            # process.stdin.write((command + '\n').encode('utf8'))
            # process.stdin.write(b'boot\n')
        return grub_command
