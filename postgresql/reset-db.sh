#! /bin/sh
docker cp scripts postgres-14:/tmp/
docker exec -it postgres-14 psql -U sigl2023 -d socrate -f /tmp/scripts/create-database.sql
docker exec -it postgres-14 psql -U sigl2023 -d socrate -f /tmp/scripts/create-tables.sql
docker exec -it postgres-14 psql -U sigl2023 -d socrate -f /tmp/scripts/load-data-source.sql
docker exec -it postgres-14 psql -U sigl2023 -d socrate -f /tmp/scripts/export-tables.sql
docker exec -it postgres-14 psql -U sigl2023 -d socrate -f /tmp/scripts/load-data.sql

