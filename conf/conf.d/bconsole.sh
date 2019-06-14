#!/bin/bash
set -euo pipefail
shopt -s nullglob

[[ -f /etc/bacula/local.d/extra.sh ]] && . /etc/bacula/local.d/extra.sh sd

set -o allexport
. /etc/sysconfig/bacula-vars
set +o allexport

. "$(dirname "$0")/../helpers.sh"

env_fill "$(dirname "$0")/bconsole.conf"
