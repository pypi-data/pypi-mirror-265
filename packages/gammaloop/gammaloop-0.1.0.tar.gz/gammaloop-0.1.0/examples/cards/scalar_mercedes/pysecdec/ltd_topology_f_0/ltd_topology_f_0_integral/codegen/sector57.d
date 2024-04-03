SECTOR57_CPP = \
	src/sector_57.cpp \
	src/sector_57_0.cpp
SECTOR57_DISTSRC = \
	distsrc/sector_57_0.cpp \
	distsrc/sector_57_0.cu
SECTOR_CPP += $(SECTOR57_CPP)

$(SECTOR57_DISTSRC) $(SECTOR57_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR57_CPP)) : codegen/sector57.done ;
