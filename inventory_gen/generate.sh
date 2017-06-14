#!/usr/bin/env bash

set -eo pipefail

INV_PATH="/home/ansible/ansible/inventories"
TEMPLATES="./templates"

main() {
  local input=$1
  local inv=$2
  
  local inv_path="${INV_PATH}/${inv}"  

  mkdir -pv "${inv_path}"
  
  log "generating hosts file" 
  python ./inv_gen.py --input_file="$input" --template_file="$TEMPLATES/hosts.j2" --output_file="${inv_path}/hosts"

  mkdir -pv "${inv_path}/group_vars"

  log "generating vars file" 
  python ./inv_gen.py --input_file="$input" --template_file="$TEMPLATES/all.yml.j2" --output_file="${inv_path}/group_vars/all.yml"

  log 'complete!'
}

log() {
  echo -e "\n[$(date +'%Y-%m-%d %H:%M:%S%z')]: $@"
}

if [[ $1 == '-h' || $1 == '--help' || $# -lt 2 ]]; then
  echo -e "Usage: $0 <input> <inventory>"
  echo -e "\tinput     \tinput xml file"
  echo -e "\tinventory \tinventory name to generate at ${INV_PATH}"
  exit 1
fi

main "$@"
