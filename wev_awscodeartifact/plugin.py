from datetime import datetime, timedelta
from logging import Logger
from typing import List, Optional

from wev.sdk import PluginBase, Resolution, ResolutionSupport
from wev.sdk.exceptions import MissingConfigurationError

from wev_awscodeartifact.authoriser import Authoriser
from wev_awscodeartifact.version import get_version


class Plugin(PluginBase):
    """ `wev-awscodeartifact` plugin. """

    @property
    def account(self) -> Optional[str]:
        return self.get("account", None)

    @property
    def domain(self) -> str:
        if domain := self.get("domain", None):
            return str(domain)
        raise MissingConfigurationError(
            key="domain",
            explanation="The domain cannot be discovered automatically.",
        )

    @property
    def duration(self) -> int:
        return self.get("duration", 12 * 60 * 60)  # 12 hours

    @property
    def region(self) -> Optional[str]:
        return self.get("region", None)

    @property
    def profile(self) -> Optional[str]:
        return self.get("profile", None)

    @property
    def cache_duration(self) -> int:
        """ Gets the cache duration. """
        return int(self.get("cache_duration", 30))

    def explain(self, logger: Logger) -> List[str]:
        wip = "An authorisation token will be requested from the "
        wip = f'{wip}"{self.domain}" CodeArtifact domain'

        if self.account:
            wip = f'{wip} in account "{self.account}"'

        if self.region:
            wip = f"{wip} in {self.region}"

        if self.profile:
            wip = f'{wip} with your "{self.profile}" profile'

        wip = f"{wip}."
        return [wip]

    def resolve(self, support: ResolutionSupport) -> Resolution:
        return Resolution.make(
            value=Authoriser(
                domain=self.domain,
                account=self.account,
                profile=self.profile,
                region=self.region,
            ).token,
            expires_at=datetime.now() + timedelta(seconds=self.duration),
        )

    @property
    def version(self) -> str:
        """ Gets the plugin's version. """
        return get_version()
