SOURCE = $(wildcard *.dts)
RULES = $(wildcard *.rules)
VERSION = 00A0
BLOB = $(SOURCE:%.dts=%-$(VERSION).dtbo)

all:
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install:
	cp $(BLOB) /lib/firmware

# probably root permissions needed for this
udev_rules:
	cp $(RULES) /etc/udev/rules.d 

clean:
	rm -f ./$(BLOB)
	rm -f /lib/firmware/$(BLOB)
