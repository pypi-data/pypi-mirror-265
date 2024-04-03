add_library(fdmss_lib
  ./src/Polynom.cpp
  ./src/Codegen.cpp
  ./src/MouseFuncX.cpp
  ./src/MouseFuncY.cpp
  ./src/MouseFuncZ.cpp
  ./src/CrtFuncX.cpp
  ./src/CrtFuncY.cpp
  ./src/CrtFuncZ.cpp
  ./src/Slau.cpp
  ./src/InputParameters.cpp
  ./src/StuffedVoxel.cpp
  ./src/EnvCaseGenerator.cpp
  ./src/OverdozenMicroperm.cpp
  ./src/PbcOverdozenMicroperm.cpp
  ./src/NfbcOverdozenMicroperm.cpp
  ./src/HorseBCOverdozenMicroperm.cpp
  ./src/FbcOverdozenMicroperm.cpp
  ./src/OverdozenPermsolver.cpp
  ./src/tinystr.cpp
  ./src/tinyxml.cpp
  ./src/tinyxmlparser.cpp
  ./src/tinyxmlerror.cpp
)
find_package(OpenMP REQUIRED)
target_include_directories(fdmss_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_options(fdmss_lib PUBLIC -fopenmp -fPIC)
target_link_libraries(fdmss_lib PUBLIC OpenMP::OpenMP_CXX)
