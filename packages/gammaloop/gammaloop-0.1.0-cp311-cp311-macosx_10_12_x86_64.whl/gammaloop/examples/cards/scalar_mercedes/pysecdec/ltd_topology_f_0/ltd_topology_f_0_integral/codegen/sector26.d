SECTOR26_CPP = \
	src/sector_26.cpp \
	src/sector_26_0.cpp
SECTOR26_DISTSRC = \
	distsrc/sector_26_0.cpp \
	distsrc/sector_26_0.cu
SECTOR_CPP += $(SECTOR26_CPP)

$(SECTOR26_DISTSRC) $(SECTOR26_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR26_CPP)) : codegen/sector26.done ;
