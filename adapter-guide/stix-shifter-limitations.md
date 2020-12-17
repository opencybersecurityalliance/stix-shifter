# STIX-Shifter Limitations

##  Length limitations on STIX pattern translation

Pattern length refers to the number of comparison operations used in the STIX pattern. These can be operators either in an observation expression or separating multiple observation expressions. As the pattern length increases, the translation time increases exponentially due to how ANTLR 4 recursively parses the pattern. Python recursion limits can be exceeded for the same reason; when this happens, stix-shifter will throw an error (`RecursionError: maximum recursion depth exceeded`). The following tests were run on a local machine using different pattern lengths to show these limitations:

**Test Machine Configuration:**

    OS : MAC
    OS Version: 11.0.1
    Processor: 2.6 GHz 6-Core Intel Core i7
    Memory: 16 GB 2400 MHz DDR4

|     Pattern Length (operators)            |   Python Recursion Limit    | Pattern Translation Time (seconds) |
| :-----------------------------: | :------------------: | :-------------------------------: |
|     500                         |   10000              |          45.61                    |
|     1000                        |   10000              |          154.24                   |
|     2000                        |   15000              |          859.97                   |
|     2000 (Combined Observation)  |   20000              |          1078.52                  |
|     4000                        |   25000              |          4090.36                  |




