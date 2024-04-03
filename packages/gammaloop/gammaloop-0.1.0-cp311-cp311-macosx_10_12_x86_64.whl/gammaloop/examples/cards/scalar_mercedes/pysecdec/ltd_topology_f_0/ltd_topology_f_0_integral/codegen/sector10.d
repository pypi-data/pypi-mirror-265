SECTOR10_CPP = \
	src/sector_10.cpp \
	src/sector_10_0.cpp
SECTOR10_DISTSRC = \
	distsrc/sector_10_0.cpp \
	distsrc/sector_10_0.cu
SECTOR_CPP += $(SECTOR10_CPP)

$(SECTOR10_DISTSRC) $(SECTOR10_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR10_CPP)) : codegen/sector10.done ;
