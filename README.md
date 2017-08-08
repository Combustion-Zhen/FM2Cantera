A convertor from FlameMaster solution to Cantera form, to be used as input for the flameletFoam

Compilation:
    make

Usage:
    1. Put FlameMaster solution in a folder, say <FMdata>, flamelet solution file has the original name such as CH4_p01_0chi00.01_tf0291to0294
    2. Run the script list_chi.sh to generate input for the FM2Cantera. Two parameters are required, e.g. the parts of flamelet solution file name before and after the value of scalar dissipation rate. The command looks like ./list_chi.sh <FMdata>/CH4_p01_0chi tf0291to0294
    3. Run the program, one parameter is required. It is a value of scalar dissipatio rate, used to extract the Z_parameter.include. The command looks like ./FM2Cantera 10
