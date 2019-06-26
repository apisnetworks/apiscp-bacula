#!/bin/bash
set -euo pipefail
shopt -s nullglob

DIR="$(dirname "$0")"
CNFDIR="/etc/bacula/local.d"
[[ -f /etc/bacula/local.d/extra.sh ]] && . /etc/bacula/local.d/extra.sh sd

set -o allexport
. /etc/sysconfig/bacula-vars
set +o allexport

. "${DIR}/../helpers.sh"

env_fill "${DIR}/sd-director.conf"

find "$CNFDIR" -mindepth 1 -type d | while read -r n ; do
		SLOT=$(basename "$n")
done
