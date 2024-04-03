SECTOR22_CPP = \
	src/sector_22.cpp \
	src/sector_22_0.cpp
SECTOR22_DISTSRC = \
	distsrc/sector_22_0.cpp \
	distsrc/sector_22_0.cu
SECTOR_CPP += $(SECTOR22_CPP)

$(SECTOR22_DISTSRC) $(SECTOR22_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR22_CPP)) : codegen/sector22.done ;
