SECTOR53_CPP = \
	src/sector_53.cpp \
	src/sector_53_0.cpp
SECTOR53_DISTSRC = \
	distsrc/sector_53_0.cpp \
	distsrc/sector_53_0.cu
SECTOR_CPP += $(SECTOR53_CPP)

$(SECTOR53_DISTSRC) $(SECTOR53_CPP) $(patsubst %.cpp,%.hpp,$(SECTOR53_CPP)) : codegen/sector53.done ;
