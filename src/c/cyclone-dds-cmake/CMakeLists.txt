cmake_minimum_required(VERSION 3.16)
project(shape LANGUAGES C)

# Find the CycloneDDS package.
find_package(CycloneDDS REQUIRED)
set(EXECUTABLE_NAME "eclipse_cyclone-${CycloneDDS_VERSION}_linux")

add_executable(${EXECUTABLE_NAME} ../test_main.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/domtree.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/domtree.h
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/type_cache.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/type_cache.h
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/print_sample.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/print_sample.h
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/print_type.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/print_type.h
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/compare_samples.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/compare_samples.h
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/scan_sample.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/scan_sample.h
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/xmltype.c
    ~/eboasson-cyclonedds/install/share/CycloneDDS/examples/dynsub/xmltype.h
    )

target_compile_definitions(${EXECUTABLE_NAME} PUBLIC -DCYCLONE_DDS)

target_link_libraries(${EXECUTABLE_NAME} CycloneDDS::ddsc m)
