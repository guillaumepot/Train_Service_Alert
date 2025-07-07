- Ingestion BDD (consumer) (finir construction des df en particulier df sa)
kafka1 et 2 ports à #

-> DBT
-> BI
-> (API)


docker compose --profile database up -d
docker compose --profile administration up -d
docker compose --profile pipeline up -d

**GTFS update:**
docker compose --profile gtfs-update up -d