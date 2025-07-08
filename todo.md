-> DBT
-> BI
-> (API)
-> CI/CD pipeline


**services**
docker compose --profile database up -d
docker compose --profile administration up -d
docker compose --profile pipeline up -d

**GTFS update:**
docker compose --profile gtfs-update up


**Config**
Secrets:
postgres_user.secret
postgres_password.secret