#!/usr/bin/env python
# -*- enconding: utf-8 -*-

import docker
from docker.types import ServiceMode


class DockerAPIClient(object):

    def __init__(self, native_docker_client=None):
        self.native_docker_client = native_docker_client or docker.from_env()


    def _get_service(self, service_name):
        services = self.native_docker_client.services.list(filters=dict(name=service_name))
        return services[0] if services is not None and len(services) > 0 else None


    def get_service_replica_count(self, service_name):
        service = self._get_service(service_name)
        return service.attrs['Spec']['Mode']['Replicated']['Replicas'] if service is not None else -1


    def scale_service(self, service_name, replica_count):
        service = self._get_service(service_name)
        service.update(mode=ServiceMode("replicated", replicas=replica_count))


    def get_containers(self, service_name):
        containers = []
        for container in self.native_docker_client.containers.list():
            if container.attrs["HostConfig"]["Config"]["Labels"]["com.docker.swarm.service.name"] == service_name:
                containers.push(container.attrs["HostConfig"]["Config"]["Hostname"])
        return containers
