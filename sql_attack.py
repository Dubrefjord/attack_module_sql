import subprocess
import os
import sys
import json


def filter_sqlmap_output(output):
    save_data = False
    filtered_output = ""
    f = open("debugfile.txt", "a")
    for line in output.splitlines():
        f.write(line+"\n")
        if line.find("---") != -1:
            save_data = not save_data
        if save_data:
            filtered_output = filtered_output + line + "\n"
    return filtered_output


json_data = sys.argv[1]
node_data = json.loads(json_data)

sqlmap_command = ["sqlmap"]
sqlmap_command.append('--answers=keep testing=Y')

# TODO ADD level==5 and risk==3 ,  REMOVE --forms.


#sqlmap_command.append('testing=Y\'')
sqlmap_command.append("--batch") #Can replace with --answers [list of answers] if batch misses vulns. (Attack more params if one is found)
sqlmap_command.append("-v")
sqlmap_command.append("0")
sqlmap_command.append("--flush-session")
#sqlmap_command.append("--risk=3")
#sqlmap_command.append("--level=5")
if "url" in node_data:
  sqlmap_command.append("-u")
  sqlmap_command.append(node_data["url"])
if "cookies" in node_data:
  sqlmap_command.append("--cookie")
  sqlmap_command.append(node_data["cookies"])
if "data" in node_data and node_data["method"] == "post":
  sqlmap_command.append("--data")
  sqlmap_command.append(node_data["data"])
if "data" in node_data and node_data["method"] == "get":
  sqlmap_command.append("--forms")
if "parameters" in node_data and node_data["parameters"] != "":
  sqlmap_command.append("-p")
  sqlmap_command.append(node_data["parameters"])



attack = subprocess.run(sqlmap_command, capture_output=True, text=True)

if attack.returncode==0:
  filtered_output = filter_sqlmap_output(attack.stdout)
  print("Node: "+json_data)

  if len(filtered_output) > 0:
      print("SQLmap command: "+str(attack.args))
      print(filtered_output)
  if len(filtered_output) == 0:
      print("no vulnerabilities found at node.")
if attack.returncode !=  0:
  print("ERROR OCCURED IN SQLMAP FOR NODE")
  print(attack.args)
  print(attack.stdout)
