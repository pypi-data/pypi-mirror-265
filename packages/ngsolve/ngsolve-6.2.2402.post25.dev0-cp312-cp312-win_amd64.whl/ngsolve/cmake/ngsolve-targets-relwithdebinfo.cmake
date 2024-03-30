#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ngsolve" for configuration "RelWithDebInfo"
set_property(TARGET ngsolve APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(ngsolve PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/netgen/lib/libngsolve.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/netgen/libngsolve.dll"
  )

list(APPEND _cmake_import_check_targets ngsolve )
list(APPEND _cmake_import_check_files_for_ngsolve "${_IMPORT_PREFIX}/netgen/lib/libngsolve.lib" "${_IMPORT_PREFIX}/netgen/libngsolve.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
