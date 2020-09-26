cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(shot_esf_compute)

find_package(PCL 1.7 REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})

link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable (shotA_compute shotA_compute.cpp)
target_link_libraries (shotA_compute ${PCL_LIBRARIES})
target_link_libraries (shotA_compute ${PCL_COMMONLIBRARIES})
target_link_libraries (shotA_compute ${PCL_VISUALIZATION_LIBRARIES})

add_executable (shotC_compute shotC_compute.cpp)
target_link_libraries (shotC_compute ${PCL_LIBRARIES})
target_link_libraries (shotC_compute ${PCL_COMMONLIBRARIES})
target_link_libraries (shotC_compute ${PCL_VISUALIZATION_LIBRARIES})

add_executable (esf_compute esf_compute.cpp)
target_link_libraries (esf_compute ${PCL_LIBRARIES})
target_link_libraries (esf_compute ${PCL_COMMONLIBRARIES})
target_link_libraries (esf_compute ${PCL_VISUALIZATION_LIBRARIES})
