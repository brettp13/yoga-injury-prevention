#!/bin/bash
#
# This script generates a pg_dump database backup
#

DB_CONTAINER_ID=$(docker ps | grep postgresql | head -n1 | awk '{print $1;}')
DATE=$(date +"%m-%d-%y")

backup()
{	
	docker exec -i $DB_CONTAINER_ID pg_dump -U yogaforyoursake yipee > YIP-BACKUP-$DATE.sql
	aws s3 mv YIP-BACKUP-$DATE.sql s3://yoga-injury-prevention-db-backups
}

restore()
{
	docker exec -i $DB_CONTAINER_ID psql -U yogaforyoursake -d yipee < db.sql
}

# main execution
while [ "$1" != "" ]; do
	case $1 in
		--backup )
			backup
			shift
			;;
		--restore )
			restore
			shift
			;;
		* )
			exit
	esac
done

exit

