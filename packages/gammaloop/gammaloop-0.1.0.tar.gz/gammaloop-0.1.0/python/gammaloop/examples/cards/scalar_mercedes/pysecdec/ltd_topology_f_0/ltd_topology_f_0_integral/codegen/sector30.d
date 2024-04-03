SECTOR30_CPP = \
	src/sector_30.cpp \
	src/sector_30_0.cpp
SECTOR30_DISTSRC = \
	distsrc/sector_30_0.cpp \
	distsrc/sector_30_0.cu
SECTOR_CPP += $(SECTOR30_CPP)

$(SECTOR30_DISTSRC) $(SECTOR30_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR30_CPP)) : codegen/sector30.done ;
