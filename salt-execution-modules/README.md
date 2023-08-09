python scripts go under /srv/salt/\_modules

sls files go under /srv/salt/

sync modules with sudo salt '\*' saltutil.sync_modules
run modules with sudo salt '\*' state.apply \<state name\>
