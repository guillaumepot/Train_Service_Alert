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


**Crontab**
# every 2 minutes
*/2 * * * * cd /home/sandbox/train-service-alert/src/dbt/train_service_alert && dbt run >> /home/sandbox/train-service-alert/logs/dbt_run.log 2>&1