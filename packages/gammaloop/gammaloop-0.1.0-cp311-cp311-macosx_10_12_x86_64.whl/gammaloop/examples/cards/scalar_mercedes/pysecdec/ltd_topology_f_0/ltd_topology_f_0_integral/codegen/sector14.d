SECTOR14_CPP = \
	src/sector_14.cpp \
	src/sector_14_0.cpp
SECTOR14_DISTSRC = \
	distsrc/sector_14_0.cpp \
	distsrc/sector_14_0.cu
SECTOR_CPP += $(SECTOR14_CPP)

$(SECTOR14_DISTSRC) $(SECTOR14_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR14_CPP)) : codegen/sector14.done ;
