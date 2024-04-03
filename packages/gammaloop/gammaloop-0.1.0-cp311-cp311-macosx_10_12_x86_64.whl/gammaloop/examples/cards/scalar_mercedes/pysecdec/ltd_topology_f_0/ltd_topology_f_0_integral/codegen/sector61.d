SECTOR61_CPP = \
	src/sector_61.cpp \
	src/sector_61_0.cpp
SECTOR61_DISTSRC = \
	distsrc/sector_61_0.cpp \
	distsrc/sector_61_0.cu
SECTOR_CPP += $(SECTOR61_CPP)

$(SECTOR61_DISTSRC) $(SECTOR61_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR61_CPP)) : codegen/sector61.done ;
