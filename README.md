This script parses the public vhosts.json file from srv-2ssio.srv.mysociety.org
and creates an SSH config file (~/.ssh/mysociety_vhosts) to make server
connecting easier. It will add vhost-app and vhost-db entries for every vhost in
the data.

If your mySociety username is different to your local username set it in the
MYSOCIETY_USERNAME environment variable before running this script.

Add "Include mysociety_vhosts" to your ~/.ssh/config to include this new file.

To SSH to the app server for e.g. www.fixmystreet.com, you can then run
`ssh www.fixmystreet.com-app`. Similarly, for the DB server for that vhost
`ssh www.fixmystreet.com-db`. For vhosts with more than one app server, you could
use `...-app2`, `...-app3` etc.
