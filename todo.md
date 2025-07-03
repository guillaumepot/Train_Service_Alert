- Cmd pour faire des backup postgres sur le container dans le volume


docker exec -it postgres-gtfs psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
SHOW shared_buffers;
SHOW work_mem;
SHOW effective_cache_size;
