########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(dictionary_COMPONENT_NAMES "")
if(DEFINED dictionary_FIND_DEPENDENCY_NAMES)
  list(APPEND dictionary_FIND_DEPENDENCY_NAMES math util)
  list(REMOVE_DUPLICATES dictionary_FIND_DEPENDENCY_NAMES)
else()
  set(dictionary_FIND_DEPENDENCY_NAMES math util)
endif()
set(math_FIND_MODE "NO_MODULE")
set(util_FIND_MODE "NO_MODULE")

########### VARIABLES #######################################################################
#############################################################################################
set(dictionary_PACKAGE_FOLDER_RELEASE "/home/esat/.conan2/p/b/dictie420030821bcf/p")
set(dictionary_BUILD_MODULES_PATHS_RELEASE )


set(dictionary_INCLUDE_DIRS_RELEASE "${dictionary_PACKAGE_FOLDER_RELEASE}/include")
set(dictionary_RES_DIRS_RELEASE )
set(dictionary_DEFINITIONS_RELEASE )
set(dictionary_SHARED_LINK_FLAGS_RELEASE )
set(dictionary_EXE_LINK_FLAGS_RELEASE )
set(dictionary_OBJECTS_RELEASE )
set(dictionary_COMPILE_DEFINITIONS_RELEASE )
set(dictionary_COMPILE_OPTIONS_C_RELEASE )
set(dictionary_COMPILE_OPTIONS_CXX_RELEASE )
set(dictionary_LIB_DIRS_RELEASE "${dictionary_PACKAGE_FOLDER_RELEASE}/lib")
set(dictionary_BIN_DIRS_RELEASE )
set(dictionary_LIBRARY_TYPE_RELEASE STATIC)
set(dictionary_IS_HOST_WINDOWS_RELEASE 0)
set(dictionary_LIBS_RELEASE Dictionary)
set(dictionary_SYSTEM_LIBS_RELEASE )
set(dictionary_FRAMEWORK_DIRS_RELEASE )
set(dictionary_FRAMEWORKS_RELEASE )
set(dictionary_BUILD_DIRS_RELEASE )
set(dictionary_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(dictionary_COMPILE_OPTIONS_RELEASE
    "$<$<COMPILE_LANGUAGE:CXX>:${dictionary_COMPILE_OPTIONS_CXX_RELEASE}>"
    "$<$<COMPILE_LANGUAGE:C>:${dictionary_COMPILE_OPTIONS_C_RELEASE}>")
set(dictionary_LINKER_FLAGS_RELEASE
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${dictionary_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${dictionary_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${dictionary_EXE_LINK_FLAGS_RELEASE}>")


set(dictionary_COMPONENTS_RELEASE )