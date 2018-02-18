import asyncio
import asyncio.subprocess
import shlex
from .await_process import exec_command

async def load_image(image, memory, name, console):
    command = "bhyveload -m {memory} -c {console} -d {image} -e autoboot_delay=-1 {name}".format(
        memory=memory,
        console=console,
        image=image,
        name=name
    )
    (out, err) = await exec_command(command)
    return (out, err)

