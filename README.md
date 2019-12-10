
# VyOS configuration utility

This utility parses VyOS configuration file and allows dumping it as
list of rules that can be copied to the CLI configuration session.

Main idea is to copy large segments of rules to new device, without
loading the whole configuration file.

## Installing

Checkout from git and install:

    git clone https://github.com/hile/vyos-config
    cd vyos-config
    pip install .

## Example usage

Dump backed up configuration file::

    vyos-config list ~/config.boot

Dump only 'service' section from loaded file:

    vyos-config list --prefix service ~/config.boot

Dump configuration for eth2 VLAN 102

    vyos-config list --prefix 'interfaces ethernet eth2 vif 102' ~/config.boot
