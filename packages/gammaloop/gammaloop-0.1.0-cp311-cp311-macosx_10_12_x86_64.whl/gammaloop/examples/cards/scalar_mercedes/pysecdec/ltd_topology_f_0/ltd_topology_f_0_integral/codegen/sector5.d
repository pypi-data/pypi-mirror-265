SECTOR5_CPP = \
	src/sector_5.cpp \
	src/sector_5_0.cpp
SECTOR5_DISTSRC = \
	distsrc/sector_5_0.cpp \
	distsrc/sector_5_0.cu
SECTOR_CPP += $(SECTOR5_CPP)

$(SECTOR5_DISTSRC) $(SECTOR5_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR5_CPP)) : codegen/sector5.done ;
