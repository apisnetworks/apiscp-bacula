#!/bin/bash
set -euo pipefail
shopt -s nullglob

[[ -f /etc/bacula/local.d/extra.sh ]] && . /etc/bacula/local.d/extra.sh sd
. "$(dirname "$0")/../helpers.sh"

set -o allexport
. /etc/sysconfig/bacula-vars
set +o allexport

env_fill "$(dirname "$0")/sd-director.conf"
