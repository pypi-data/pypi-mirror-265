SECTOR2_CPP = \
	src/sector_2.cpp \
	src/sector_2_0.cpp
SECTOR2_DISTSRC = \
	distsrc/sector_2_0.cpp \
	distsrc/sector_2_0.cu
SECTOR_CPP += $(SECTOR2_CPP)

$(SECTOR2_DISTSRC) $(SECTOR2_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR2_CPP)) : codegen/sector2.done ;
