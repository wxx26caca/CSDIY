#!/bin/bash

# Get ethernet ipv4/ipv6 address
eth_ipv4=$(ifconfig $eth_name | grep -i 'inet addr' | sed 's/^.*addr://g' | sed 's/Bcast.*$//g' | sed 's/[[:space:]]//g')
eth_ipv6=$(ifconfig $eth_name | grep -i 'inet6 addr:' | grep -i 'Scope:Global' | sed 's/^.*addr://g' | cut -d'/' -f1 | sed 's/[[:space:]]//g')

# Output with timestamp
info() {
    local cmd; cmd=$(basename $0)
    echo "$(date --rfc-3339=seconds) $cmd.info: $*" >> "$LOGFILE_"
    >&2 echo "$cmd.info: $*"
}

