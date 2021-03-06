# Debug And Run

----

A linux python script for compiling and executing .cc files 

##### Example

```shell
dbrun <fname>.cc
```

```shell 
[DEBUG MODE] Compiling <fname>.cc with C++17
--------------------

<sample program output>

```


The script can also be used by providing an input and output file for the program

##### Example

```shell
dbrun <fname>.cc / <sample input file>.txt / <sample output file>.txt
```

```shell
[DEBUG MODE] Compiling <fname>.cc with C++17
[INPUT FILE] Selected Input File is <sample input file>.txt
[OUTPUT FILE] Selected Output File is <sample output file>.txt
--------------------
[SUCCESS] Write lines to file <sample output file>.txt successful
```

A output file is not always required as the script will print the program output if no 
output file is provided

For this version a input file is needed to make an output file

### Define DBG_MODE

----

This script will also define the macro 'DBG_MODE'

This is mostly used for competitive programming as you only want your debug functions to run
if you are testing the program localy this prevents the program validater from failing your program due to 
debug function calls that you forgot to remove

##### Example

```cpp
#include <iostream>
using namespace std;

//dbg
void DBG_OUT() { cerr << endl; }
template<typename Front, typename... Back> void DBG_OUT(Front K, Back... T) { cerr << ' ' << K; DBG_OUT(T...); }
#ifdef DBG_MODE
#define test(...) cerr << '(' << #__VA_ARGS__ << "):", DBG_OUT(__VA_ARGS__)
#else
#define test(...)
#endif


int main() {
    int A, B;
    cin >> A >> B;

    test(A - B, A * B);

    cout << A + B << '\n';
    cout << flush;
}
```

##### Input

```
5 2
```

##### Output

Without defining DBG_MODE

```
7
```

With defining DBG_MODE

```
(A - B, A * B): 3 10
7
```

If you want to look more at my debug template for competitive programming that can be found [Here](https://github.com/BrandonPacewic/CompetitiveProgramming/blob/master/tools)

At the moment this does mean that there is no way to turn this off however an option for this will be added in the future using argparse

### Install

----

For your convinence there is a install script that will make the global command for you

```shell
sudo ./INSTALL.sh
```

Enjoy :)