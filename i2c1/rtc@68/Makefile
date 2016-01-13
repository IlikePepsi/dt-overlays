RULES = $(wildcard *.rules)
SCRIPTS = $(wildcard *.sh)
SERVICES = $(wildcard *.service)

RULESPATH = /etc/udev/rules.d
SCRIPTPATH = /usr/src
SERVICEPATH = /usr/lib/systemd/system

# Make targets will break if there are more than one	\
# files of each type

install:
	@echo "    ..rtc@68.."
	@sudo cp $(SERVICES) $(SERVICEPATH)
	@sudo cp $(SCRIPTS) $(SCRIPTPATH)
	@sudo cp $(RULES) $(RULESPATH)
	@sudo systemctl daemon-reload
	@sudo systemctl enable $(SERVICES) 1>/dev/null
	@sudo systemctl start $(SERVICES)
	@echo "    ..done!"

uninstall:
	@echo "    ..rtc@68.."
	@sudo systemctl stop $(SERVICES)
	@sudo systemctl disable $(SERVICES)
	@if [ -e $(RULESPATH)/$(RULES) ] ; then 	\
		sudo rm -fv $(RULESPATH)/$(RULES) ;	\
	fi
	@if [ -e $(SCRIPTPATH)/$(SCRIPTS) ] ; then 	\
		sudo rm -fv $(SCRIPTPATH)/$(SCRIPTS) ;	\
	fi
	@if [ -e $(SERVICEPATH)/$(SERVICES) ] ; then 	\
		sudo rm -fv $(SERVICEPATH)/$(SERVICES) ;\
	fi
	@echo "    ..done!"


