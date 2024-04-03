cmake_minimum_required(VERSION 3.14)
project(
  pyfdmss
  VERSION 0.0.3
  LANGUAGES CXX)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_UNITY_BUILD ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(src)

find_package(Python COMPONENTS Interpreter Development)
add_library(pyfdmss SHARED ./src/pyfdmss/pyfdmss.cpp)
target_include_directories(pyfdmss PUBLIC ${Python_INCLUDE_DIRS})
target_link_libraries(pyfdmss PUBLIC ${Python_LIBRARIES} fdmss_lib)
target_compile_options(pyfdmss PUBLIC -fPIC)
set_target_properties(
  pyfdmss
  PROPERTIES PREFIX ""
             OUTPUT_NAME "pyfdmss"
             LANGUAGE CXX
             LINKER_LANGUAGE CXX)



