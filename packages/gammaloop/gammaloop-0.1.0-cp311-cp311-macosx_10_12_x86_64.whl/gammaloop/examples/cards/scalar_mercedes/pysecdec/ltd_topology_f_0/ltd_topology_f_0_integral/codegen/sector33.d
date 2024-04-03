SECTOR33_CPP = \
	src/sector_33.cpp \
	src/sector_33_0.cpp
SECTOR33_DISTSRC = \
	distsrc/sector_33_0.cpp \
	distsrc/sector_33_0.cu
SECTOR_CPP += $(SECTOR33_CPP)

$(SECTOR33_DISTSRC) $(SECTOR33_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR33_CPP)) : codegen/sector33.done ;
