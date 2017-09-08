import time
import pip

try:
    import psutil
except ImportError:
    pip.main(['install', 'psutil'])
    import psutil

try:
    memory = psutil.virtual_memory().percent
except Exception as E:
    memory = None

try:
    cpu = psutil.cpu_percent(interval=1, percpu=False)
except Exception as E:
    cpu = None

try:
    uptime = time.time() - psutil.boot_time()
except Exception as E:
    uptime = None

results = (memory, cpu, uptime)

print(results)
