#!/bin/bash

rabbitmqctl add_user geoadmin geoadmin
rabbitmqctl add_vhost geovhost
rabbitmqctl set_permissions -p geovhost geoadmin ".*" ".*" ".*"
# rabbitmq-server restart