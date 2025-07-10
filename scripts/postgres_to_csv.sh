#!/bin/bash
set -e 

DB_NAME="gtfs"
DB_HOST="localhost"
DB_PORT="5432"
OUTPUT_DIR="/backups/csv"

# Create output directory in PG container
docker exec postgres-gtfs mkdir -p $OUTPUT_DIR

# Verify directory was created
if ! docker exec postgres-gtfs test -d $OUTPUT_DIR; then
    echo "Error: Failed to create directory $OUTPUT_DIR"
    exit 1
fi

# Get tables from PG container
TABLES=$(docker exec postgres-gtfs psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -Atc "SELECT tablename FROM pg_tables WHERE schemaname = 'public';")

if [ -z "$TABLES" ]; then
    echo "No tables found in the database"
    exit 1
fi

echo "Found tables: $TABLES"

# Export tables to CSV
for TABLE in $TABLES; do
  echo "Exporting table: $TABLE"
  docker exec postgres-gtfs psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "\COPY \"$TABLE\" TO '$OUTPUT_DIR/$TABLE.csv' WITH CSV HEADER"
done

echo "CSV export completed. Files are available in: ./data/postgres/backups/csv/"