import logging

from .authelia import AutheliaDeployer
from .blast import BlastDeployer
from .dockercompose import DockerComposeDeployer
from .download import DownloadDeployer
from .elasticsearch import ElasticsearchDeployer
from .genoboo import GenobooDeployer
from .genomehomepage import GenomeHomepageDeployer
from .jbrowse import JbrowseDeployer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class Deployers():
    def __init__(self, config):

        self.config = config
        self.deployers = {}

        self.deployers[DockerComposeDeployer.service_name] = DockerComposeDeployer
        self.deployers[GenomeHomepageDeployer.service_name] = GenomeHomepageDeployer

        self.deployers[AutheliaDeployer.service_name] = AutheliaDeployer
        self.deployers[BlastDeployer.service_name] = BlastDeployer
        self.deployers[DownloadDeployer.service_name] = DownloadDeployer
        self.deployers[ElasticsearchDeployer.service_name] = ElasticsearchDeployer
        self.deployers[JbrowseDeployer.service_name] = JbrowseDeployer
        self.deployers[GenobooDeployer.service_name] = GenobooDeployer

    def has(self, service):

        return service in self.deployers

    def get(self, service, server, entity):

        if service in self.deployers:
            return self.deployers[service](self.config, server, entity)

        raise RuntimeError('Could not find deployer for service "%s"' % service)
