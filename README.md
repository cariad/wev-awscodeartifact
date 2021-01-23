# wev-awscodeartifact:<br />A wev plugin to support Amazon Web Services CodeArtifact authorisation on the command line

[![codecov](https://codecov.io/gh/cariad/wev-awscodeartifact/branch/main/graph/badge.svg?token=D48XKZJXJ7)](https://codecov.io/gh/cariad/wev-awscodeartifact)

- ⚙️ Plugin for **[wev](https://github.com/cariad/wev)** (**w**ith **e**nvironment **v**ariables).
- 📋 **Requests** and **caches** CodeArtifact authorisation tokens.
- 👩🏼‍💻 **Great for freelancers** working with multiple clients hosting CodeArtifact repositories.

[![asciicast](https://asciinema.org/a/386503.svg)](https://asciinema.org/a/386503)

## 🔥 The Problem

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

`wev-awscodeartifact` extends [wev](https://github.com/cariad/wev) to handle your CodeArtifact authorisation token for you.

## 🎁 Installation

`wev-awscodeartifact` requires Python 3.8 or later and [wev](https://github.com/cariad/wev).

`wev` and `wev` plugins are usually happy to run within virtual environments, but that's tricky if your project's `Pipfile` has _only_ private sources that require a token. `wev-awscodeartifact` cannot generate a token before it's installed.

I recommend installing `wev` and `wev-awscodeartifact` globally, _outside_ of your virtual environment.

```bash
python -m pip install wev
python -m pip install wev-awscodeartifact
```

## ⚙️ Configuration

### Filename and location

See [wevcli.app/configuration](https://wevcli.app/configuration) for a detailed guide to `wev` configuration files.

If in doubt, create your configuration file as `wev.yml` in your project directory.

### Properties

| Property | Required | Description                                 | Default                  |
|----------|----------|---------------------------------------------|--------------------------|
| account  |          | AWS account ID                              | _Your profile's account_ |
| domain   | ✔️        | CodeArtifact domain name<sup>1</sup>        |                          |
| profile  |          | AWS named profile to use for authentication | _Your default profile_   |
| region   |          | AWS region hosting the CodeArtifact domain  | _Your profile's region_  |

<sup>1</sup> The CodeArtifact domain is _not_ the same as the repository's domain name. Given the domain name `corp-000000000000.d.codeartifact.eu-west-1.amazonaws.com`, the CodeArtifact domain is `corp`.

### Examples

#### Minimal configuration

```yaml
CODEARTIFACT_AUTH_TOKEN:
  plugin:
    id: wev-awscodeartifact
    domain: corp
```

#### Team + personal configuration

You probably don't want to add the `profile` property to `.wev.yml` if you plan to commit and share it with your team mates. Profile names are personal, and you don't want to force everyone to use the same as you.

If you _do_ need to set `profile`, I suggest you create it in `.wev.user.yml` (which should not be shared) and let `wev` merge it in.

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
    profile: work
```

## 💻 Usage

Run `wev` with any command that requires a CodeArtifact authorisation token.

For example, to run `pipenv install` with a CodeArtifact authorisation token:

```bash
wev pipenv install
```

More examples:

- [Amazon Web Services CodeArtifact authorisation token](https://wevcli.app/examples/aws-codeartifact/) on [wevcli.app](https://wevcli.app).

## 🙋‍♀️ FAQs

### Can I change the environment variable from CODEARTIFACT_AUTH_TOKEN?

Yes! Call it anything you like.

### Does wev-awscodeartifact work with other package managers?

Yes! `wev-awscodeartifact` will work with _any_ command line tool that needs CodeArtifact authorisation tokens in environment variables.

## 🎉 Thank you!

My name is **Cariad**, and I'm an [independent freelance DevOps engineer](https://cariad.me).

I'd love to spend more time working on projects like this, but--as a freelancer--my income is sporadic and I need to chase gigs that pay the rent.

If this project has value to you, please consider [☕️ sponsoring](https://github.com/sponsors/cariad) me. Sponsorships grant me time to work on _your_ wants rather than _someone else's_.

Thank you! ❤️
