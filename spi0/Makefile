SOURCE = $(wildcard *.dts)
VERSION = 00A0
BLOB = $(SOURCE:%.dts=%-$(VERSION).dtbo)

all:
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install:
	cp $(BLOB) /lib/firmware

clean:
	rm -f ./$(BLOB)
	rm -f /lib/firmware/$(BLOB)
