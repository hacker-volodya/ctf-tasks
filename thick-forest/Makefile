all: clean
	mkdir -p build
	gcc -s checker.c main.c -o build/check_password
debug: clean
	mkdir -p build
	gcc -D DEBUG checker.c main.c -o build/check_password
clean:
	rm -rf build