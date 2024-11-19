from pythonping import ping
from getmac import get_mac_address
from rich.progress import track



def scan_subnet(host_list: list):
    ip_scan_results = {}
    for ip in track(host_list):
        ping_status=ping(ip.compressed, count=1)
        ping_result = ping_status.success(option=3)
        if ping_result==True:
            mac=get_mac_address(ip=ip.compressed)
            ip_scan_results[ip.compressed] = [ping_result,mac,mac_oui_to_brand(mac)]
        else:
            ip_scan_results[ip.compressed] = [ping_result,"NA","NA"]
    return ip_scan_results


def mac_oui_to_brand(mac):
    oui = mac[0:8]
    with open(".\\data\\mac-vendors-export.csv", encoding="utf8") as csv_file:
        for csv_data in csv_file:
            if csv_data.split(",")[0][0:8] == oui.upper():
                return csv_data.split(",")[1]
    
        


