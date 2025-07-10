#!/bin/bash

DB_NAME="gtfs"
DB_HOST="localhost"
DB_PORT="5432"
OUTPUT_DIR="/backups/csv"

# Create output directory in PG container
docker exec postgres-gtfs mkdir -p $OUTPUT_DIR

# Get tables from PG container
TABLES=$(docker exec postgres-gtfs psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -Atc "SELECT tablename FROM pg_tables WHERE schemaname = 'public';")

# Export tables to CSV
for TABLE in $TABLES; do
  echo "Exporting table: $TABLE"
  docker exec postgres-gtfs psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "\COPY \"$TABLE\" TO '$OUTPUT_DIR/$TABLE.csv' WITH CSV HEADER"
done