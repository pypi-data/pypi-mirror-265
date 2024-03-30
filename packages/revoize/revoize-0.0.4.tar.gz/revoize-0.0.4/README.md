# Revoize SDK

Stay tuned for updates!

## Publishing to PyPi

This section contains a guide for maintainers about publishing to PyPi.

Before you can publish updates to this package you need to go through a few steps of configuration:
1. Create a PyPi account.
2. Contact Revoize admins to add you to package maintainers.
3. Create a PyPi API token.
4. Configure Poetry to use the API token with `poetry config pypi-token.pypi <token>`

You can then issue updates with:
1. `poe bump-version (major|minor|patch)`
2. Commit the change, have it reviewed and merged
3. `poe publish`
