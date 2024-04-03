SECTOR50_CPP = \
	src/sector_50.cpp \
	src/sector_50_0.cpp
SECTOR50_DISTSRC = \
	distsrc/sector_50_0.cpp \
	distsrc/sector_50_0.cu
SECTOR_CPP += $(SECTOR50_CPP)

$(SECTOR50_DISTSRC) $(SECTOR50_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR50_CPP)) : codegen/sector50.done ;
