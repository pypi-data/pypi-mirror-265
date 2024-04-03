SECTOR25_CPP = \
	src/sector_25.cpp \
	src/sector_25_0.cpp
SECTOR25_DISTSRC = \
	distsrc/sector_25_0.cpp \
	distsrc/sector_25_0.cu
SECTOR_CPP += $(SECTOR25_CPP)

$(SECTOR25_DISTSRC) $(SECTOR25_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR25_CPP)) : codegen/sector25.done ;
