import asyncio
import asyncio.subprocess
import shlex

async def get_status(name):
    process = await asyncio.create_subprocess_shell('bhyvectl --vm={} --get-all'.format(shlex.quote(name)), stdout=asyncio.subprocess.PIPE)
    line = await process.stdout.read()
    await process.wait()
    return line.decode('utf8')

async def poweroff(name):
    process = await asyncio.create_subprocess_shell('bhyvectl --vm={} --force-poweroff'.format(shlex.quote(name)), stdout=asyncio.subprocess.PIPE)
    line = await process.stdout.read()
    await process.wait()
    return line.decode('utf8')

async def destroy(name):
    process = await asyncio.create_subprocess_shell('bhyvectl --vm={} --destroy'.format(shlex.quote(name)), stdout=asyncio.subprocess.PIPE)
    line = await process.stdout.read()
    await process.wait()
    return line.decode('utf8')
