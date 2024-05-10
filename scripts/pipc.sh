#! /bin/bash

#####################################################################
# Per https://sharats.me/posts/shell-script-best-practices/ (partial)
set -o errexit
#set -o nounset  # We want the treat-undef-as-empty-string behavior here
set -o pipefail

if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi
#####################################################################


if [[ -z $1 ]]
then
  echo "No pip-compile targets provided."
  exit 1
fi

for arg
do
  case "$arg" in
    (dev | ci | flake8 | rtd)
      CUSTOM_COMPILE_COMMAND="$0 $*" pip-compile -o "requirements-$arg.txt" "requirements-$arg.in"
      ;;
    *)
      echo "Unknown argument '$arg'"
      ;;
  esac
done
