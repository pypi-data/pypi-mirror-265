SECTOR6_CPP = \
	src/sector_6.cpp \
	src/sector_6_0.cpp
SECTOR6_DISTSRC = \
	distsrc/sector_6_0.cpp \
	distsrc/sector_6_0.cu
SECTOR_CPP += $(SECTOR6_CPP)

$(SECTOR6_DISTSRC) $(SECTOR6_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR6_CPP)) : codegen/sector6.done ;
