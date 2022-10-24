/*
    pyPiCode
    Python C extension module to wrap the PiCode library

    See: https://github.com/latchdevel/pyPiCode

    Command: `swig -python -o picode_wrap.c -outdir pypicode picode_wrap.i`

    Source file:
        picode_wrap.i
    
    Generated files:
        picode_wrap.c
        pypicode/picode_wrap.py

    Copyright (c) 2022 Jorge Rivera. All right reserved.
    License GNU Lesser General Public License v3.0.

*/

// 'split module' configuration be supported with a simple customization
// [Python] #848 #1343 See: https://github.com/swig/swig/issues/2260
%module(package="pypicode", moduleimport="import $module") picode_wrap

%include <stdint.i>

// This module defines macros that assist in wrapping ordinary C pointers as arrays.
// Note: %array_functions() and %array_class() should not be used with types of char or char *.
// See: https://www.swig.org/Doc3.0/Library.html#Library_carrays
%include <carrays.i>

%array_class(uint32_t, uint32Array)

%{
// Pure C library to manage OOK protocols supported by "pilight" project.
// See: https://github.com/latchdevel/PiCode
#include "libs/PiCode/src/cPiCode.h"
%} 

/* Find protocol by name */
protocol_t* findProtocol(const char* name);

/* Convert pulses and length to pilight string format. Must be free() after use */
char* pulseTrainToString(const uint32_t* pulses, uint16_t maxlength, uint8_t repeats);

/* Encode protocol and json data to array of pulses if success */
int encodeToPulseTrain(uint32_t* pulses, uint16_t maxlength, protocol_t* protocol, const char* json_data);

/* Encode from protocol name and json data to array of pulses if success */
int encodeToPulseTrainByName(uint32_t* pulses, uint16_t maxlength, const char* protocol_name, const char* json_data);

/* Convert from pilight string to array of pulses if success */
int stringToPulseTrain(const char* data, uint32_t* pulses, uint16_t maxlength);

/* Decode from array of pulses to json as dynamic char*. Must be free() after use */
char* decodePulseTrain(uint32_t* pulses, uint16_t length, const char* indent);

/* Decode from pilight string. Must be free() after use */
char* decodeString(const char* pilight_string);

/* Encode to pilight string. Must be free() after use */
char* encodeToString(const char* protocol_name, const char* json_data, uint8_t repeats);

/* Encode to pilight string from json. Must be free() after use */
char* encodeJson(const char* json, uint8_t repeats);

/* Get PiCode library version. Must be free() after use */
char* getPiCodeVersion(void);

/* Getter for protocols_t* pilight_protocols */
protocols_t* usedProtocols(void);

/* Getter for max possible number of pulses from protocol.h */
uint16_t protocol_maxrawlen(void);
