SOURCE = $(wildcard *.dts)
VERSION = 00A0
RULES = $(SOURCE:%.dts=99-%.rules)
BLOB = $(SOURCE:%.dts=%-$(VERSION).dtbo)

blob:
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install:
	sudo cp $(BLOB) /lib/firmware
	sudo cp $(RULES) /etc/udev/rules.d 

unistall:
	sudo rm -fv /lib/firmware/$(BLOB)
	sudo rm -fv /etc/udev/rules.d/$(RULES)

clean:
	sudo rm -fv ./$(BLOB)
