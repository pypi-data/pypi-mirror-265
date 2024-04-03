SECTOR45_CPP = \
	src/sector_45.cpp \
	src/sector_45_0.cpp
SECTOR45_DISTSRC = \
	distsrc/sector_45_0.cpp \
	distsrc/sector_45_0.cu
SECTOR_CPP += $(SECTOR45_CPP)

$(SECTOR45_DISTSRC) $(SECTOR45_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR45_CPP)) : codegen/sector45.done ;
