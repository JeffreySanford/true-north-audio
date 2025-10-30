import psutil
import platform

def check_resources(min_ram_gb=2, min_cpu_ghz=2):
    ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    cpu_freq = psutil.cpu_freq().max / 1000 if psutil.cpu_freq() else 0
    warnings = []
    if ram_gb < min_ram_gb:
        warnings.append(f"Warning: RAM ({ram_gb:.1f} GB) below recommended {min_ram_gb} GB.")
    if cpu_freq < min_cpu_ghz:
        warnings.append(f"Warning: CPU ({cpu_freq:.1f} GHz) below recommended {min_cpu_ghz} GHz.")
    if platform.system() == 'Windows' and not psutil.WINDOWS:
        warnings.append("Warning: Windows platform detected, some features may be limited.")
    for w in warnings:
        print(w)
    return warnings
