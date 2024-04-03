SECTOR37_CPP = \
	src/sector_37.cpp \
	src/sector_37_0.cpp
SECTOR37_DISTSRC = \
	distsrc/sector_37_0.cpp \
	distsrc/sector_37_0.cu
SECTOR_CPP += $(SECTOR37_CPP)

$(SECTOR37_DISTSRC) $(SECTOR37_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR37_CPP)) : codegen/sector37.done ;
