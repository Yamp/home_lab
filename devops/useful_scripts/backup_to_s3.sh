echo Starting "$(date)"
cd /root/compose-config/postgres_config/ || exit 1
/usr/local/bin/docker-compose exec -T real_postgres backup || (echo "Have not backuped" && exit 1)
/usr/local/bin/docker-compose run -T --rm awscli upload
echo Stopping "$(date)"
