from logging import Logger
from typing import Optional

from pytest import mark

from wev_awscodeartifact.plugin import Plugin


@mark.parametrize(
    "domain, account, region, profile, expect",
    [
        (
            "foo",
            None,
            None,
            None,
            '"foo" CodeArtifact domain.',
        ),
        (
            "foo",
            "00",
            None,
            None,
            '"foo" CodeArtifact domain in account "00".',
        ),
        (
            "foo",
            "00",
            "eu",
            "ow",
            '"foo" CodeArtifact domain in account "00" in eu with your "ow" profile.',
        ),
    ],
)
def test_explain(
    domain: str,
    account: Optional[str],
    region: Optional[str],
    profile: Optional[str],
    expect: str,
    logger: Logger,
) -> None:
    head = "An authorisation token will be requested from the "
    plugin = Plugin({"domain": domain})
    if account:
        plugin["account"] = account
    if region:
        plugin["region"] = region
    if profile:
        plugin["profile"] = profile
    assert plugin.explain(logger=logger)[0] == head + expect
