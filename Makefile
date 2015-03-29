
all: upload test

test:
	nosetests -s t_createuptodateregister.py
	./createuptodateregister.py work/something.db | diff -wiu createuptodateregister.sql - > /dev/null || ( echo -e '\033[00;31m=== FAIL ===\033[00m'; false )
	@echo -e '\033[00;32mSUCCESS\033[00m';
