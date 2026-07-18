# Vagrant Environment

The Vagrant environment provides a Debian VM for running the `vagrant/Makefile`
Docker Compose stack.

[Back to the project README](../README.md)

## Architecture

The root `Vagrantfile` provisions Debian with Docker and Compose, mounts the
repository at `/vagrant`, and forwards guest port `8080` to
`127.0.0.1:8080` on the host.

Inside the VM, Compose starts components in this order:

1. PostgreSQL becomes healthy.
2. The one-shot migration container upgrades the database.
3. Two API containers become healthy.
4. Nginx listens on port `8080` and balances requests across both APIs.

## Requirements

- Vagrant
- libvirt and the Vagrant libvirt provider

## Run Order

Create and enter the VM from the repository root:

```bash
vagrant up
vagrant ssh
```

Run the following commands inside the VM:

```bash
cd /vagrant
cp vagrant/.env.example vagrant/.env
make -C vagrant build
make -C vagrant up
make -C vagrant status
```

The API is available from the host at `http://127.0.0.1:8080`.

## Targets

| Target | Purpose |
|---|---|
| `build` | Build the API images |
| `up` | Start PostgreSQL, migration, API replicas, and Nginx |
| `status` | Show Compose service state |
| `logs` | Follow Compose logs |
| `down` | Stop the Compose stack |
| `clean` | Remove the stack, volumes, and unused Docker objects |

`clean` runs `docker system prune -f` inside the current Docker environment.
