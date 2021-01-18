# wev-awscodeartifact: A `wev` plugin to support Amazon Web Services CodeArtifact authorisation on the command line

[![codecov](https://codecov.io/gh/cariad/wev-awscodeartifact/branch/main/graph/badge.svg?token=D48XKZJXJ7)](https://codecov.io/gh/cariad/wev-awscodeartifact)

`wev-awscodeartifact` is a plugin for [wev](https://github.com/cariad/wev) to generate Amazon Web Services CodeArtifact authorisation tokens.

## Example

Say your `Pipfile` is configured to pull packages from a private Amazon Web Services CodeArtifact repository. The file expects `$CODEARTIFACT_AUTH_TOKEN` to be set to your authorisation token.

```text
[[source]]
name = "private"
url = "https://aws:$CODEARTIFACT_AUTH_TOKEN@wev-awscodeartifact-test-807041577214.d.codeartifact.eu-west-1.amazonaws.com/pypi/pypi-mirror/simple/"
verify_ssl = true

[packages]
tupper = "*"

[requires]
python = "3.9"
```


Say your IAM user policy requires you to verify your identity via multi-factor authentication.

This limits your ability to use the `aws` CLI because you can't provide MFA tokens with your request:

```text
$ aws s3 ls

An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied
```

`wev-awsmfa` will ask for your MFA token as-needed and authenticate you automatically.

## Setup

Install [wev](https://github.com/cariad/wev) (if you haven't already) and `wev-awsmfa`:

```bash
pip3 install wev
pip3 install wev-awsmfa
```

In your working directory (or home directory, to enable `wev-awsmfa`) create or edit a `.wev.yml` file and add the following configuration:

```yaml
[AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
  plugin:
    id: wev-awsmfa
```

This configures [wev](https://github.com/cariad/wev) to set the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` environment variables via the `wev-awsmfa` plugin.

Now, to run `aws s3 ls` via `wev`:

```bash
wev aws s3 ls
```

You'll be prompted to enter your MFA token, then `wev` will authenticate you and run the command.

[wev](https://github.com/cariad/wev) will cache your session for as long as possible, so you won't need to enter a new token every time.

## Advanced configuration

The configuration key must be a list of three strings which prescribe the environment variables to set for:

1. **The access key ID.** You probably want this to be `AWS_ACCESS_KEY_ID`.
1. **The secret access key.** You probably want this to be `AWS_SECRET_ACCESS_KEY`.
1. **The session token.** You probably want this to be `AWS_SESSION_TOKEN`.

Your minimal configuration is likely to look like this:

```yaml
[AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
  plugin:
    id: wev-awsmfa
```

There are two optional properties:

- `mfa_device` describes the ARN of the MFA device to use. `wev-awsmfa` will attempt to discover this automatically if omitted.
- `duration` describes the duration of the temporary session in seconds. Default is 900 seconds.

A configuration with these optional properties set would look like this:

```yaml
[AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN]:
  plugin:
    id: wev-awsmfa
    duration: 1800
    mfa_device: arn:aws:iam::123456789012:mfa/foo
```

## Thank you! 🎉

My name is **Cariad**, and I'm an [independent freelance DevOps engineer](https://cariad.me).

I'd love to spend more time working on projects like this, but--as a freelancer--my income is sporadic and I need to chase gigs that pay the rent.

If this project has value to you, please consider [☕️ sponsoring](https://github.com/sponsors/cariad) me. Sponsorships grant me time to work on _your_ wants rather than _someone else's_.

Thank you! ❤️
