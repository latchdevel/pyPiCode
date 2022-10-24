"""
Unit tests for pyPiCode
Python C extension module to wrap the PiCode library

See: https://github.com/latchdevel/pyPiCode

Copyright (c) 2022 Jorge Rivera. All right reserved.
License GNU Lesser General Public License v3.0.
"""

import unittest
import pypicode as picode 

class test_pypicode(unittest.TestCase):
    
    # Conrad RSL Switches Protocol
    protocol_name   = 'conrad_rsl_switch'
    json_data_in    = {'id': 1, 'unit': 2, 'on': 1}
    json_dict_in    = {'conrad_rsl_switch': {'id': 1, 'unit': 2, 'on': 1}}
    json_dict_inout = {'conrad_rsl_switch': {'id': 1, 'unit': 2, 'state': 'on'}}
    json_data_out   = {'id': 1, 'unit': 2, 'state': 'on'}
    json_dict_out   = {'protocols': [{'conrad_rsl_switch': {'id': 1, 'unit': 2, 'state': 'on'}}]}
    pulses_list     = [1400,600,600,1400,600,1400,600,1400,1400,600,1400,600,1400,600,600,1400,600,1400,600,1400,1400,600,600,1400,600,1400,600,1400,1400,600,600,1400,1400,600,600,1400,1400,600,1400,600,1400,600,600,1400,1400,600,600,1400,600,1400,600,1400,600,1400,600,1400,600,1400,600,1400,600,1400,600,1400,600,6800]
    picode_string   = 'c:011010100101011010100110101001100110010101100110101010101010101012;p:1400,600,6800@'
    picode_string_r = 'c:011010100101011010100110101001100110010101100110101010101010101012;p:1400,600,6800;r:5@'
    picode_repeats  = 5

    def test_getPiCodeVersion(self):
        result = picode.getPiCodeVersion()
        self.assertIsNotNone(result)

    def test_findProtocol(self):
        result = picode.findProtocol(self.protocol_name)
        self.assertIsNotNone(result)

    def test_findProtocolFail(self):
        result = picode.findProtocol("fail")
        self.assertIsNone(result)

    def test_pulseTrainToString(self):
        result = picode.pulseTrainToString(self.pulses_list)
        self.assertEqual(result, self.picode_string)

    def test_pulseTrainToStringFail(self):
        result = picode.pulseTrainToString([])
        self.assertIsNone(result)
 
    def test_pulseTrainToStringRepeat(self):
        result = picode.pulseTrainToString(self.pulses_list,self.picode_repeats)
        self.assertEqual(result, self.picode_string_r)

    def test_encodeToPulseTrain(self):
        protocol = picode.findProtocol(self.protocol_name)
        result = picode.encodeToPulseTrain(protocol,self.json_data_in)
        self.assertEqual(result, self.pulses_list)

    def test_encodeToPulseTrainJson(self):
        protocol = picode.findProtocol(self.protocol_name)
        result = picode.encodeToPulseTrain(protocol,self.json_data_in)
        self.assertEqual(result, self.pulses_list)

    def test_encodeToPulseTrainJsonOut(self):
        protocol = picode.findProtocol(self.protocol_name)
        result = picode.encodeToPulseTrain(protocol,self.json_data_out)
        self.assertEqual(result, self.pulses_list)

    def test_encodeToPulseTrainFailJson(self):
        protocol = picode.findProtocol(self.protocol_name)
        result = picode.encodeToPulseTrain(protocol,{})
        self.assertIsNone(result)

    def test_encodeToPulseTrainByName(self):
        result = picode.encodeToPulseTrainByName(self.protocol_name,self.json_data_in)
        self.assertEqual(result, self.pulses_list)

    def test_encodeToPulseTrainByNameJsonOut(self):
        result = picode.encodeToPulseTrainByName(self.protocol_name,self.json_data_out)
        self.assertEqual(result, self.pulses_list)

    def test_encodeToPulseTrainByNameFailName(self):
        result = picode.encodeToPulseTrainByName("fail",self.json_data_in)
        self.assertIsNone(result)

    def test_encodeToPulseTrainByNameFailJson(self):
        result = picode.encodeToPulseTrainByName(self.protocol_name,{})
        self.assertIsNone(result)

    def test_stringToPulseTrain(self):
        result = picode.stringToPulseTrain(self.picode_string)
        self.assertEqual(result, self.pulses_list)

    def test_stringToPulseTrainRepeat(self):
        result = picode.stringToPulseTrain(self.picode_string_r)
        self.assertEqual(result, self.pulses_list)

    def test_decodePulseTrain(self):
        result = picode.decodePulseTrain(self.pulses_list)
        self.assertDictEqual(result, self.json_dict_out)

    def test_decodePulseTrainFail(self):
        result = picode.decodePulseTrain([])
        self.assertDictEqual(result, {'protocols': []})

    def test_decodeString(self):
        result = picode.decodeString(self.picode_string)
        self.assertDictEqual(result, self.json_dict_out)

    def test_decodeStringRepeat(self):
        result = picode.decodeString(self.picode_string_r)
        self.assertDictEqual(result, self.json_dict_out)

    def test_decodeStringFail(self):
        result = picode.decodeString("fail")
        self.assertIsNone(result)

    def test_encodeToString(self):
        result = picode.encodeToString(self.protocol_name,self.json_data_in)
        self.assertEqual(result, self.picode_string)

    def test_encodeToStringOut(self):
        result = picode.encodeToString(self.protocol_name,self.json_data_out)
        self.assertEqual(result, self.picode_string)

    def test_encodeToStringRepeat(self):
        result = picode.encodeToString(self.protocol_name,self.json_data_in,self.picode_repeats)
        self.assertEqual(result, self.picode_string_r)

    def test_encodeToStringRepeatOut(self):
        result = picode.encodeToString(self.protocol_name,self.json_data_out,self.picode_repeats)
        self.assertEqual(result, self.picode_string_r)

    def test_encodeToStringFailName(self):
        result = picode.encodeToString("fail",self.json_data_in)
        self.assertIsNone(result)

    def test_encodeToStringFailJson(self):
        result = picode.encodeToString(self.protocol_name,{})
        self.assertIsNone(result)

    def test_encodeJson(self):
        result = picode.encodeJson(self.json_dict_in)
        self.assertEqual(result, self.picode_string)

    def test_encodeJsonOut(self):
        result = picode.encodeJson(self.json_dict_inout)
        self.assertEqual(result, self.picode_string)

    def test_encodeJsonRepeat(self):
        result = picode.encodeJson(self.json_dict_in,self.picode_repeats)
        self.assertEqual(result, self.picode_string_r)

    def test_encodeJsonRepeatOut(self):
        result = picode.encodeJson(self.json_dict_inout,self.picode_repeats)
        self.assertEqual(result, self.picode_string_r)

    def test_encodeJsonFail(self):
        result = picode.encodeJson({})
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
