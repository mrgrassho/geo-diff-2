#!/usr/bin/env python
# -*- enconding: utf-8 -*-

import docker
from docker.types import ServiceMode
from ast import literal_eval

env_to_dict = lambda l : {i.split("=")[0]: i.split("=")[1] for i in l}
dict_to_env = lambda d : [ '='.join([k, v]) for k, v in d.items()]        

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


    def get_container(self, container_id):
        try:
            return self.native_docker_client.containers.get(container_id)
        except docker.errors.NotFound:
            return None


    def get_service_env(self, service_name):
        service = self._get_service(service_name)
        return env_to_dict(service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Env']) if service is not None else None


    def update_service_env_add(self, service_name, new_env):
        service = self._get_service(service_name)
        old_env = self.get_service_env(service_name)
        if all([old_env, service]): # if both values are not None
            for k, v in new_env.items():
                if (k in old_env and v is not None):
                    old_env[k] = str(literal_eval(old_env[k]) + v)
            env_list = dict_to_env(old_env)
            service.update(env=env_list)


    def get_containers(self, service_name):
        containers = []
        for container in self.native_docker_client.containers.list():
            if container.attrs["Config"]["Labels"]["com.docker.swarm.service.name"] == service_name:
                containers.append(container.attrs["Config"]["Hostname"])
        return containers
