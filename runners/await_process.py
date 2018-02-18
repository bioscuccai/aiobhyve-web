import asyncio
import asyncio.subprocess

async def exec_command(command):
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    line = await process.stdout.read()
    err = await process.stderr.read()
    await process.wait()
    return (line.decode('utf8'), err.decode('utf8'))

async def fire_command(command):
    process = await asyncio.create_subprocess_shell(command)