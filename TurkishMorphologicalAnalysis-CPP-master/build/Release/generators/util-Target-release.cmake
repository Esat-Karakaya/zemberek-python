# Avoid multiple calls to find_package to append duplicated properties to the targets
include_guard()########### VARIABLES #######################################################################
#############################################################################################
set(util_FRAMEWORKS_FOUND_RELEASE "") # Will be filled later
conan_find_apple_frameworks(util_FRAMEWORKS_FOUND_RELEASE "${util_FRAMEWORKS_RELEASE}" "${util_FRAMEWORK_DIRS_RELEASE}")

set(util_LIBRARIES_TARGETS "") # Will be filled later


######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
if(NOT TARGET util_DEPS_TARGET)
    add_library(util_DEPS_TARGET INTERFACE IMPORTED)
endif()

set_property(TARGET util_DEPS_TARGET
             APPEND PROPERTY INTERFACE_LINK_LIBRARIES
             $<$<CONFIG:Release>:${util_FRAMEWORKS_FOUND_RELEASE}>
             $<$<CONFIG:Release>:${util_SYSTEM_LIBS_RELEASE}>
             $<$<CONFIG:Release>:>)

####### Find the libraries declared in cpp_info.libs, create an IMPORTED target for each one and link the
####### util_DEPS_TARGET to all of them
conan_package_library_targets("${util_LIBS_RELEASE}"    # libraries
                              "${util_LIB_DIRS_RELEASE}" # package_libdir
                              "${util_BIN_DIRS_RELEASE}" # package_bindir
                              "${util_LIBRARY_TYPE_RELEASE}"
                              "${util_IS_HOST_WINDOWS_RELEASE}"
                              util_DEPS_TARGET
                              util_LIBRARIES_TARGETS  # out_libraries_targets
                              "_RELEASE"
                              "util"    # package_name
                              "${util_NO_SONAME_MODE_RELEASE}")  # soname

# FIXME: What is the result of this for multi-config? All configs adding themselves to path?
set(CMAKE_MODULE_PATH ${util_BUILD_DIRS_RELEASE} ${CMAKE_MODULE_PATH})

########## GLOBAL TARGET PROPERTIES Release ########################################
    set_property(TARGET util::util
                 APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                 $<$<CONFIG:Release>:${util_OBJECTS_RELEASE}>
                 $<$<CONFIG:Release>:${util_LIBRARIES_TARGETS}>
                 )

    if("${util_LIBS_RELEASE}" STREQUAL "")
        # If the package is not declaring any "cpp_info.libs" the package deps, system libs,
        # frameworks etc are not linked to the imported targets and we need to do it to the
        # global target
        set_property(TARGET util::util
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     util_DEPS_TARGET)
    endif()

    set_property(TARGET util::util
                 APPEND PROPERTY INTERFACE_LINK_OPTIONS
                 $<$<CONFIG:Release>:${util_LINKER_FLAGS_RELEASE}>)
    set_property(TARGET util::util
                 APPEND PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                 $<$<CONFIG:Release>:${util_INCLUDE_DIRS_RELEASE}>)
    # Necessary to find LINK shared libraries in Linux
    set_property(TARGET util::util
                 APPEND PROPERTY INTERFACE_LINK_DIRECTORIES
                 $<$<CONFIG:Release>:${util_LIB_DIRS_RELEASE}>)
    set_property(TARGET util::util
                 APPEND PROPERTY INTERFACE_COMPILE_DEFINITIONS
                 $<$<CONFIG:Release>:${util_COMPILE_DEFINITIONS_RELEASE}>)
    set_property(TARGET util::util
                 APPEND PROPERTY INTERFACE_COMPILE_OPTIONS
                 $<$<CONFIG:Release>:${util_COMPILE_OPTIONS_RELEASE}>)

########## For the modules (FindXXX)
set(util_LIBRARIES_RELEASE util::util)
