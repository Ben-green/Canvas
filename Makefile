
all: upload test

test:
	./try2.py && echo '.schema' | sqlite3 work/something.db
