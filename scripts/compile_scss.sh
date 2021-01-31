#!/usr/bin/env bash

set -e # Stop the script on errors
set -u # Unset variables are an error

this_script_path=$(cd "$(dirname "$0")" && pwd) # Relative, Absolutized and normalized
if [ -z "$this_script_path" ]; then # Error, for some reason, the path is not accessible to the script (e.g. permissions re-evalued after suid)
  exit 1
fi

cd "$this_script_path/../" || exit 1

sass --stop-on-error noxcrux_server/static/scss/basics.scss noxcrux_server/static/css/basics.css;
sass --stop-on-error noxcrux_server/static/scss/main.scss noxcrux_server/static/css/main.css;
