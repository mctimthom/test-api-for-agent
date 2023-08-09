# /srv/salt/sync_actors_state.sls

sync_actors_state:
  module.run:
    - name: sync_actors.sync_actors