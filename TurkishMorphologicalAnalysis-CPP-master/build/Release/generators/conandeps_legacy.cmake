message(STATUS "Conan: Using CMakeDeps conandeps_legacy.cmake aggregator via include()")
message(STATUS "Conan: It is recommended to use explicit find_package() per dependency instead")

find_package(corpus)
find_package(xml_parser)
find_package(dictionary)
find_package(data_structure)
find_package(util)

set(CONANDEPS_LEGACY  corpus::corpus  xml_parser::xml_parser  dictionary::dictionary  data_structure::data_structure  util::util )