#!/bin/sh

/usr/local/mysql/bin/mysqldump -u root antares_demo Alert AlertReplica Attribute AttributeValue AstroObject Locus > LA_Alert_DB.sql
