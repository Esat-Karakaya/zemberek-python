########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(util_COMPONENT_NAMES "")
if(DEFINED util_FIND_DEPENDENCY_NAMES)
  list(APPEND util_FIND_DEPENDENCY_NAMES )
  list(REMOVE_DUPLICATES util_FIND_DEPENDENCY_NAMES)
else()
  set(util_FIND_DEPENDENCY_NAMES )
endif()

########### VARIABLES #######################################################################
#############################################################################################
set(util_PACKAGE_FOLDER_RELEASE "/home/esat/.conan2/p/b/util51844fb9664e4/p")
set(util_BUILD_MODULES_PATHS_RELEASE )


set(util_INCLUDE_DIRS_RELEASE "${util_PACKAGE_FOLDER_RELEASE}/include")
set(util_RES_DIRS_RELEASE )
set(util_DEFINITIONS_RELEASE )
set(util_SHARED_LINK_FLAGS_RELEASE )
set(util_EXE_LINK_FLAGS_RELEASE )
set(util_OBJECTS_RELEASE )
set(util_COMPILE_DEFINITIONS_RELEASE )
set(util_COMPILE_OPTIONS_C_RELEASE )
set(util_COMPILE_OPTIONS_CXX_RELEASE )
set(util_LIB_DIRS_RELEASE "${util_PACKAGE_FOLDER_RELEASE}/lib")
set(util_BIN_DIRS_RELEASE )
set(util_LIBRARY_TYPE_RELEASE STATIC)
set(util_IS_HOST_WINDOWS_RELEASE 0)
set(util_LIBS_RELEASE Util)
set(util_SYSTEM_LIBS_RELEASE )
set(util_FRAMEWORK_DIRS_RELEASE )
set(util_FRAMEWORKS_RELEASE )
set(util_BUILD_DIRS_RELEASE )
set(util_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(util_COMPILE_OPTIONS_RELEASE
    "$<$<COMPILE_LANGUAGE:CXX>:${util_COMPILE_OPTIONS_CXX_RELEASE}>"
    "$<$<COMPILE_LANGUAGE:C>:${util_COMPILE_OPTIONS_C_RELEASE}>")
set(util_LINKER_FLAGS_RELEASE
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>:${util_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>:${util_SHARED_LINK_FLAGS_RELEASE}>"
    "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${util_EXE_LINK_FLAGS_RELEASE}>")


set(util_COMPONENTS_RELEASE )