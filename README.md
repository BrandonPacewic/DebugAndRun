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

This script will also open the .cc file that you intend to run and will replace

```shell
//dbg
```

With

```cpp
#define DBG_MODE
```

This is mostly used for competitive programming as you only want your debug functions to run

If you are testing the program localy this prevents the program validater from failing your program due to 
debug function calls that you forgot to remove

##### Example

```cpp
#include <iostream>
using namespace std;

//dbg
void DBG_OUT() { cerr << endl; }
template<typename Front, typename... Back> void DBG_OUT(Front K, Back... T) { cerr << ' ' << K; DBG_OUT(T...); }
#ifdef DBG_MODE
#define testArgs(...) cerr << '(' << #__VA_ARGS__ << "):", DBG_OUT(__VA_ARGS__)
#else
#define testArgs(...)
#endif


int main() {
    int A, B;
    cin >> A >> B;

    testArgs(A - B, A * B);

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

If you want to look more at my debug template for competitive programming that can be found [Here](https://github.com/BrandonPacewic/CompetitiveProgramming/blob/master/tools/dbg.hpp)

At the moment this does mean that the script checks every line to see if it needs to define the dbg macro but a feature to disable this with sys.args is to be added in newer versions

### Install

----

For your convinence there is a install script that will make the global command for you

```shell
chmod +x INSTALL.sh
sudo ./INSTALL.sh
```

Enjoy :)