SOURCE = $(wildcard *.dts)
VERSION = 00A0
RULES = $(SOURCE:%.dts=99-%.rules)
BLOB = $(SOURCE:%.dts=%-$(VERSION).dtbo)
NAME = $(SOURCE:%.dts=%)
UENV.TXT = /boot/uEnv.txt
UENV.PY = ../scripts/uEnv.py

build: $(SOURCE)
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install: build
	sudo cp $(BLOB) /lib/firmware
	sudo cp $(RULES) /etc/udev/rules.d
	if ! [ -x $(UENV.PY) ] ; then \
		chmod a+x $(UENV.PY) ;
	sudo $(UENV.PY) $(UENV.TXT) --select capemgr.enable_partno --append $(NAME)

uninstall:
	if ! [ -e /lib/firmware/$(BLOB) ] ; then \
		sudo rm -fv /lib/firmware/$(BLOB) ;
	if ! [ -e /etc/udev/rules.d/$(RULES) ] ; then \
		sudo rm -fv /etc/udev/rules.d/$(RULES) ;
	if ! [ -x $(UENV.PY) ] ; then \
		chmod a+x $(UENV.PY) ;
	sudo $(UENV.PY) $(UENV.TXT) --select capemgr.enable_partno --remove $(NAME)

clean:
	sudo rm -fv ./$(BLOB)
