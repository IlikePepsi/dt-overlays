SOURCE = $(wildcard *.dts)
RULES = $(SOURCE:%.dts=99-%.rules)
NAME ?= $(SOURCE:%.dts=%)
BLOB = $(NAME)-$(VERSION).dtbo
VERSION = 00A0
UENV.TXT = /boot/uEnv.txt
UENV.PY = ../scripts/uEnv.py

build: $(SOURCE)
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install: build
	sudo cp $(BLOB) /lib/firmware
	sudo cp $(RULES) /etc/udev/rules.d
	@if ! [ -x $(UENV.PY) ] ; then \
		chmod a+x $(UENV.PY) ;\
	fi
	@if [[ "$($(UENV.PY) $(UENV.TXT) --select capemgr.enable_partno 1>/dev/null)" != 0 ]] ; then \
		$(UENV.PY) $(UENV.TXT) --select optargs --append capemgr.enable_partno 1>/dev/null ;\
	fi
	@sudo $(UENV.PY) $(UENV.TXT) --select capemgr.enable_partno --append $(NAME)

uninstall:
	@if ! [ -e /lib/firmware/$(BLOB) ] ; then \
		sudo rm -fv /lib/firmware/$(BLOB) ;\
	fi
	@if ! [ -e /etc/udev/rules.d/$(RULES) ] ; then \
		sudo rm -fv /etc/udev/rules.d/$(RULES) ;\
	fi
	if ! [ -x $(UENV.PY) ] ; then \
		chmod a+x $(UENV.PY) ;\
	fi
	sudo $(UENV.PY) $(UENV.TXT) --select capemgr.enable_partno --remove $(NAME)

clean:
	sudo rm -fv ./$(BLOB)
