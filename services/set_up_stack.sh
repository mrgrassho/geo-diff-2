#!/usr/bin/env bash

if [[ $# == 2 ]]; then
    find . -name ".env.example" | xargs -i echo cp {} {} | sed -e "s/.example$//" | xargs -i bash -c {}
    docker stack rm $2
    docker-compose -f $1 build
    docker stack deploy --compose-file $1 $2
else
  echo " Usage: setup.sh DOCKER_COMPOSE_FILE STACK_NAME"
  echo ""
  echo " Example:"
  echo "     setup.sh docker-compose-work.yml geo-diff-work"
fi
