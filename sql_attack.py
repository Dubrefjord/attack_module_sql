import subprocess
import os
import sys
import json

def filter_sqlmap_output(output):
  return output


json_data = sys.argv[1]
node_data = json.loads(json_data)

sqlmap_command = ["sqlmap"]
sqlmap_command.append("--batch") #Can replace with --answers [list of answers] if batch misses vulns.
sqlmap_command.append("-v")
sqlmap_command.append("1")
if "url" in node_data:
  sqlmap_command.append("-u")
  sqlmap_command.append(node_data["url"])
if "cookies" in node_data:
  sqlmap_command.append("--cookie")
  sqlmap_command.append("&".join(node_data["cookies"]))
if "data" in node_data:
  sqlmap_command.append("--data")
  sqlmap_command.append("&".join(node_data["data"]))
if "parameters" in node_data and node_data["parameters"] != "":
  sqlmap_command.append("-p")
  sqlmap_command.append(",".join(node_data["parameters"]))
if "method" in node_data:
  sqlmap_command.append("--forms")
  #sqlmap_command.append("--method")
  #sqlmap_command.append(node_data["method"])

attack = subprocess.run(sqlmap_command, capture_output=True, text=True)

if attack.returncode==0:
  print(attack.args)
  print(filter_sqlmap_output(attack.stdout))
else:
  print("ERROR OCCURED IN SQLMAP FOR NODE")
  print(attack.args)
  print(attack.stdout)
