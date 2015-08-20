#!/bin/sh

/usr/local/mysql/bin/mysqldump -u root antares_demo Alert AlertReplica Attribute AttributeValue AstroObject Locus AlertStatus Combo InCombo PLV_SDSS > LA_Alert_DB.sql
