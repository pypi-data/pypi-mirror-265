SECTOR1_CPP = \
	src/sector_1.cpp \
	src/sector_1_0.cpp
SECTOR1_DISTSRC = \
	distsrc/sector_1_0.cpp \
	distsrc/sector_1_0.cu
SECTOR_CPP += $(SECTOR1_CPP)

$(SECTOR1_DISTSRC) $(SECTOR1_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR1_CPP)) : codegen/sector1.done ;
