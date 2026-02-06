########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(corpus_COMPONENT_NAMES "")
if(DEFINED corpus_FIND_DEPENDENCY_NAMES)
  list(APPEND corpus_FIND_DEPENDENCY_NAMES dictionary data_structure util)
  list(REMOVE_DUPLICATES corpus_FIND_DEPENDENCY_NAMES)
else()
  set(corpus_FIND_DEPENDENCY_NAMES dictionary data_structure util)
endif()
set(dictionary_FIND_MODE "NO_MODULE")
set(data_structure_FIND_MODE "NO_MODULE")
set(util_FIND_MODE "NO_MODULE")

########### VARIABLES #######################################################################
#############################################################################################
set(corpus_PACKAGE_FOLDER_RELEASE "/home/esat/.conan2/p/b/corpue9e8f596bda6a/p")
set(corpus_BUILD_MODULES_PATHS_RELEASE )


set(corpus_INCLUDE_DIRS_RELEASE "${corpus_PACKAGE_FOLDER_RELEASE}/include")
set(corpus_RES_DIRS_RELEASE )
set(corpus_DEFINITIONS_RELEASE )
set(corpus_SHARED_LINK_FLAGS_RELEASE )
set(corpus_EXE_LINK_FLAGS_RELEASE )
set(corpus_OBJECTS_RELEASE )
set(corpus_COMPILE_DEFINITIONS_RELEASE )
set(corpus_COMPILE_OPTIONS_C_RELEASE )
set(corpus_COMPILE_OPTIONS_CXX_RELEASE )
set(corpus_LIB_DIRS_RELEASE "${corpus_PACKAGE_FOLDER_RELEASE}/lib")
set(corpus_BIN_DIRS_RELEASE )
set(corpus_LIBRARY_TYPE_RELEASE STATIC)
set(corpus_IS_HOST_WINDOWS_RELEASE 0)
set(corpus_LIBS_RELEASE Corpus)
set(corpus_SYSTEM_LIBS_RELEASE )
set(corpus_FRAMEWORK_DIRS_RELEASE )
set(corpus_FRAMEWORKS_RELEASE )
set(corpus_BUILD_DIRS_RELEASE )
set(corpus_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(corpus_COMPILE_OPTIONS_RELEASE
    "$<$<COMPILE_LANGUAGE:CXX>:${corpus_COMPILE_OPTIONS_CXX_RELEASE}>"
    "$<$<COMPILE_LANGUAGE:C>:${corpus_COMPILE_OPTIONS_C_RELEASE}>")
set(corpus_LINKER_FLAGS_RELEASE
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${corpus_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${corpus_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${corpus_EXE_LINK_FLAGS_RELEASE}>")


set(corpus_COMPONENTS_RELEASE )