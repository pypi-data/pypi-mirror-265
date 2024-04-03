SECTOR21_CPP = \
	src/sector_21.cpp \
	src/sector_21_0.cpp
SECTOR21_DISTSRC = \
	distsrc/sector_21_0.cpp \
	distsrc/sector_21_0.cu
SECTOR_CPP += $(SECTOR21_CPP)

$(SECTOR21_DISTSRC) $(SECTOR21_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR21_CPP)) : codegen/sector21.done ;
