import re
import subprocess
from rich.console import Console

console = Console()

console.rule('[bold red]All wifi & password')


netsh_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True).stdout.decode()
profile_names = (re.findall('All User Profile     : (.*)\r', netsh_output))

wifi_list = []
if len(profile_names) > 0:
    for profile_name in profile_names:
        profile_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles', profile_name],
                                        capture_output=True).stdout.decode()
        wifi_info = {}
        if re.search('Security key           : Absent', profile_output):
            continue
        else:
            wifi_info['SSID'] = profile_name
            password_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles', profile_name, 'key=clear'],
                                             capture_output=True).stdout.decode()
            password = (re.search('Key Content            : (.*)\r', password_output))
            if password == None:
                wifi_info['password'] = None
            else:
                wifi_info['password'] = password[1]
            wifi_list.append(wifi_info)

for wifi in wifi_list:
    console.print(wifi['SSID'], ':', wifi['password'], justify='center')

inn = input('inter "exit" to end >>> ')
if inn == 'exit':
    pass