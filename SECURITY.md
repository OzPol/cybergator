# Security and deployment scope

This version is a local sample-data research demo with shared mutable JSON/CSV
files. It has no accounts, private data isolation, or production authorization.
Docker Compose binds the published port to 127.0.0.1. Public hosting and private
uploads require a separate application security and tenancy design.

## Credentials

Use environment variables or an untracked .env file. These files and Git history
are excluded from Docker build context. Previously committed Neo4j credentials
must be revoked or rotated at the provider; source removal alone does not fix
credential exposure. Do not reuse them.

Legacy authentication routes are not registered, including the old account
deletion endpoint. Keeping those modules for development does not make their
old access-control model suitable for deployment.

## Dependency updates

Rebuild and recreate containers after dependency/base-image updates. GitHub
alerts refer to repository dependencies and do not establish what is installed
on a developer's host. Check each active environment separately.

CI audits resolved Python dependencies with pip-audit. A clean audit means no
known findings in that advisory source at that time; it is not a complete
security assessment. OS packages, client-side JavaScript, retained Git history,
and deployment configuration require their own review.
