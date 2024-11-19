from subnet import subnet
from scan import scan_subnet
from yaml import CLoader as Loader
import yaml
import argparse
from rich.console import Console
from rich.table import Table

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='NetworkScan',description='Small network scan')
    parser.add_argument("--config_file",help="YAML File containing the network config")
    parser.add_argument("-op","--only_up",help="Get only up hosts",action='store_true')
    args = parser.parse_args()
    try:
        with open(args.config_file) as yaml_file:
            yaml_data = yaml.load(yaml_file,Loader=Loader)
    except TypeError:
        raise FileNotFoundError("Missing file")
    
    for subnets in yaml_data["subnet"]:
        print(f'Starting the scan of {yaml_data["subnet"][subnets]["ip"]}')
        subnet_scan = subnet(yaml_data["subnet"][subnets]["ip"],yaml_data["subnet"][subnets]["cidr"])
        all_ips = subnet_scan.get_all_possible_hosts()
        results = scan_subnet(all_ips)
    
        console = Console()
        table = Table(show_header = True,header_style="bold magenta")
        table.add_column("Host")
        table.add_column("Status")
        table.add_column("MAC Address")
        table.add_column("Vendor")
        up_hosts=0
        down_hosts=0
        for result in results:
            add_value = lambda:table.add_row(result,str(results[result][0]),str(results[result][1]),str(results[result][2]))
            if(args.only_up and results[result][0]==True):
                add_value()
            elif(args.only_up and results[result][0]==False):
                continue
            else:
                add_value()
            if (results[result][0]==True):
                up_hosts+=1
            else:
                down_hosts+=1
                
        table.add_row("Number of Hosts Up:"," ",str(up_hosts))
        table.add_row("Number of Hosts Down:"," ",str(down_hosts))

        console.print(table)   
