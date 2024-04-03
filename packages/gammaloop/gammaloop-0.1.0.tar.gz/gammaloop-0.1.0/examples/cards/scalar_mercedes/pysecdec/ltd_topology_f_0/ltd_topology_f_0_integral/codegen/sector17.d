SECTOR17_CPP = \
	src/sector_17.cpp \
	src/sector_17_0.cpp
SECTOR17_DISTSRC = \
	distsrc/sector_17_0.cpp \
	distsrc/sector_17_0.cu
SECTOR_CPP += $(SECTOR17_CPP)

$(SECTOR17_DISTSRC) $(SECTOR17_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR17_CPP)) : codegen/sector17.done ;
