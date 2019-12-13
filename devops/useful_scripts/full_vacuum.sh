echo Starting "$(date)"
cd /root/compose-config/postgres_config/ || exit 1
/usr/local/bin/docker-compose exec -T real_postgres full_maintenance
echo Stopping "$(date)"
