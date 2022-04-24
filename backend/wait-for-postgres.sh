#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD="drfpassword" psql -h "$host" -d "database" -U "drf" -c '\q'
do
	>&2 echo "Postgres is unavailable - sleeping"
	sleep 1
done

>&2 echo "Postgres is up"
exec $cmd
