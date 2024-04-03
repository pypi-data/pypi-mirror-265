SECTOR18_CPP = \
	src/sector_18.cpp \
	src/sector_18_0.cpp
SECTOR18_DISTSRC = \
	distsrc/sector_18_0.cpp \
	distsrc/sector_18_0.cu
SECTOR_CPP += $(SECTOR18_CPP)

$(SECTOR18_DISTSRC) $(SECTOR18_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR18_CPP)) : codegen/sector18.done ;
