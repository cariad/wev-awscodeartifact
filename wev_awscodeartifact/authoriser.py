from typing import Any, Dict, Optional

from boto3.session import Session
from botocore.config import Config


class Authoriser:
    """
    Requests an authorisation token from an AWS CodeArtifact domain.

    Arguments:
        domain (Domain): AWS CodeArtifact domain.

        profile (str):   Optional AWS named profile to use. Will be used preferentially
                         over any AWS named profile described in `domain`.
    """

    def __init__(
        self,
        domain: str,
        account: Optional[str] = None,
        profile: Optional[str] = None,
        region: Optional[str] = None,
    ) -> None:
        self.account = account
        self.domain = domain
        self.profile = profile
        self.region = region

    @property
    def client_kwargs(self) -> Dict[str, Any]:
        """ Gets the keyword arguments to pass to the boto3 client. """
        args: Dict[str, Any] = {
            "config": Config(
                connect_timeout=3,
                read_timeout=20,
                retries={"max_attempts": 20},
            )
        }
        if self.region:
            args.update({"region_name": self.region})
        return args

    @property
    def token(self) -> str:
        """ Gets an authorisation token from the prescribed AWS CodeArtifact domain. """
        session = Session(**self.session_kwargs)
        codeart = session.client("codeartifact", **self.client_kwargs)
        response = codeart.get_authorization_token(**self.token_kwargs)
        return str(response["authorizationToken"])

    @property
    def session_kwargs(self) -> Dict[str, Any]:
        """ Gets the keyword arguments to pass to the boto3 session. """
        args: Dict[str, Any] = {}
        if self.profile:
            args.update({"profile_name": self.profile})
        return args

    @property
    def token_kwargs(self) -> Dict[str, Any]:
        """
        Gets the keyword arguments to pass to the boto3 `get_authorization_token`
        function.
        """
        args: Dict[str, Any] = {"domain": self.domain}
        if self.account:
            args.update({"domainOwner": self.account})
        return args
