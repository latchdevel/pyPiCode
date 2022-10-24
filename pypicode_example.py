#!/usr/bin/env python3
"""
Example of using 'pypicode'
Python C extension module to wrap the PiCode library

See: https://github.com/latchdevel/pyPiCode

Copyright (c) 2022 Jorge Rivera. All right reserved.
License GNU Lesser General Public License v3.0.
"""

import sys, json
import pypicode as picode

if __name__ == "__main__":

    result = 0 # no error

    print("pypicode_example")

    # Get PiCode library version

    library_version = picode.getPiCodeVersion()

    if (library_version):
        print("PiCode library version: %s" % library_version)
    else:
        print("ERROR: Unable to get PiCode library version.")
        result|=(1 << 0) # error mask 0b00000001

    print("")

    # Decode from pilight string

    pilight_string = "c:011010100101011010100110101001100110010101100110101010101010101012;p:1400,600,6800@"

    decoded_string = picode.decodeString(pilight_string)

    print("String to decode: \"%s\"" % pilight_string)

    if (decoded_string):

        print("Decode string successful:")
        print(json.dumps(decoded_string,indent=4))
         
    else:
        print("ERROR: Unable to decode string.")
        result|=(1 << 1) # error mask 0b00000010

    print("")

    # Encode to pilight string from json dict
   
    json_dict = { 'arctech_switch' : { 'id': 92, 'unit': 0, 'on': 1 }}
    repeats = 5

    encoded_json_string = picode.encodeJson(json_dict,repeats)

    print("JSON to encode: \"%s\"" % json_dict)

    if (encoded_json_string):

        print("Encode successful:")
        print("%s" % encoded_json_string)
    
    else:
        print("ERROR: Unable to encode JSON.")
        result|=(1 << 2) # error mask 0b00000100

    print("")

    # Encode from protocol name and json data to array of pulses if success
    
    protocol_name = "arctech_switch"
    json_data_dict = {'id': 92, 'unit': 0, 'on': 1}

    print("Encode protocol: \"%s\" JSON data: \"%s\"" % (protocol_name,json_data_dict))

    pulses = picode.encodeToPulseTrainByName(protocol_name, json_data_dict)

    if isinstance(pulses,list):
        print("Encode successful:")
        print("pulses(%d)=%s" % (len(pulses),pulses))
    else:
        print("ERROR: Unable to encode.")
        result|=(1 << 3) # error mask 0b00001000

    print("")
    sys.exit(result)
