#!bin/bash

if [ -d "/home/dontmanage/dontmanage-bench/apps/dontmanage" ]; then
    echo "Bench already exists, skipping init"
    cd dontmanage-bench
    bench start
else
    echo "Creating new bench..."
fi

bench init --skip-redis-config-generation dontmanage-bench

cd dontmanage-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis:6379
bench set-redis-queue-host redis:6379
bench set-redis-socketio-host redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

bench get-app lms

bench new-site lms.localhost \
--force \
--mariadb-root-password 123 \
--admin-password admin \
--no-mariadb-socket

bench --site lms.localhost install-app lms
bench --site lms.localhost set-config developer_mode 1
bench --site lms.localhost clear-cache
bench --site lms.localhost set-config mute_emails 1
bench use lms.localhost

bench start