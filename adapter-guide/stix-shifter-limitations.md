# STIX-Shifter Limitations

##  Limitations on pattern length tranlsation

As the STIX pattern length increases, the translation time seems to increase exponentially. We also hit a the limitations on the python recursion limit due to the way the antlr parsing works. We have run test on our local machine different on pattern length to verify and show how the pattern trasnlattion time increases with the increase of the pattern lenght: 

**Test Machine Configuration:**

    OS : MAC
    OS Version: 11.0.1
    Processor: 2.6 GHz 6-Core Intel Core i7
    Memory: 16 GB 2400 MHz DDR4

|     Pattern Length              |   Recursion Limit    | Pattern Translation Time(seconds) |
| :-----------------------------: | :------------------: | :-------------------------------: |
|     500                         |   10000              |          45.61                    |
|     1000                        |   10000              |          154.24                   |
|     2000                        |   15000              |          859.97                   |
|     2000(Combined Observation)  |   20000              |          1078.52                  |
|     4000                        |   25000              |          4090.36                  |


**Note:** The value in the Recursion limit coloumn is the approximate minimum limit of python recursion to translate the pattern


