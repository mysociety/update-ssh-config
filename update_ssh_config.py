#!/usr/bin/env python3

import json
import subprocess
from os.path import expanduser
from getpass import getuser
from os import getenv

# If your mySociety username is different to your local username set it in the
# MYSOCIETY_USERNAME environment variable before running this script
username = getenv("MYSOCIETY_USERNAME", getuser())

j = subprocess.run(["ssh", f"{username}@raven.ukcod.org.uk", "cat" ,"/data/vhosts.json"], capture_output=True)
j = json.loads(j.stdout)

def host_out(host, server):
    return f"""Host {host}
  Hostname {server}
  User {username}
  IdentityFile ~/.ssh/id_rsa
  ForwardAgent yes
  ProxyJump raven.ukcod.org.uk
"""

def process():
    with open(expanduser("~/.ssh/mysociety_hosts"), "w") as f:
        for v, data in j['vhosts'].items():
            ct = data.get('crontab')
            server = data['servers'][0]
            if ct and ct not in (1, 'only-one'):
                server = ct
            print(host_out(f"{v}-app", server), file=f)
            if 'databases' in data:
                database = data['databases'][0]
                print(host_out(f"{v}-db", j['databases'][database]['host']), file=f)

process()
print("Done! Make sure you add the following to ~/.ssh/config:\n\nInclude mysociety_hosts")
