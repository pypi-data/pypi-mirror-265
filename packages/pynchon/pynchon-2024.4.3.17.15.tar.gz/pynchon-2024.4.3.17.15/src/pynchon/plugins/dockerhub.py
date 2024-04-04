""" pynchon.plugins.mermaid
"""

from fleks import cli, tagging  # noqa

from pynchon import abcs, events, models  # noqa
from pynchon.util import files, lme, typing  # noqa

LOGGER = lme.get_logger(__name__)


class Dockerhub(models.Planner):
    """Dockerhub Plugin"""

    class config_class(abcs.Config):
        config_key: typing.ClassVar[str] = "dockerhub"
        org_name: typing.StringMaybe = typing.Field(default=None, help="")
        repo_name: typing.StringMaybe = typing.Field(default=None, help="")

        @property
        def org_url(self) -> str:
            return self.org_name and f"https://hub.docker.com/r/{self.org_name}"

        @property
        def repo_url(self) -> str:
            return (
                self.repo_name and self.org_url and f"{self.org_url}/{self.repo_name}"
            )

    name = "dockerhub"
    cli_name = "dockerhub"

    def open(self):
        import webbrowser

        url = self.config.repo_url or self.config.org_url
        # assert url,err
        webbrowser.open(url)
