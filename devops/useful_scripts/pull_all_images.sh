/usr/bin/docker images | /bin/grep -v REPOSITORY | /usr/bin/awk '{print $1}' | xargs -L1 /usr/bin/docker pull
