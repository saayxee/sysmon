import socket
import os
import time
import platform
import psutil
from termcolor import colored
import ipaddress
from datetime import datetime
from screeninfo import get_monitors


def get_system_info():
    # general variables
    os_info = platform.uname()
    cpu_freq = psutil.cpu_freq()
    unavailable = colored("Unavailable", "red")

    # system information variables
    current_datetime = time.ctime() if time.ctime() else unavailable
    current_working_directory = os.getcwd() if os.getcwd() else unavailable
    python_version = platform.python_version() if platform.python_version() else unavailable
    operating_system = os_info.system if os_info.system else unavailable
    operating_system_version = os_info.version if os_info.version else unavailable
    internet_protocol_address = socket.gethostbyname(socket.gethostname()) if os_info.system else unavailable
    internet_protocol_address_version = "IPv" + str(ipaddress.ip_address(socket.gethostbyname(socket.gethostname())).version) if os_info.system else unavailable
    node = os_info.node if os_info.node else unavailable
    release = os_info.release if os_info.release else unavailable
    machine = os_info.machine if os_info.machine else unavailable
    processor = os_info.processor if os_info.processor else unavailable
    architecture = platform.architecture()[0] if platform.architecture()[0] else unavailable
    physical_cores = psutil.cpu_count(logical=False) if psutil.cpu_count(logical=False) else unavailable
    logical_cores = psutil.cpu_count(logical=True) if psutil.cpu_count(logical=True) else unavailable
    cpu_frequency = f"{cpu_freq.current:.2f}" if cpu_freq else unavailable
    total_random_access_memory = f"{psutil.virtual_memory().total / (1024 ** 3):.2f}" if psutil.virtual_memory() else unavailable
    available_random_access_memory = f"{psutil.virtual_memory().available / (1024 ** 3):.2f}" if psutil.virtual_memory() else unavailable    
    monitor_count = len(get_monitors())
    system_uptime = time.strftime("%H Hours, %M minutes, %S seconds", time.gmtime(time.time() - psutil.boot_time()))
    processes = len(list(psutil.process_iter()))




    system_info = {
        "  [#] Datetime": current_datetime,
        "  [#] Python Version": python_version,
        "  [#] Monitors": monitor_count,
        "  [#] Current Working Directory (CWD)": current_working_directory,
        "  [#] Processes Running": processes,
        "  [#] Operating System (OS)": operating_system,
        "  [#] OS Version": operating_system_version,
        "  [#] OS Release": release,
        "  [#] OS Architecture": architecture,
        "  [#] System Uptime": system_uptime,
        "  [#] Machine": machine,
        "  [#] Central Processing Unit (CPU)": processor,
        "  [#] CPU Frequency": cpu_frequency + "MHz",
        "  [#] Physical Cores": physical_cores,
        "  [#] Logical Cores": logical_cores,
        "  [#] Hostname/Node": node,
        "  [#] Internet Protocol (IP) Address": internet_protocol_address,
        "  [#] IP Address Version": internet_protocol_address_version,
        "  [#] Memory Access Control (MAC) Addresses": "[MAC_ADDRESSES]",
        "  [#] Storage": "[STORAGE]",
        "  [#] Users": "[USERS]",
        "  [#] Total Memory": total_random_access_memory + "GB",
        "  [#] Available Memory": available_random_access_memory + "GB",
    }

    return system_info

def display_system_info(system_info):
    for key, value in system_info.items():
        if (value == "[MAC_ADDRESSES]"):    
            print(key + ": ")
            network_interfaces = psutil.net_if_addrs()

            for interface, addresses in network_interfaces.items():
                for address in addresses:
                    if address.family == psutil.AF_LINK:
                        print(f"  ==[#] MAC Address - {interface}: {colored(address.address, "light_green")}")
        elif (value == "[USERS]"):
            print(key + ": ")
            users = psutil.users()
            for user in users:
                print(f"  ==[#] {user.name} (Last Login: {datetime.fromtimestamp(user.started).strftime(f"%H:%M:%S, %d/%m/%Y")})")
        elif (value == "[STORAGE]"):
            print(key + ": ")
            # Get all mounted disk partitions
            partitions = psutil.disk_partitions()

            # Iterate over each partition to get the file system type
            for partition in partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                total_disk = usage.total
                used_disk = usage.used
                free_disk = usage.free
                print(f"  ==[#] Drive {partition.device}")
                print(f"  ====[#] Mountpoint: {colored(partition.mountpoint, "light_green")}")
                print(f"  ====[#] File System Type: {colored(partition.fstype, "light_green")}")
                print(f"  ====[#] Total Disk Space: {total_disk / (1024 ** 3):.2f}GB")
                print(f"  ====[#] Used Disk Space: {used_disk / (1024 ** 3):.2f}GB")
                print(f"  ====[#] Free Disk Space: {free_disk / (1024 ** 3):.2f}GB")
        else:
          print(f"{key}: {colored(value, "light_green")}")

def main():
    print(colored(fr""" 
  
   _____ __ __  _____ ___ ___   ___   ____  
  / ___/|  |  |/ ___/|   |   | /   \ |    \ 
 (   \_ |  |  (   \_ | _   _ ||     ||  _  |
  \__  ||  ~  |\__  ||  \_/  ||  O  ||  |  |
  /  \ ||___, |/  \ ||   |   ||     ||  |  |
  \    ||     |\    ||   |   ||     ||  |  |
   \___||____/  \___||___|___| \___/ |__|__|

    {colored("")}
  Helping you get familiar with your system.
  {colored("https://github.com/saayxee/sysmon", "blue")}

  ------------------------------------------                                        """, "light_blue"))
    print("")
    system_info = get_system_info()
    display_system_info(system_info)
    print("")

if __name__ == "__main__":
    main()


