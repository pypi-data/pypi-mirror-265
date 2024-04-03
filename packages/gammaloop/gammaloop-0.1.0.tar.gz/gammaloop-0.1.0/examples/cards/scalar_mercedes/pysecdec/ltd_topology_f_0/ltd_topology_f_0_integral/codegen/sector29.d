SECTOR29_CPP = \
	src/sector_29.cpp \
	src/sector_29_0.cpp
SECTOR29_DISTSRC = \
	distsrc/sector_29_0.cpp \
	distsrc/sector_29_0.cu
SECTOR_CPP += $(SECTOR29_CPP)

$(SECTOR29_DISTSRC) $(SECTOR29_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR29_CPP)) : codegen/sector29.done ;
