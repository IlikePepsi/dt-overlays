SOURCE = $(wildcard *.dts)
RULES = $(SOURCE:%.dts=99-%.rules)
NAME ?= $(SOURCE:%.dts=%)
BLOB = $(NAME)-$(VERSION).dtbo
VERSION = 00A0
KEY ?= bone_capemgr.enable_partno
UENV = /boot/uEnv.txt
SET_UENV = ../scripts/set_uenv.py
RM_SLOTS = ../scripts/read_slots.py
SLOTS ?= /sys/devices/platform/bone_capemgr/slots


define get_slotnumber =
-$(shell $(RM_SLOTS) $(SLOTS) $(NAME) --slot true 2>/dev/null)
endef


define test_slot =
$(RM_SLOTS) $(SLOTS) $(NAME) &>/dev/null
endef


build: $(SOURCE)
	@echo
	@echo "Building.."
	@echo "    ..overlay.."
	dtc -O dtb -o $(BLOB) -b 0 -@ $(SOURCE)
	@echo


install: build
	@echo "Installing.."
	@echo "    ..install overlay binary.."
	@sudo cp $(BLOB) /lib/firmware
	@echo "    ..install udev rules.."
	@sudo cp $(RULES) /etc/udev/rules.d
	@if [[ "$($(SET_UENV) $(UENV) --select $(KEY) 1>/dev/null)" != 0 ]] ; then \
		$(SET_UENV) $(UENV) --select optargs --append $(KEY) &>/dev/null ; \
	fi
	@echo "    ..set boot parameter.."
	@sudo $(SET_UENV) $(UENV) --select $(KEY) --append $(NAME) &>/dev/null
	@echo "    ..assign overlay slot.."
	@$(call test_slot) ; if [ $$? != 0 ] ; then 	\
		echo $(NAME) > $(SLOTS) ;		\
	fi
	@echo "    ..install $(NAME) bus devices.."
	@cd ./rtc@68 ;					\
	make install
	@echo "Cleaning build directory.."
	@$(MAKE) clean
	@echo "    ..done!"


uninstall:
	@echo "Uninstalling.."
	@echo "    ..uninstall $(NAME) bus devices.."
	@cd ./rtc@68 ;					\
		make uninstall
	@echo "    ..free overlay slot.."
	$(eval SLOT := $(call get_slotnumber))
	@$(call test_slot) ; if [ $$? == 0 ] ; then 	\
		echo $(SLOT) > $(SLOTS) ;		\
	fi
	@echo "    ..uninstall overlay binary.."
	@if [ -e /lib/firmware/$(BLOB) ] ; then 	\
		sudo rm -fv /lib/firmware/$(BLOB) ;	\
	fi
	@echo "    ..uninstall udev rules.."
	@if [ -e /etc/udev/rules.d/$(RULES) ] ; then 	\
		sudo rm -fv /etc/udev/rules.d/$(RULES) ;\
	fi
	@echo "    ..remove boot parameter.."
	$(call set_permission, $(SET_UENV))
	@sudo $(SET_UENV) $(UENV) --select $(KEY) --remove $(NAME) &>/dev/null
	@echo "    ..done!"


clean:
	@echo "    ..remove overlay binary.."
	@sudo rm -fv ./$(BLOB)
