import asyncio
import shutil
import psutil
from typing import Dict, Union

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    
    time_list.reverse()
    ping_time += ":".join(time_list)
    
    return ping_time

def bytes_to_mb(bytes_val):
    return round(bytes_val / 1024 / 1024, 2)

def get_size(bytes_val):
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if bytes_val == 0:
        return "0 Byte"
    i = 0
    while bytes_val >= 1024 and i < len(sizes) - 1:
        bytes_val /= 1024.0
        i += 1
    return f"{bytes_val:.2f} {sizes[i]}"

async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    
    stats = {
        "uptime": get_readable_time((bot_uptime)),
        "cpu": cpu,
        "ram": mem,
        "disk": disk,
        "process_ram": round(process.memory_info()[0] / 1024 / 1024 / 1024, 3),
        "process_cpu": process.cpu_percent() / psutil.cpu_count()
    }
    return stats

def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 60,
        )
        if d > 0:
            return f"{d}d, {h}h, {m}m, {s}s"
        elif h > 0:
            return f"{h}h, {m}m, {s}s"
        elif m > 0:
            return f"{m}m, {s}s"
        elif s > 0:
            return f"{s}s"
    return "-"

def speed_converter(size):
    if not size:
        return ""
    power = 2**10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))