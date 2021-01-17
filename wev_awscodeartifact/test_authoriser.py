from typing import Any, Dict, Optional

from mock import Mock, patch
from pytest import mark

from wev_awscodeartifact.authoriser import Authoriser


@mark.parametrize(
    "region, expect",
    [
        (None, {}),
        ("eu-west-2", {"region_name": "eu-west-2"}),
    ],
)
def test_client_kwargs(region: Optional[str], expect: Dict[str, Any]) -> None:
    kwargs = Authoriser(domain="foo", region=region).client_kwargs
    # kwargs["config"] is a boto object that we can't easily describe in our
    # expectations above. We'll test it "manually" here, then remove it from the
    # response before asserting it matches our expectation.
    assert kwargs["config"].connect_timeout == 3
    assert kwargs["config"].read_timeout == 20
    assert kwargs["config"].retries == {"max_attempts": 20}
    del kwargs["config"]
    assert kwargs == expect


@mark.parametrize(
    "profile, expect",
    [
        (None, {}),
        ("foo", {"profile_name": "foo"}),
    ],
)
def test_session_kwargs(profile: Optional[str], expect: Dict[str, Any]) -> None:
    assert Authoriser(domain="bar", profile=profile).session_kwargs == expect


@patch("wev_awscodeartifact.authoriser.Session")
def test_token(session_maker: Mock) -> None:
    session = Mock()
    session_maker.return_value = session
    client = Mock()
    client.get_authorization_token = Mock(return_value={"authorizationToken": "foo"})
    session.client = Mock(return_value=client)
    assert Authoriser(domain="bar").token == "foo"


@mark.parametrize(
    "domain, account, expect",
    [
        ("foo", None, {"domain": "foo"}),
        ("foo", "0", {"domain": "foo", "domainOwner": "0"}),
    ],
)
def test_token_kwargs(
    domain: str,
    account: Optional[str],
    expect: Dict[str, Any],
) -> None:
    assert Authoriser(account=account, domain=domain).token_kwargs == expect
