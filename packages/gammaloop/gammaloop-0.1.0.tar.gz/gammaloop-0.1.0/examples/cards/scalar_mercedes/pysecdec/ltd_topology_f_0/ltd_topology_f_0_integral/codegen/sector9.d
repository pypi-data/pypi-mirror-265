SECTOR9_CPP = \
	src/sector_9.cpp \
	src/sector_9_0.cpp
SECTOR9_DISTSRC = \
	distsrc/sector_9_0.cpp \
	distsrc/sector_9_0.cu
SECTOR_CPP += $(SECTOR9_CPP)

$(SECTOR9_DISTSRC) $(SECTOR9_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR9_CPP)) : codegen/sector9.done ;
