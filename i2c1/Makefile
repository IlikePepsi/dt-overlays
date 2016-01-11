SOURCE = $(wildcard *.dts)
RULES = $(SOURCE:%.dts=99-%.rules)
NAME ?= $(SOURCE:%.dts=%)
BLOB = $(NAME)-$(VERSION).dtbo
VERSION = 00A0
UENV = /boot/uEnv.txt
SET_UENV = ../scripts/set_uenv.py
RM_SLOTS = ../scripts/remove_slots.py
SLOTS ?= /sys/devices/platform/bone_capemgr/slots

build: $(SOURCE)
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)

install: build
	sudo cp $(BLOB) /lib/firmware
	sudo cp $(RULES) /etc/udev/rules.d
	@if ! [[ -x $(SET_UENV) ]] ; then \
		sudo chmod a+x $(SET_UENV) ;\
	fi
	@if [[ "$($(SET_UENV) $(UENV) --select capemgr.enable_partno 1>/dev/null)" != 0 ]] ; then \
		$(SET_UENV) $(UENV) --select optargs --append capemgr.enable_partno 1>/dev/null ; \
	fi
	@sudo $(SET_UENV) $(UENV) --select capemgr.enable_partno --append $(NAME)
	@echo $(NAME) > $(SLOTS)
	make clean

uninstall:
	@if ! [[ -x $(RM_SLOTS) ]] ; then \
		sudo chmod a+x $(RM_SLOTS) ;\
	fi
	@if [[ "$($(RM_SLOTS) $(SLOTS) $(NAME) 1>/dev/null)" == 0 ]] ; then \
		echo "-$($(RM_SLOTS) $(SLOTS) $(NAME) --slot true)" > $(SLOTS) ; \
	fi
	@if ! [ -e /lib/firmware/$(BLOB) ] ; then \
		sudo rm -fv /lib/firmware/$(BLOB) ;\
	fi
	@if ! [ -e /etc/udev/rules.d/$(RULES) ] ; then \
		sudo rm -fv /etc/udev/rules.d/$(RULES) ;\
	fi
	@if ! [ -x $(SET_UENV) ] ; then \
		sudo chmod a+x $(SET_UENV) ;\
	fi
	@sudo $(SET_UENV) $(UENV) --select capemgr.enable_partno --remove $(NAME)
clean:
	sudo rm -fv ./$(BLOB)

test:
	@if ! [[ -x $(RM_SLOTS) ]] ; then \
		sudo chmod a+x $(RM_SLOTS) ;\
	fi
	echo "$($(RM_SLOTS) $(SLOTS) $(NAME) --slot true)"

