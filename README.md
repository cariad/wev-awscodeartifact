# wev-awscodeartifact: A `wev` plugin to support Amazon Web Services CodeArtifact authorisation on the command line

[![codecov](https://codecov.io/gh/cariad/wev-awscodeartifact/branch/main/graph/badge.svg?token=D48XKZJXJ7)](https://codecov.io/gh/cariad/wev-awscodeartifact)

- ⚙️ Plugin for **[wev](https://github.com/cariad/wev)** (**w**ith **e**nvironment **v**ariables).
- 📋 **Requests** and **caches** CodeArtifact authorisation tokens.
- 👩🏼‍💻 **Great for freelancers** working with multiple clients hosting CodeArtifact repositories.

## The Problem

Say your `Pipfile` is configured to pull packages from a private Amazon Web Services CodeArtifact repository:

```text
[[source]]
name = "private"
url = "https://aws:$CODEARTIFACT_AUTH_TOKEN@corp-012345678901.d.codeartifact.eu-west-1.amazonaws.com/pypi/pypi-mirror/simple/"
verify_ssl = true

[packages]
tupper = "*"

[requires]
python = "3.9"
```

Your `Pipfile` expects the `CODEARTIFACT_AUTH_TOKEN` environment variable to be set to your authorisation token.

If you try to use `pipenv` before setting `CODEARTIFACT_AUTH_TOKEN` or if it holds an expired token, your pull from the repository will fail.

`wev-awscodeartifact` extends [wev](https://github.com/cariad/wev) to handle your CodeArtifact authorisation token for you.

## Installation

[wev](https://github.com/cariad/wev) and `wev` plugins are usually happy to run within virtual environments, but that's tricky if your project's `Pipfile` has _only_ private sources that require a token.

`wev-awscodeartifact` cannot generate a token before it's installed.

For an easy life, I recommend installing `wev` and `wev-awscodeartifact` globally, _outside_ of your virtual environment.

```bash
pip3 install wev
pip3 install wev-awscodeartifact
```

## Configuration

### Location

[wev](https://github.com/cariad/wev) configuration files apply to the _working_ and _child_ directories.

This gives you a few options for where to place your configuration:

- If you always use the same CodeArtifact repository then place the configuration in your home directory (i.e. `~/.wev.yml`).
- If you're a contractor working on a few projects for a client with a CodeArtifact repository (i.e. you have `~/client-foo/project-a` and `~/client-foo/project-b` on your machine) then place the configuration in your client's project directory (i.e. `~/client-foo/.wev.yml`).
- If you have only one project that requires a CodeArtifact token then place the configuration in that project's directory (i.e. `~/project-foo/.wev.yml`).

### Content

A minimal configuration would look like this:

```yaml
CODEARTIFACT_AUTH_TOKEN:
  plugin:
    id: wev-awscodeartifact
    domain: corp
```

Required properties:

- `domain`: Name of the CodeArtifact domain hosting the private repository.

Optional properties:

- `account`: ID of the AWS account hosting the CodeArtifact domain. Defaults to the account that your credentials authenticate into.
- `region`: AWS region hosting the CodeArtifact domain. Defaults to your AWS credentials profile's region.
- `profile`: Name of the AWS credentials profile to use.

### Configuring your profile when you work in a team

You probably don't want to add the `profile` property to `.wev.yml` if you plan to commit and share it with your team mates. Profile names are personal, and you don't want to force everyone to use the same as you.

If you do need to set `profile`, I suggest you create it in `.wev.user.yml` (which should not be shared) and let `wev` merge it in.

For example:

```yaml
# .wev.yml
CODEARTIFACT_AUTH_TOKEN:
  plugin:
    id: wev-awscodeartifact
    account: "012345678901"
    domain: corp
    region: eu-west-1
```

```yaml
# .wev.user.yml
CODEARTIFACT_AUTH_TOKEN:
  plugin:
    id: wev-awscodeartifact
    profile: work
```

## Usage

With `wev` and `wev-awscodeartifact` installed and configured, you can run `pipenv install` via `wev` to set your CodeArtifact authorisation token:

```bash
wev pipenv install
```

## FAQs

### Can I change the environment variable from CODEARTIFACT_AUTH_TOKEN?

Yes! Call it anything you like.

### Does wev-awscodeartifact work with other package managers?

Yes! `wev-awscodeartifact` will work with _any_ command line tool tnat needs CodeArtifact authorisation tokens in environment variables.

## Thank you! 🎉

My name is **Cariad**, and I'm an [independent freelance DevOps engineer](https://cariad.me).

I'd love to spend more time working on projects like this, but--as a freelancer--my income is sporadic and I need to chase gigs that pay the rent.

If this project has value to you, please consider [☕️ sponsoring](https://github.com/sponsors/cariad) me. Sponsorships grant me time to work on _your_ wants rather than _someone else's_.

Thank you! ❤️
