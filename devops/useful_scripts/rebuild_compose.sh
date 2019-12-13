echo Starting "$(date)"
cd /root/compose-config/postgres_config/scripts/ && /usr/bin/docker image prune -a -f
./pull_all_images.sh
/usr/local/bin/docker-compose pull
/usr/local/bin/docker-compose build --no-cache
/usr/local/bin/docker-compose up -d
echo Stopping "$(date)"
