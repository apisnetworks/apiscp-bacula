#!/bin/bash
set -euo pipefail
shopt -s nullglob

DIR=$(dirname "$0")
CNFDIR="$DIR/servers"
[[ -f /etc/bacula/local.d/extra.sh ]] && . /etc/bacula/local.d/extra.sh sd

set -o allexport
. /etc/sysconfig/bacula-vars
set +o allexport

. "$(dirname "$0")/../helpers.sh"

env_fill "$(dirname "$0")/sd-director.conf"

find "$CNFDIR" -mindepth 1 -type d | while read -r n ; do
		SLOT=$(basename "$n")
done
