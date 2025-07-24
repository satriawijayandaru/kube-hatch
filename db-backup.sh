#!/bin/bash

# Configuration
BACKUP_DIR="/home/ubuntu-server/backupdb"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_HOST=""
POSTGRES_PORT=""
POSTGRES_DB=""
MONGO_HOST=""
MONGO_USER=""
MONGO_PASSWORD=""
MONGO_PORT=""
ELASTIC_HOST=""
ELASTIC_PORT=""
ELASTIC_URL="http://$ELASTIC_HOST:$ELASTIC_PORT"


mkdir -p "$BACKUP_DIR/$TIMESTAMP"

echo "Backing up all MongoDB databases..."
mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" --username "$MONGO_USER" --password "$MONGO_PASSWORD" --out "$BACKUP_DIR/$TIMESTAMP/mongo" && echo "All MongoDB databases backup completed."
echo "------------------------------------------------"
echo "Backing up all PostgreSQL databases..."
mkdir -p "$BACKUP_DIR/$TIMESTAMP/postgres"
PGPASSWORD="$POSTGRES_PASSWORD" pg_dumpall -U "$POSTGRES_USER" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -f "$BACKUP_DIR/$TIMESTAMP/postgres/postgres.dump"
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -U "$POSTGRES_USER" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" $POSTGRES_DB > $BACKUP_DIR/$TIMESTAMP/postgres/$POSTGRES_DB.sql
echo "All PostgreSQL databases backup completed."
echo "------------------------------------------------"
echo "Backing up Elasticsearch..."
elasticdump --input="$ELASTIC_URL" --output="$BACKUP_DIR/$TIMESTAMP/elasticsearch.json" --type=data
echo "Elasticsearch backup completed."
echo "------------------------------------------------"
echo "Compressing backups..."
tar -czf "$BACKUP_DIR/$TIMESTAMP.tar.gz" -C "$BACKUP_DIR" "$TIMESTAMP" && rm -rf "$BACKUP_DIR/$TIMESTAMP"
echo "Backup completed: $BACKUP_DIR/$TIMESTAMP.tar.gz"
echo "------------------------------------------------"
echo "Removing backups older than 30 days..."
find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +30 -exec rm -f {} \;
echo "Old backups removed.
