
all: upload test

test:
	./try2.py
	echo '.schema' | sqlite3 work/something.db | md5
	echo 'SELECT COUNT( * ) FROM councilfull;' | sqlite3 work/something.db
