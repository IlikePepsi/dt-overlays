i2c1:
	cd i2c1/ ;\
	make blob ;\
	make install ;

i2c1_remove:
	cd i2c1/ ;\
	make uninstall ;

spi0:
	cd spi0/ ;\
	make blob ;\
	make install ;

spi0_remove:
	cd spi0/ ;\
	make uninstall ;

clean:
	cd i2c1/ ;\
	make clean;
	cd spi0/ ;\
	make clean;
