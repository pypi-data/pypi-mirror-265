import logging
import os

import gitlab

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class MR_Bot():

    def __init__(self):
        self.ready = False

        needed_env_vars = [
            'CI_MERGE_REQUEST_IID',
            'CI_PROJECT_ID',
            'CI_SERVER_URL',
            'GITLAB_BOT_TOKEN',
            'CI_MERGE_REQUEST_PROJECT_URL'
        ]

        if not all(item in os.environ for item in needed_env_vars):
            log.info("Not in a GitLab MR or band env vars, cannot send message to bot")
            return

        gl_url = os.getenv('CI_SERVER_URL')
        gl = gitlab.Gitlab(url=gl_url, private_token=os.getenv('GITLAB_BOT_TOKEN'))

        project = gl.projects.get(os.getenv('CI_PROJECT_ID'), lazy=True)
        self.mr = project.mergerequests.get(os.getenv('CI_MERGE_REQUEST_IID'), lazy=True)
        self.ready = True

    def write_message(self, message):
        if self.ready:
            self.mr.notes.create({'body': message})
