"""
Python C extension module to wrap the PiCode library.

The PiCode library provides an easy way to handle the wireless protocols of 
weather stations and radio control switches using 433/315Mhz radio frequency 
in ASK/OOK modulation, which have been implemented by the 'pilight' project.

See: https://github.com/latchdevel/pyPiCode

Copyright (c) 2022 Jorge Rivera. All right reserved.
License GNU Lesser General Public License v3.0.
"""

from ast  import literal_eval
from copy import deepcopy
from re   import sub

# Import picode wrapper module as private module
from pypicode import picode_wrap as _picode_wraper

# Remove picode wrapper module from namespace
if 'picode_wrap' in dir():
    del picode_wrap

# Redefine Python functions from picode wrapper module
# Added parameter checks and basic docstrings

def getPiCodeVersion():
    """Get version of PiCode library. 
    Returns the full version string of the PiCode library or None on failure.
    """

    version = _picode_wraper.getPiCodeVersion()

    if isinstance(version,str):
        return version
    else:
        return None

def findProtocol(name:str):
    """Find a protocol among all those initialized by name. 
    Returns a Swig Object of type 'protocol_t *' or None on failure.
    """

    if (not isinstance(name,str)):
        raise TypeError("in method 'findProtocol', argument 1 'name' must be a string.")

    result = _picode_wraper.findProtocol(name)

    if type(result).__name__ == 'SwigPyObject':
        return result
    else:
        return None


def pulseTrainToString(pulses_list:list, repeats:int=0):
    """Converts a list of pulses to a string in pilight format.
    Returns a pilight string or None on failure.
    """

    if (not isinstance(pulses_list,list)):
        raise TypeError("in method 'pulseTrainToString', argument 1 'pulses_list' must be a list.")

    if (not isinstance(repeats,int)):
        raise TypeError("in method 'pulseTrainToString', argument 2 'repeats' must be an integer.")

    if (repeats < 0 or repeats > 255):
        raise TypeError("in method 'pulseTrainToString', argument 2 'repeats' must be in range from 0 to 255.")

    # Define a C type array of unit32_t
    pulses = _picode_wraper.uint32Array(len(pulses_list))

    # Populate C type array from python list
    for i in range(len(pulses_list)):
        pulses[i]=abs(int(pulses_list[i]))

    # Call wrapped C function to convert an array of pulses to pilight string format
    result = _picode_wraper.pulseTrainToString(pulses.cast(), len(pulses_list), repeats)

    # Free pulses C type array
    pulses.__swig_destroy__(pulses)

    if isinstance(result,str):
        return result
    else:
        return None


def encodeToPulseTrain(protocol, json_data:dict):
    """Encodes a Swig Object of type 'protocol_t *' and a json data dict to a pulses list. 
    Returns a pulses list or None on failure.
    """
    
    if not type(protocol).__name__ == 'SwigPyObject':
        raise TypeError("in method 'encodeToPulseTrain', argument 1 'protocol' must be a Swig Object of type 'protocol_t *'.")

    if (not isinstance(json_data,dict)):
        raise TypeError("in method 'encodeToPulseTrain', argument 2 'json_data' must be a dict.")

    # Define a C array type of unit32_t
    pulses = _picode_wraper.uint32Array(_picode_wraper.protocol_maxrawlen())

    # Make a deep copy of json_data dict to change it to support a dict out as dict in
    json_data_copy = deepcopy(json_data)

    if len(json_data_copy) > 0:
        if 'state' in json_data_copy:
            if json_data_copy['state'] == 'on':
                json_data_copy['on']=1
                del json_data_copy['state']
            elif json_data_copy['state'] == 'off':
                json_data_copy['off']=1
                del json_data_copy['state']

    # Call wrapped C function to encode from protocol and json data to array of pulses
    result_code = _picode_wraper.encodeToPulseTrain(pulses.cast(), _picode_wraper.protocol_maxrawlen(), protocol, str(json_data_copy))

    # If success, populate a python list from C type array of pulses
    if result_code > 0:
        result = [ pulses[i] for i in range(result_code) ]
    else:
        result = None

    # Free pulses C type array
    pulses.__swig_destroy__(pulses)

    return result


def encodeToPulseTrainByName(protocol_name:str, json_data:dict):
    """Encodes a protocol name string and a json data dict to a pulses list. 
    Returns a pulses list or None on failure.
    """

    if (not isinstance(protocol_name,str)):
        raise TypeError("in method 'encodeToPulseTrainByName', argument 1 'protocol_name' must be a string.")

    if (not isinstance(json_data,dict)):
        raise TypeError("in method 'encodeToPulseTrainByName', argument 2 'json_data' must be a dict.")

    # Define a C array type of unit32_t
    pulses = _picode_wraper.uint32Array(_picode_wraper.protocol_maxrawlen())

    # Make a deep copy of json_data dict to change it to support a dict out as dict in
    json_data_copy = deepcopy(json_data)

    if len(json_data_copy) > 0:
        if 'state' in json_data_copy:
            if json_data_copy['state'] == 'on':
                json_data_copy['on']=1
                del json_data_copy['state']
            elif json_data_copy['state'] == 'off':
                json_data_copy['off']=1
                del json_data_copy['state']

   # Call wrapped C function to encode from protocol name and json data to array of pulses
    result_code = _picode_wraper.encodeToPulseTrainByName(pulses.cast(), _picode_wraper.protocol_maxrawlen(), protocol_name, str(json_data_copy))    

    # If success, populate a python list from C type array of pulses
    if result_code > 0:
        result = [ pulses[i] for i in range(result_code) ]
    else:
        result = None

    # Free pulses C type array
    pulses.__swig_destroy__(pulses)

    return result


def stringToPulseTrain(pilight_string:str):
    """Converts a string in pilight format to a pulses lists. 
    Returns a pulses list or None on failure.
    """

    if (not isinstance(pilight_string,str)):
        raise TypeError("in method 'stringToPulseTrain', argument 1 'pilight_string' must be a string.")

    # Define a C array type of unit32_t
    pulses = _picode_wraper.uint32Array(_picode_wraper.protocol_maxrawlen())

    # Call wrapped C function to convert from pilight string to array of pulses
    result_code = _picode_wraper.stringToPulseTrain(pilight_string, pulses.cast(), _picode_wraper.protocol_maxrawlen())

    # If success, populate a python list from C type array of pulses
    if result_code > 0:
        result = [ pulses[i] for i in range(result_code) ]
    else:
        result = None

    # Free pulses C type array
    pulses.__swig_destroy__(pulses)

    return result


def decodePulseTrain(pulses_list:list):
    """Decodes a list of pulses to a results dict.
    Returns a dict always, with a key "protocols" and a list of decoded protocols as its value, 
    which will be empty if none are decoded, like as { 'protocols': [ ] }
    """

    if ( not isinstance(pulses_list,list) ):
        raise TypeError("in method 'decodePulseTrain', argument 1 'pulses_list' must be a list.")

    pulses = _picode_wraper.uint32Array(len(pulses_list))

    for i in range(len(pulses_list)):
        pulses[i]=pulses_list[i]

    result = literal_eval(_picode_wraper.decodePulseTrain(pulses.cast(), len(pulses_list), ""))

    pulses.__swig_destroy__(pulses)

    if isinstance(result,dict):
        return result
    else:
        return dict()


def decodeString(pilight_string:str):
    """Decodes a string in pilight format to a results dict. 
    Returns a dict with a key "protocols" and a list of decoded protocols as its value, 
    or None on failure.
    """

    if (not isinstance(pilight_string,str)):
        raise TypeError("in method 'decodeString', argument 1 'pilight_string' must be a string.")

    decoded_protocols = _picode_wraper.decodeString(pilight_string)

    if (isinstance(decoded_protocols,str)):
        decoded_protocols = sub("\n\ *","",decoded_protocols)
        result = literal_eval(decoded_protocols)
        if not isinstance(result,dict):
            result = None
    else:
        result = None

    return result


def encodeToString(protocol_name:str, json_data:dict, repeats:int=0):
    """Encodes a protocol name string and a json data dict to a string in pilight format. 
    Returns a pilight string or None on failure.
    """

    if (not isinstance(protocol_name,str)):
        raise TypeError("in method 'encodeToString', argument 1 'protocol_name' must be a string.")

    if (not isinstance(json_data,dict)):
        raise TypeError("in method 'encodeToString', argument 2 'json_data' must be a dict.")

    if (not isinstance(repeats,int)):
        raise TypeError("in method 'encodeToString', argument 3 'repeats' must be an integer.")

    if (repeats < 0 or repeats > 255):
        raise TypeError("in method 'encodeToString', argument 3 'repeats' must be in range from 0 to 255.")

    # Make a deep copy of json_data dict to change it to support a dict out as dict in
    json_data_copy = deepcopy(json_data)

    if len(json_data_copy) > 0:
        if 'state' in json_data_copy:
            if json_data_copy['state'] == 'on':
                json_data_copy['on']=1
                del json_data_copy['state']
            elif json_data_copy['state'] == 'off':
                json_data_copy['off']=1
                del json_data_copy['state']

    result = _picode_wraper.encodeToString(protocol_name, str(json_data_copy), repeats)

    if isinstance(result,str):
        return result
    else:
        return None


def encodeJson(json:dict, repeats:int=0):
    """Encodes a full json dict to a string in pilight format.
    Returns a pilight string or None on failure.
    """

    if (not isinstance(json,dict)):
        raise TypeError("in method 'encodeJson', argument 1 'json' must be a dict.")

    if (not isinstance(repeats,int)):
        raise TypeError("in method 'encodeJson', argument 2 'repeats' must be an integer.")

    if (repeats < 0 or repeats > 255):
        raise TypeError("in method 'encodeJson', argument 2 'repeats' must be in range from 0 to 255.")

    # Make a deep copy of json dict to change it to support a dict out as dict in
    json_copy = deepcopy(json)

    if len(json_copy) > 0:
        if 'state' in json_copy[list(json_copy.keys())[0]]:
            if json_copy[list(json_copy.keys())[0]]['state'] == 'on':
                json_copy[list(json_copy.keys())[0]]['on']=1
                del json_copy[list(json_copy.keys())[0]]['state']
            elif json_copy[list(json_copy.keys())[0]]['state'] == 'off':
                json_copy[list(json_copy.keys())[0]]['off']=1
                del json_copy[list(json_copy.keys())[0]]['state']

    result = _picode_wraper.encodeJson(str(json_copy), repeats)

    if isinstance(result,str):
        return result
    else:
        return None
