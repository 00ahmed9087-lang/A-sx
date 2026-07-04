import os
import xml.etree.ElementTree as ET
import json
import subprocess
print("[$ *] Starting Masscan...")
ii = "masscan 0.0.0.0/0 -p1-3000 --rate 100000 --excludefile exclude.txt -oX open_ports.xml"
os.system(ii)
print("[$ *] Parsing XML data...")
known_services = {
    80: "http", 443: "tls", 22: "ssh", 21: "ftp", 25: "smtp", 
    23: "telnet", 53: "dns", 110: "pop3", 143: "imap", 3306: "mysql", 
    5432: "postgres", 6379: "redis", 8080: "http", 8443: "tls"
}
try:
    with open("targets.json", "w") as f_out:
        for event, elem in ET.iterparse("open_ports.xml", events=("end",)):
            if elem.tag == "host":
                ip = ""
                address = elem.find("address")
                if address is not None:
                    ip = address.get("addr")
                
                ports = elem.find("ports")
                if ports is not None and ip:
                    for port_elem in ports.findall("port"):
                        port = int(port_elem.get("portid"))
                        service = known_services.get(port, "http")
                        data = {"ip": ip, "port": port, "service": service}
                        
                        f_out.write(json.dumps(data) + "\n")
                elem.clear()
    print("[$ +] XML parsed successfully into targets.json")
except Exception as e:
    print(f"[-] Error during parsing: {e}")

print("[$*] Starting ZGrab2...")
zgrab_cmd = "zgrab2 multiple --input-file=targets.json --senders=1000 --output-file=vs-.txt"
os.system(zgrab_cmd)

print("[$ +] Done! Results saved in vs-.txt")
