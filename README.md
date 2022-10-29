# pyPiCode
Python C extension module to wrap the PiCode library.

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

The [**PiCode library**](http://github.com/latchdevel/PiCode) provides an easy way to handle the wireless protocols of weather stations and radio control switches using 433/315Mhz radio frequency in ASK/OOK modulation, which have been implemented by the [pilight project](https://manual.pilight.org/protocols/433.92/index.html)

The PiCode library is a standard C/C++ library, both static and dynamic, that works on any libc/libc++ compatible system, such as macOS, FreeBSD, Linux, and even Windows.

Using [SWIG](https://www.swig.org/), to generate the Python C extension source files that wraps PiCode's static C library:
- `picode_wrap.c`: CMake compiles the C source file, as does the PiCode library, and they link together to build the Python C extension module.
- `picode_wrap.py`: Python functions of the picode wrapper module are redefined to add basic docstrings and parameter checks in `__init__.py` package file.

## Install
Package installation builds the C extension module, so some OS tools are required like these packages on Debian-based Linux systems:
- Python3 development tools: `python3-dev`
- Python3 package installer: `python3-pip`
- C compiler suite: `build-essential`
- CMake make system: `cmake`
- Git version control system: `git`

Command to install from GitHub:
```
$ python3 -m pip install -v --user git+https://github.com/latchdevel/pyPiCode.git
```

## Tests
PyPiCode provides a unit tests module to verify its correct operation:
```
$ python3 -m unittest discover -v pypicode
```

## Usage
```python
>>> import pypicode as picode
>>>
>>> picode.decodeString("c:011010100101011010100110101001100110010101100110101010101010101012;p:1400,600,6800@")
{'protocols': [{'conrad_rsl_switch': {'id': 1, 'unit': 2, 'state': 'on'}}]}
>>>
```

## Functions:

+ **`decodePulseTrain(pulses_list: list)`**

    Decodes a list of pulses to a results dict.

    Returns a dict always, with a key "protocols" and a list of decoded protocols as its value,
    which will be empty if none are decoded, like as { 'protocols': [ ] }

+ **`decodeString(pilight_string: str)`**
  
    Decodes a string in pilight format to a results dict.

    Returns a dict with a key "protocols" and a list of decoded protocols as its value, or None on failure.

+ **`encodeJson(json: dict, repeats: int = 0)`**

    Encodes a full json dict to a string in pilight format.

    Returns a pilight string or None on failure.

+ **`encodeToPulseTrain(protocol, json_data: dict)`**

    Encodes a Swig Object of type 'protocol_t *' and a json data dict to a pulses list.

    Returns a pulses list or None on failure.

+ **`encodeToPulseTrainByName(protocol_name: str, json_data: dict)`**

    Encodes a protocol name string and a json data dict to a pulses list.

    Returns a pulses list or None on failure.

+ **`encodeToString(protocol_name: str, json_data: dict, repeats: int = 0)`**

    Encodes a protocol name string and a json data dict to a string in pilight format.

    Returns a pilight string or None on failure.

+ **`findProtocol(name: str)`**

    Find a protocol among all those initialized by name.

    Returns a Swig Object of type 'protocol_t *' or None on failure.

+ **`getPiCodeVersion()`**

    Get version of PiCode library.

    Returns the full version string of the PiCode library or None on failure.

+ **`pulseTrainToString(pulses_list: list, repeats: int = 0)`**

    Converts a list of pulses to a string in pilight format.

    Returns a pilight string or None on failure.

+ **`stringToPulseTrain(pilight_string: str)`**

    Converts a string in pilight format to a pulses lists.
    
    Returns a pulses list or None on failure.


# License
Copyright (c) 2021-2022 Jorge Rivera. All right reserved.

License GNU Lesser General Public License v3.0.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

See the [LICENSE](LICENSE) file for license rights and limitations (lgpl-3.0).