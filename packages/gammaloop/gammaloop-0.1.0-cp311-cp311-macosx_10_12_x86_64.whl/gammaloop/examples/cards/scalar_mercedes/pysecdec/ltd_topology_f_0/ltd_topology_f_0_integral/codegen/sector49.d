SECTOR49_CPP = \
	src/sector_49.cpp \
	src/sector_49_0.cpp
SECTOR49_DISTSRC = \
	distsrc/sector_49_0.cpp \
	distsrc/sector_49_0.cu
SECTOR_CPP += $(SECTOR49_CPP)

$(SECTOR49_DISTSRC) $(SECTOR49_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR49_CPP)) : codegen/sector49.done ;
