SECTOR41_CPP = \
	src/sector_41.cpp \
	src/sector_41_0.cpp
SECTOR41_DISTSRC = \
	distsrc/sector_41_0.cpp \
	distsrc/sector_41_0.cu
SECTOR_CPP += $(SECTOR41_CPP)

$(SECTOR41_DISTSRC) $(SECTOR41_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR41_CPP)) : codegen/sector41.done ;
