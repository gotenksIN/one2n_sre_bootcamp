# Vagrant

Runs the API stack in a Debian VM with PostgreSQL, two API containers, migrations, and Nginx load balancing.

## Prerequisites

- **Vagrant**

## Quick Start

From the repository root:

```bash
vagrant up
```

Create the environment file:

```bash
cp vagrant/.env.example vagrant/.env
```

Run these commands from the `vagrant/` directory:

```bash
make build
make up
make status
```

The API is available on `http://127.0.0.1:8080`.

## Commands

```bash
make logs   # Follow container logs
make down   # Stop the stack
make clean  # Remove containers and volumes
```

## Verify

```bash
curl http://127.0.0.1:8080/api/v1/healthcheck
```

Expected response:

```json
{"status":"healthy"}
```
