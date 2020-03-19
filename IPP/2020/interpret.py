#!/usr/bin/python 3.6
# -*- coding: utf-8 -*-
"""
IPP projekt 2

@author: Daniel Stepanek
@email: kxstepa61@stud.fit.vutbr.cz
"""
import sys
import re
import getopt
import xml.etree.ElementTree as ET
from xml.sax.saxutils import unescape

class InstructionDict():

    def __init__(self):
        self.opcode_dict = dict()
        self.opcode_dict['MOVE'] = [2,'var','symb']
        self.opcode_dict['CREATEFRAME'] = [0]
        self.opcode_dict['PUSHFRAME'] = [0]
        self.opcode_dict['POPFRAME'] = [0]
        self.opcode_dict['DEFVAR'] = [1,'var']
        self.opcode_dict['CALL'] = [1,'label']
        self.opcode_dict['RETURN'] = [0]
        self.opcode_dict['PUSHS'] = [1, 'symb']
        self.opcode_dict['POPS'] = [1, 'var']
        self.opcode_dict['ADD'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['SUB'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['MUL'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['IDIV'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['LT'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['GT'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['EQ'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['AND'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['OR'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['NOT']= [2, 'var', 'symb']
        self.opcode_dict['INT2CHAR'] = [2, 'var', 'symb']
        self.opcode_dict['STRI2INT'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['READ'] = [2, 'var', 'type']
        self.opcode_dict['WRITE'] = [1, 'symb']
        self.opcode_dict['CONCAT'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['STRLEN'] = [2, 'var', 'symb']
        self.opcode_dict['GETCHAR'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['SETCHAR'] = [3, 'var', 'symb', 'symb']
        self.opcode_dict['TYPE'] = [2, 'var', 'symb']
        self.opcode_dict['LABEL'] = [1, 'label']
        self.opcode_dict['JUMP'] = [1, 'label']
        self.opcode_dict['JUMPIFEQ'] = [3, 'label', 'symb', 'symb']
        self.opcode_dict['JUMPIFNEQ'] = [3, 'label', 'symb', 'symb']
        self.opcode_dict['EXIT'] = [1, 'symb']
        self.opcode_dict['DPRINT'] = [1, 'symb']
        self.opcode_dict['BREAK'] = [0]

    def get_keys(self):
        return self.opcode_dict.keys()

    def get_argc(self, opcode):
        op = self.opcode_dict.get(opcode)
        return op[0]

#Zpracovani vstupniho souboru ve formatu XML
class ParseXML():

    def parse(self, source):
        tree = ""
        root = ""

        try:
            tree = ET.parse(source)
            root = tree.getroot()
        except:
            sys.stderr.write("Invalid source file\n")
            exit(11)

        self.__check_root(root)

        instructions = dict()

        for child in root:
            if child.tag == 'name' or child.tag == 'description':
                continue
            if child.tag == 'instruction':
                order = int(child.attrib['order'])
                opcode = child.attrib['opcode']
                instruction = list()
                instruction.insert(0, order)
                instruction.insert(1, opcode.upper())
                args = list()
                for elem in child.iterfind('arg1'):
                    args.insert(0, elem)
                for elem in child.iterfind('arg2'):
                    args.insert(1, elem)
                for elem in child.iterfind('arg3'):
                    args.insert(2, elem)
                instruction.insert(2, args)

                if order not in instructions.keys():
                    instructions[order] = instruction
                else:
                    sys.stderr.write("Wrong order of instruction\n")
                    exit(32)
            else:
                sys.stderr.write("Wrong XML format\n")
                exit(32)

        return instructions

    def __check_root(self, root):
        if root.tag != 'program' or len(root.attrib) > 3 or root.attrib.get('language') != 'IPPcode20':
            sys.stderr.write("Wrong XML header format\n")
            exit(32)

class LabelDict():

    def __init__(self):
        self.labels = dict()

    def insert_label(self, label, order):
        if label not in self.labels.keys():
            self.labels[label] = order
        elif self.labels[label] == order:
            return
        else:
            sys.stderr.write("Label is already defined.\n")
            exit(52)

    def get_index(self, label):
        return self.labels.get(label)

    def get_labels(self):
        return self.labels


class Frame():

    def __init__(self):
        self.frame = dict()

    def set_value(self, key, value):
        self.frame[key] = value

    def get_item(self, key):
        if key in self.frame.keys():
            return self.frame[key]
        else:
            return None

    def is_var_set(self, key):
        if key in self.frame.keys():
            return key
        else:
            return None

    def get_frame(self):
        return self.frame

class Stack():

    def __init__(self):
        self.stack = list()

    def _push(self, value):
        self.stack.append(value)

    def _pop(self):
        try:
            return self.stack.pop()
        except:
            sys.stderr.write("Stack is empty.\n")
            exit(56)

class Processor():

    def __init__(self, input_f, label_dict):
        self.GF = Frame()
        self.LF = None
        self.TF = None
        self.input_f = input_f
        self.label_dict = label_dict
        self.data_stack = Stack()
        self.call_stack = Stack()
        self.frame_stack = Stack()

    def parse_var(self, var):
        return re.split('@', var, 2)

    def check_var_in_frame(self, var):
        if var[0] == 'GF':
            return self.GF.is_var_set(var[1])
        elif var[0] == 'LF':
            if self.LF != None:
                return self.LF.is_var_set(var[1])
            else:
                return None
        elif var[0] == 'TF':
            if self.TF != None:
                return self.TF.is_var_set(var[1])
            else:
                return None

    def get_var_value(self, var):
        if var[0] == 'GF':
            return self.GF.get_item(var[1])
        elif var[0] == 'LF':
            if self.LF != None:
                return self.LF.get_item(var[1])
            else:
                return None

        elif var[0] == 'TF':
            if self.TF != None:
                return self.TF.get_item(var[1])
            else:
                return None

    def set_var_value(self, var, symb):
        if var[0] == 'GF':
            self.GF.set_value(var[1], symb)
        elif var[0] == 'LF':
            if self.LF != None:
                self.LF.set_value(var[1], symb)
            else:
                return None

        elif var[0] == 'TF':
            if self.TF != None:
                self.TF.set_value(var[1], symb)
            else:
                return None

    def symb_switch(self, symb):
        s = symb.get("var")
        if s:
            return self.parse_var(s)
        elif s == None:
            return symb

    def get_symb(self, symb):
        s = self.symb_switch(symb)
        if isinstance(s, list):
            if self.check_var_in_frame(s):
                return self.get_var_value(s)
        else:
            return s

    def str_to_bool(self, value):
        pattern = {'true': True, 'false': False}
        return pattern.get(value)

    def bool_to_str(self, value):
        pattern = {'True': 'true', 'False': 'false'}
        return pattern.get(value)

    def get_type(self, symb):
        for k in symb.keys():
            return k

    def cmp(self, symb1, symb2, type, op):
        if type == 'bool':
            symb1 = self.str_to_bool(symb1)
            symb2 = self.str_to_bool(symb2)
        elif type == 'nil' and op != 'eq':
            sys.stderr.write("Bad comparison.\n")
            exit(53)

        if op == 'lt':
            return symb1 < symb2
        elif op == 'gt':
            return symb1 > symb2
        elif op == 'eq':
            return symb1 == symb2

    def conversion(self, value, type):
        if type == 'int':
            try:
                return int(value)
            except ValueError:
                sys.stderr.write("Invalid READ input\n")
                exit(57)
        elif type == 'bool':
            if value.lower() == 'true':
                return 'true'
            else:
                return 'false'
        elif type == 'string':
            return value

# Instruction set

    def _move(self, instruction):
        var = instruction[2].get("var")
        self.set_var_value(['GF', 'abc'], {'int':'2'})
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb = self.get_symb(instruction[3])
            if symb == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            self.set_var_value(var, symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _createframe(self):
        self.TF = Frame()

    def _pushframe(self):
        self.LF = self.TF
        self.TF = None
        self.frame_stack._push(self.LF)

    def _popframe(self):
        self.TF = self.frame_stack._pop()

    def _defvar(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            sys.stderr.write("Semantic error: Variable already exists.\n")
            exit(52)

        self.set_var_value(var, {'nil':'nil'})

    def _call(self, instruction):
        label = self.get_symb(instruction[2])
        if label == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)
        self.call_stack._push(instruction[0] + 1)
        return self._jump(instruction)

    def _return(self):
        return self.call_stack._pop()

    def _pushs(self, instruction):
        symb = self.get_symb(instruction[2])
        if symb == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

        self.data_stack._push(symb)

    def _pops(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb = self.data_stack._pop()
            self.set_var_value(var, symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _add(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("int")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("int")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            result = int(symb1) + int(symb2)
            symb = dict()
            symb['int'] = str(result)
            self.set_var_value(var, symb)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _sub(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("int")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("int")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            result = int(symb1) - int(symb2)
            symb = dict()
            symb['int'] = str(result)
            self.set_var_value(var, symb)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _mul(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("int")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("int")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            result = int(symb1) * int(symb2)
            symb = dict()
            symb['int'] = str(result)
            self.set_var_value(var, symb)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _idiv(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("int")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("int")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)
            if int(symb2) == 0:
                sys.stderr.write("Zero division.\n")
                exit(57)

            result = int(symb1) // int(symb2)
            symb = dict()
            symb['int'] = str(result)
            self.set_var_value(var, symb)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _lt(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            type1 = self.get_type(symb1)
            type2 = self.get_type(symb2)

            for v in symb1.values():
                symb1 = v

            for v in symb2.values():
                symb2 = v

            if type1 == type2:
                result = self.cmp(symb1, symb2, type1, 'lt')
                symb = dict()
                symb['bool'] = self.bool_to_str(str(result))
                self.set_var_value(var, symb)
            else:
                sys.stderr.write("Bad comparison.\n")
                exit(53)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _gt(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            type1 = self.get_type(symb1)
            type2 = self.get_type(symb2)

            for v in symb1.values():
                symb1 = v

            for v in symb2.values():
                symb2 = v

            if type1 == type2:
                result = self.cmp(symb1, symb2, type1, 'gt')
                symb = dict()
                symb['bool'] = self.bool_to_str(str(result))
                self.set_var_value(var, symb)
            else:
                sys.stderr.write("Bad comparison.\n")
                exit(53)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _eq(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            type1 = self.get_type(symb1)
            type2 = self.get_type(symb2)

            for v in symb1.values():
                symb1 = v

            for v in symb2.values():
                symb2 = v

            if type1 == type2:
                result = self.cmp(symb1, symb2, type1, 'eq')
                symb = dict()
                symb['bool'] = self.bool_to_str(str(result))
                self.set_var_value(var, symb)
            elif type1 == 'nil' or type2 == 'nil':
                symb = dict()
                symb['bool'] = 'false'
                self.set_var_value(var, symb)
            else:
                sys.stderr.write("Bad comparison.\n")
                exit(53)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _and(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("bool")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("bool")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb1 = self.str_to_bool(symb1)
            symb2 = self.str_to_bool(symb2)
            symb = symb1 and symb2
            d_symb = dict()
            d_symb['bool'] = self.bool_to_str(str(symb))
            self.set_var_value(var, d_symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _or(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("bool")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("bool")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb1 = self.str_to_bool(symb1)
            symb2 = self.str_to_bool(symb2)
            symb = symb1 or symb2
            d_symb = dict()
            d_symb['bool'] = self.bool_to_str(str(symb))
            self.set_var_value(var, d_symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _not(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb = self.get_symb(instruction[3])
            if symb == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb = symb.get("bool")
            if symb == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb = self.str_to_bool(symb)
            symb = not symb
            d_symb = dict()
            d_symb['bool'] = self.bool_to_str(str(symb))
            self.set_var_value(var, d_symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _int2char(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb = self.get_symb(instruction[3])
            if symb == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb = symb.get("int")
            if symb == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            if int(symb) < 0 or int(symb) > 1114111:
                sys.stderr.write("Semantic error: Wrong value of argument (out of range).\n")
                exit(58)

            result = chr(int(symb))
            d_symb = dict()
            d_symb['string'] = str(result)
            self.set_var_value(var, d_symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _stri2int(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("string")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("int")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            len_of_symb1 = len(symb1)
            index = int(symb2)
            if index < 0 or index >= len_of_symb1:
                sys.stderr.write("Semantic error: Index out of range.\n")
                exit(58)

            result = ord(symb1[index])
            r_dict = dict()
            r_dict['int'] = str(result)
            self.set_var_value(var, r_dict)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _read(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb = self.get_symb(instruction[3])
            if symb == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb = symb.get("type")
            if symb == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            try:
                file = open(self.input_f)
                sys.stdin = file
            except:
                sys.stderr.write("Unable to open input file.\n")
                exit(11)

            input_value = ""
            try:
                input_value = input()
            except:
                input_value = 'nil'

            if input_value == 'nil':
                input_d = dict()
                input_d['nil'] = 'nil'
            else:
                input_value = self.conversion(input_value, symb)
                input_d = dict()
                input_d[symb] = input_value
                self.set_var_value(var, input_d)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _write(self, instruction):
        symb = self.get_symb(instruction[2])
        if symb == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)
        type = ""
        value = ""
        for type, value in symb.items():
            pass
        if type == 'bool':
            value = value.lower()
        elif type == 'nil':
            value = ''

        if type == 'string':
            #unescape XML special signs(&lt;, &gt;, ...)
            value = unescape(value)
            #nahradi escape sekvence validnimi bilymi znaky
            value = re.sub(r"\\([0-9][0-9][0-9])", lambda sign: chr(int(sign.group(1))), value)

        print(value, end = '')

    def _concat(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("string")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("string")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb = "%s%s"%(symb1, symb2)
            symb_d = dict()
            symb_d['string'] = symb
            self.set_var_value(var, symb_d)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _strlen(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("string")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            length = len(symb1)
            symb_d = dict()
            symb_d['int'] = length
            self.set_var_value(var, symb_d)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _getchar(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("string")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("int")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            len_of_symb1 = len(symb1)
            index = int(symb2)
            if index < 0 or index >= len_of_symb1:
                sys.stderr.write("Semantic error: Index out of range.\n")
                exit(58)

            char = symb1[index]
            r_dict = dict()
            r_dict['string'] = str(char)
            self.set_var_value(var, r_dict)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _setchar(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            var_v = self.get_var_value(var)
            var_v = var_v.get("string")
            if var_v == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(55)

            symb1 = self.get_symb(instruction[3])
            if symb1 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb1 = symb1.get("int")
            if symb1 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            symb2 = self.get_symb(instruction[4])
            if symb2 == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)
            symb2 = symb2.get("string")
            if symb2 == None:
                sys.stderr.write("Semantic error: Wrong type of argument.\n")
                exit(53)

            len_of_var_v = len(var_v)
            index = int(symb1)
            if index < 0 or index >= len_of_var_v:
                sys.stderr.write("Semantic error: Index out of range.\n")
                exit(58)
            if len(symb2) < 1:
                sys.stderr.write("Semantic error: Wrong value of argument.\n")
                exit(58)

            char = symb2[0]
            var_v = var_v.replace(var_v[index], char)
            r_dict = dict()
            r_dict['string'] = str(var_v)
            self.set_var_value(var, r_dict)

        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _type(self, instruction):
        var = instruction[2].get("var")
        var = self.parse_var(var)
        if self.check_var_in_frame(var):
            symb = self.get_symb(instruction[3])
            if symb == None:
                sys.stderr.write("Semantic error: Undefined variable.\n")
                exit(54)

            type = self.get_type(symb)
            d_symb = dict()
            d_symb['type'] = type
            self.set_var_value(var, d_symb)
        else:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

    def _label(self, instruction):
        label = self.get_symb(instruction[2])
        if label == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)
        label = label.get("label")
        if label == None:
            sys.stderr.write("Semantic error: Wrong type of argument.\n")
            exit(53)

        self.label_dict.insert_label(label, instruction[0])

    def _jump(self, instruction):
        label = self.get_symb(instruction[2])
        if label == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)
        label = label.get("label")
        if label == None:
            sys.stderr.write("Semantic error: Wrong type of argument.\n")
            exit(53)

        index = self.label_dict.get_index(label)
        if index == None:
            sys.stderr.write("Semantic error: label does not exist.\n")
            exit(52)

        return index

    def _jumpifeq(self, instruction):
        symb1 = self.get_symb(instruction[3])
        if symb1 == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

        symb2 = self.get_symb(instruction[4])
        if symb2 == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

        type1 = self.get_type(symb1)
        type2 = self.get_type(symb2)

        for v in symb1.values():
            symb1 = v

        for v in symb2.values():
            symb2 = v

        if type1 == type2:
            if self.cmp(symb1, symb2, type1, 'eq'):
                self._jump(instruction)
        elif type1 == 'nil' or type2 == 'nil':
            if self.cmp(symb1, symb2, type1, 'eq'):
                self._jump(instruction)
        else:
            sys.stderr.write("Bad comparison.\n")
            exit(53)

    def _jumpifneq(self, instruction):
        symb1 = self.get_symb(instruction[3])
        if symb1 == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

        symb2 = self.get_symb(instruction[4])
        if symb2 == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

        type1 = self.get_type(symb1)
        type2 = self.get_type(symb2)

        for v in symb1.values():
            symb1 = v

        for v in symb2.values():
            symb2 = v

        if type1 == type2:
            if not self.cmp(symb1, symb2, type1, 'eq'):
                self._jump(instruction)
        elif type1 == 'nil' or type2 == 'nil':
            if not self.cmp(symb1, symb2, type1, 'eq'):
                self._jump(instruction)
        else:
            sys.stderr.write("Bad comparison.\n")
            exit(53)

    def _exit(self, instruction):
        symb = self.get_symb(instruction[2])
        if symb == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)
        symb = symb.get("int")
        if symb == None:
            sys.stderr.write("Semantic error: Wrong type of argument.\n")
            exit(53)

        code = int(symb)
        if code >= 0 and code <= 49:
            exit(code)
        else:
            sys.stderr.write("Semantic error: Value out of range.\n")
            exit(57)

    def _dprint(self, instruction):
        symb = self.get_symb(instruction[2])
        if symb == None:
            sys.stderr.write("Semantic error: Undefined variable.\n")
            exit(54)

        for v in symb.values():
            sys.stderr.write(v)

    def _break(self, instruction):
        sys.stderr.write("Debug information\n")
        sys.stderr.write("------------------\n")

        sys.stderr.write("Order: ")
        sys.stderr.write(str(instruction[0]))
        sys.stderr.write("\n")

        sys.stderr.write("Global frame:\n")
        for key, value in self.GF.get_frame().items():
            sys.stderr.write(key + " : ")
            for k, v in value.items():
                sys.stderr.write(k + " : ")
                sys.stderr.write(v)
            sys.stderr.write("\n")
        sys.stderr.write("\n")

        sys.stderr.write("Local frame:\n")
        if self.LF != None:
            for key, value in self.LF.get_frame().items():
                sys.stderr.write(key + " : ")
                for k, v in value.items():
                    sys.stderr.write(k + " : ")
                    sys.stderr.write(v)
                sys.stderr.write("\n")
            sys.stderr.write("\n")

        sys.stderr.write("Temporary frame:\n")
        if self.TF != None:
            for key, value in self.TF.get_frame().items():
                sys.stderr.write(key + " : ")
                for k, v in value.items():
                    sys.stderr.write(k + " : ")
                    sys.stderr.write(v)
                sys.stderr.write("\n")
            sys.stderr.write("\n")

        sys.stderr.write("Used labels:\n")
        for k, v in self.label_dict.get_labels().items():
            sys.stderr.write(k + "\n")
        sys.stderr.write("---------------------\n")


class Interpret():

    def __init__(self, source_f, input_f):
        self.source_f = source_f
        self.input_f = input_f
        self.label_dict = LabelDict()
        self.instruction_dict = InstructionDict()
        self.processor = Processor(self.input_f, self.label_dict)

    def main(self):
        parser = ParseXML()
        instructions = parser.parse(self.source_f)
        instructions = self.syntax(instructions)
        self.runtime(instructions)

    def op_code_switch(self, op_code, instruction):
            order = instruction[0]
            if 'MOVE' == op_code:
                self.processor._move(instruction)
            elif 'CREATEFRAME' == op_code:
                self.processor._createframe()
            elif 'PUSHFRAME' == op_code:
                self.processor._pushframe()
            elif 'POPFRAME' == op_code:
                self.processor._popframe()
            elif 'DEFVAR' == op_code:
                self.processor._defvar(instruction)
            elif 'CALL' == op_code:
                return self.processor._call(instruction)
            elif 'RETURN' == op_code:
                return self.processor._return()
            elif 'PUSHS' == op_code:
                self.processor._pushs(instruction)
            elif 'POPS' == op_code:
                self.processor._pops(instruction)
            elif 'ADD' == op_code:
                self.processor._add(instruction)
            elif 'SUB' == op_code:
                self.processor._sub(instruction)
            elif 'MUL' == op_code:
                self.processor._mul(instruction)
            elif 'IDIV' == op_code:
                self.processor._idiv(instruction)
            elif 'LT' == op_code:
                self.processor._lt(instruction)
            elif 'GT' == op_code:
                self.processor._gt(instruction)
            elif 'EQ' == op_code:
                self.processor._eq(instruction)
            elif 'AND' == op_code:
                self.processor._and(instruction)
            elif 'OR' == op_code:
                self.processor._or(instruction)
            elif 'NOT' == op_code:
                self.processor._not(instruction)
            elif 'INT2CHAR' == op_code:
                self.processor._int2char(instruction)
            elif 'STRI2INT' == op_code:
                self.processor._stri2int(instruction)
            elif 'READ' == op_code:
                self.processor._read(instruction)
            elif 'WRITE' == op_code:
                self.processor._write(instruction)
            elif 'CONCAT' == op_code:
                self.processor._concat(instruction)
            elif 'STRLEN' == op_code:
                self.processor._strlen(instruction)
            elif 'GETCHAR' == op_code:
                self.processor._getchar(instruction)
            elif 'SETCHAR' == op_code:
                self.processor._setchar(instruction)
            elif 'TYPE' == op_code:
                self.processor._type(instruction)
            elif 'LABEL' == op_code:
                self.processor._label(instruction)
            elif 'JUMP' == op_code:
                return self.processor._jump(instruction)
            elif 'JUMPIFEQ' == op_code:
                return self.processor._jumpifeq(instruction)
            elif 'JUMPIFNEQ' == op_code:
                return self.processor._jumpifneq(instruction)
            elif 'EXIT' == op_code:
                self.processor._exit(instruction)
            elif 'DPRINT' == op_code:
                self.processor._dprint(instruction)
            elif 'BREAK' == op_code:
                self.processor._break(instruction)

    def save_all_labels(self, instructions):
        for instruction in instructions.values():
            if instruction[1] == 'LABEL':
                self.processor._label(instruction)

    def get_instruction(self, instructions, order):
        return instructions[order]

    def runtime(self, instructions):
        self.save_all_labels(instructions)

        instruction_list = list(instructions.values())
        index = 0
        while index < len(instruction_list):
            instruction = self.get_instruction(instruction_list, index)
            i = self.op_code_switch(instruction[1], instruction)
            if i != None:
                index = i
            else:
                index += 1

    def regex_switch(self, type):
        switcher = {
            'var':'(TF|LF|GF)@([\-\_\$\&\%\*\!\?[a-zA-Z]+[\-\_\$\&\%\*\!\?\w]*)$',
            'int':'([+-]?\d+)$',
            'bool':'(true|false)$',
            'string':'((\w*[\<\>\&\'\"\/\-\§\,\;\)\(\=]*[áéěíýóúůžščřďťňÁÉĚÍÝÓÚŮŽŠČŘĎŤŇ]*(\\\[0-9][0-9][0-9])*\w*)*)$',
            'nil':'(nil)$',
            'label':'^([\-\_\$\&\%\*\!\?[a-zA-Z]+[^@][\-\_\$\&\%\*\!\?[a-zA-Z]*)$',
            'type':'(int|string|bool)$'
        }
        return switcher.get(type, "None")

    def check_opcode(self, opcode):
        if opcode in self.instruction_dict.get_keys():
            return 0
        else:
            return 1

    def syntax(self, instructions):
        temp_instructions = dict()
        for instruction in instructions.values():
            opcode = instruction[1]
            if self.check_opcode(opcode) != 0:
                sys.stderr.write("Wrong opcode\n")
                exit(32)

            #inst = [order, op_code, arg1:{type : value}, arg2:{type : value}, arg3:{type : value}]
            inst = list()
            inst.insert(0, instruction[0])
            inst.insert(1, opcode)

            argc = self.instruction_dict.get_argc(opcode)
            for i in range(0, argc):
                pattern = self.regex_switch(instruction[2][i].attrib.get("type"))
                if pattern == "None":
                    sys.stderr.write("Wrong type of argument\n")
                    exit(32)

                #create empty string
                if instruction[2][i].attrib.get("type") == 'string' and instruction[2][i].text == None:
                    instruction[2][i].text = str("")

                check = re.search(pattern, instruction[2][i].text)
                if check == None:
                    sys.stderr.write("Wrong value of argument\n")
                    exit(32)

                arg = dict()
                arg[instruction[2][i].attrib.get("type")] = instruction[2][i].text
                inst.insert(i + 2, arg)

            temp_instructions[instruction[0]] = inst
        return temp_instructions



#Parameter --help
def PrintHelp():
    print("Napoveda ke skriptu interpret.py\n")

    print("Skript nacte XML reprezentaci programu ze zadaneho souboru pomoci STDIO,")
    print("pote interpretuje a nasledne na STDOUT vypise odpovidajici vystup programu.\n")
    print("52 - chyba pri semantickych kontrolach vstupniho kodu v IPPcode19 (napr. pouziti nedefinovaneho navesti")
    print("53 - behova chyba interpretace – spatne typy operandu")
    print("54 - behova chyba interpretace – pristup k neexistujici promenne (ramec existuje)")
    print("55 - behova chyba interpretace – ramec neexistuje (napr. cteni z prazdneho zasobniku ramcu)")
    print("56 - behova chyba interpretace – chybejici hodnota (v promenne, na datovem zasobniku, nebo v zasobniku volani)")
    print("57 - behova chyba interpretace – spatna hodnota operandu (napr. deleni nulou, spatna navratova hodnota instrukce EXIT)")
    print("58 - behova chyba interpretace – chybna prace s retezcem\n")

    print("Chybove kody pro specificke pro interpret:")
    print("31 - chybný XML formát ve vstupním souboru \(soubor není tzv. dobře formátovaný, angl. well-formed\);")
    print("32 - neočekávaná struktura XML \(např. element pro argument mimo element pro instrukci,")
    print("     instrukce s duplicitním pořadím nebo záporným pořadím\) či lexikální nebo syntaktická chyba")
    print("     textových elementů a atributů ve vstupním XML souboru \(např. chybný lexém pro řetězcový")
    print("     literál, neznámý operační kód apod.\).\n")

    print("Vstupni parametry:")
    print("--help viz společný parametr všech skriptů v sekci 2.2\n")
    print("--source=file vstupní soubor s XML reprezentací zdrojového kódu dle definice ze sekce 3.1;\n")
    print("--input=file soubor se vstupy pro samotnou interpretaci zadaného zdrojového kódu.\n")
    print("Alespoň jeden z parametrů \(--source nebo --input\) musí být vždy zadán. Pokud jeden z nich chybí, tak jsou odpovídající data načítána ze standardního vstupu.")

if __name__ == "__main__":

    #Input Parameters
    isSource = False
    isInput = False

    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--help"):
            PrintHelp()
            exit(0)

    options, args = getopt.getopt(sys.argv[1:], 'si:',['source=', 'input=', '<'])

    if( (len(sys.argv) == 3) & (len(options) < 2) ):
        sys.stderr.write("Wrong input parameters\n")
        exit(10)

    source_f = sys.stdin
    input_f = sys.stdin

    for opt, value in options:
        if(opt in ['--source', '-s']):
            source_f = value
            isSource = True

        elif(opt in ['--input', '-i']):
            input_f = value
            isInput = True

    if( ( (isSource == False) & (isInput == False)) | (len(sys.argv) < 2) | (len(sys.argv) > 3) ):
        sys.stderr.write("Wrong input parameters\n")
        exit(10)

    interpret = Interpret(source_f, input_f)
    interpret.main()
