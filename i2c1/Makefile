SOURCE = $(wildcard *.dts)
VERSION = 00A0
RULES = $(SOURCE:%.dts=99-%.rules)
BLOB = $(SOURCE:%.dts=%-$(VERSION).dtbo)
NAME = $(SOURCE:%.dts=%)

build: $(SOURCE)
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install: build
	sudo cp $(BLOB) /lib/firmware
	sudo cp $(RULES) /etc/udev/rules.d
	sudo python ../scripts/bootargs.py /boot/uEnv.txt --select Optargs --append capemgr.enable_partno=$(NAME)

uninstall:
	sudo rm -fv /lib/firmware/$(BLOB)
	sudo rm -fv /etc/udev/rules.d/$(RULES)
	sudo python ../scripts/bootargs.py /boot/uEnv.txt --select Optargs --remove capemgr.enable_partno=$(NAME)

clean:
	sudo rm -fv ./$(BLOB)
