#!/usr/bin/env python3

import json
import subprocess
from os.path import expanduser
from getpass import getuser
from os import getenv

# If your mySociety username is different to your local username set it in the
# MYSOCIETY_USERNAME environment variable before running this script
username = getenv("MYSOCIETY_USERNAME", getuser())
jumpbox = getenv("MYSOCIETY_JUMPBOX", "srv-2ssio.srv.mysociety.org")

j = subprocess.run(["ssh", jumpbox, "cat" ,"/data/vhosts.json"], capture_output=True)
j = json.loads(j.stdout)

def host_out(host, server):
    return f"""Host {host}
  Hostname {server}
  User {username}
  IdentityFile ~/.ssh/id_rsa
  ForwardAgent yes
  ProxyJump {jumpbox}
"""

def process():
    with open(expanduser("~/.ssh/mysociety_hosts"), "w") as f:
        for v, data in j['vhosts'].items():
            ct = data.get('crontab')
            servers = data['servers']
            if ct and ct not in (1, 'only-one'):
                servers = [ct]
            for i, server in enumerate(servers, 1):
                print(host_out(f"{v}-app{i if i > 1 else ''}", server), file=f)
            if 'databases' in data:
                database = data['databases'][0]
                print(host_out(f"{v}-db", j['databases'][database]['host']), file=f)

process()
print("Done! Make sure you add the following to ~/.ssh/config:\n\nInclude mysociety_hosts")
