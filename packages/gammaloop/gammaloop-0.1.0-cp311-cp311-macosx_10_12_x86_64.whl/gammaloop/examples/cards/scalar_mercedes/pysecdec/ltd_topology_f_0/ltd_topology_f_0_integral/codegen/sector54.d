SECTOR54_CPP = \
	src/sector_54.cpp \
	src/sector_54_0.cpp
SECTOR54_DISTSRC = \
	distsrc/sector_54_0.cpp \
	distsrc/sector_54_0.cu
SECTOR_CPP += $(SECTOR54_CPP)

$(SECTOR54_DISTSRC) $(SECTOR54_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR54_CPP)) : codegen/sector54.done ;
