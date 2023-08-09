# /srv/salt/get_actors_state.sls

get_actors_state:
  module.run:
    - name: get_actors.get_actors