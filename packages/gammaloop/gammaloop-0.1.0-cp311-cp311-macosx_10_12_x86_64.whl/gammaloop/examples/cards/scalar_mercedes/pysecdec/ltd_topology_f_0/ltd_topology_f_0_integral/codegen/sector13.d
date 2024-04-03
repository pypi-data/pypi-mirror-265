SECTOR13_CPP = \
	src/sector_13.cpp \
	src/sector_13_0.cpp
SECTOR13_DISTSRC = \
	distsrc/sector_13_0.cpp \
	distsrc/sector_13_0.cu
SECTOR_CPP += $(SECTOR13_CPP)

$(SECTOR13_DISTSRC) $(SECTOR13_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR13_CPP)) : codegen/sector13.done ;
