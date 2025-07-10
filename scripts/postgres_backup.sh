#!/bin/bash

# Get secrets
POSTGRES_USER=$(docker secret ls -q gtfs-postgres-user)
POSTGRES_PASSWORD=$(docker secret ls -q gtfs-postgres-password)

# Backup postgres database
docker exec -it postgres-gtfs pg_dump -U ${POSTGRES_USER} -d gtfs -Fc -f /backups/backup_$(date +%Y%m%d_%H%M%S).sql


# Restore postgres database
# docker exec -it postgres-gtfs pg_restore -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f /backups/backup_$(date +%Y%m%d_%H%M%S).sql