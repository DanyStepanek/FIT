#!/usr/bin/python 3
# -*- coding: utf-8 -*-
"""
Created on Mon March  20 21:58:01 2019

@author: Daniel Stepanek xstepa61
"""

import sys
import re
import getopt
import xml.etree.ElementTree as ET

#Zpracovani vstupniho souboru ve formatu XML
class ParseXML():

    def Parse(self, source):
        tree = ""
        root = ""

        try:
            tree = ET.parse(source)
            root = tree.getroot()
        except:
            sys.stderr.write("Invalid source file\n")
            exit(11)
        self._check_root(root)
        instructions = list()
        order_list = list()

        for instruction in root:
            if instruction.tag == 'name' or instruction.tag == 'description':
                continue
            if instruction.tag == 'instruction':
                #seradi instrukce podle 'order'
                order = int(instruction.get('order'))
                if(order not in order_list):
                    order_list.insert(order-1, order)
                    instructions.insert(order-1, self._instruction_factory(instruction))
                else:
                    sys.stderr.write("Wrong order of instruction\n")
                    exit(32)
            else:
                sys.stderr.write("Wrong XML format\n")
                exit(32)

        for order in order_list:
            if((order > len(order_list)) | (order <= 0)):
                sys.stderr.write("Wrong order of instruction\n")
                exit(32)

        return instructions

    def _check_root(self, root):
        if root.tag != 'program' or len(root.attrib) > 3 or root.attrib.get('language') != 'IPPcode19':
            sys.stderr.write("Wrong XML header format\n")
            exit(32)


    def _instruction_factory(self, instruction):
        opcode = instruction.get('opcode')
        inst_content = list(instruction)
        inst_content.insert(0, opcode.upper())
        return inst_content


class TemporaryFrame():

    def __init__(self):
        self.frame_dict = None

    def _create(self):
        self.frame_dict = dict()

    def _clear(self):
        self.frame_dict.clear()

    def _push(self, item):
        if self.frame_dict is not None:
            self.frame_dict = item.copy()
        else:
            sys.stderr.write("ERROR: Temporary frame is not set\n")
            exit(55)


    def _push_item(self, item):
        if self.frame_dict is not None:
            if(item not in self.frame_dict.keys()):
                self.frame_dict[item] = list()
            else:
                sys.stderr.write("ERROR: Redefining variable < " + str(item)+ " > in temporary frame.\n")
                exit(52)
        else:
            sys.stderr.write("ERROR: Temporary frame is not set\n")
            exit(55)


    def _pop(self):
        if self.frame_dict is not None:
            return self.frame_dict
        else:
            sys.stderr.write("ERROR: Temporary Frame is empty\n")
            exit(55)

    def _actualize(self, item, value):
        try:
            if(item in self.frame_dict.keys()):
                self.frame_dict[item] = value
            else:
                sys.stderr.write("ERROR: Variable is not in temporary frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Temporary frame is not set\n")
            exit(54)

    def _get_type(self, item):
        try:
            if(item in self.frame_dict.keys()):
                return self.frame_dict[item][1]
            else:
                sys.stderr.write("ERROR: Variable is not in temporary frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Temporary frame is not set\n")
            exit(55)

    def _get_value(self, item):
        if(item in self.frame_dict.keys()):
            return self.frame_dict[item][0]
        else:
            sys.stderr.write("ERROR: Variable is not in temporary frame.\n")
            exit(55)

class LocalFrame():

    def __init__(self):
        self.frame_list = list()

    def _push(self, item):
        self.frame_list.insert(0, dict(item))


    def _pop(self):
        if self.frame_list != []:
            return self.frame_list.pop(0)
        else:
            sys.stderr.write("ERROR: Local Frame is empty\n")
            exit(55)

    def _push_item(self, item):
        if self.frame_list != []:
            if(item not in self.frame_list[0].keys()):
                self.frame_list[0][item] = list()
            else:
                sys.stderr.write("ERROR: Redefining variable < " + str(item)+ " > in global frame.\n")
                exit(52)
        else:
            sys.stderr.write("ERROR: Local Frame is empty\n")
            exit(55)

    def _actualize(self, item, value):
        try:
            if(item in self.frame_list[0].keys()):
                self.frame_list[0][item] = value
            else:
                sys.stderr.write("ERROR: Variable is not in local frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Local frame is not set\n")
            exit(54)

    def _get_type(self, item):
        try:
            if(item in self.frame_list[0].keys()):
                return self.frame_list[0][item][1]
            else:
                sys.stderr.write("ERROR: Variable is not in local frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Local frame is not set\n")
            exit(54)

    def _get_value(self, item):
        try:
            if(item in self.frame_list[0].keys()):
                return self.frame_list[0][item][0]
            else:
                sys.stderr.write("ERROR: Variable is not in local frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Local frame is not set\n")
            exit(55)

class GlobalFrame():

    def __init__(self):
        self.frame_dict = dict()

    def _push_item(self, item):
        try:
            if(item not in self.frame_dict.keys()):
                self.frame_dict[item] = list()
            else:
                sys.stderr.write("ERROR: Redefining variable < " + str(item)+ " > in global frame.\n")
                exit(52)
        except:
            sys.stderr.write("ERROR: Global frame is not set\n")
            exit(55)

    def _pop_item(self, item):
        try:
            if(item in self.frame_dict.keys()):
                self.frame_dict.pop(item)
            else:
                sys.stderr.write("ERROR: Global frame is undefined.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Global frame is not set\n")
            exit(55)

    def _get_type(self, item):
        try:
            if(item in self.frame_dict.keys()):
                if len(self.frame_dict[item]) > 0 :
                    return self.frame_dict[item][1]
                else:
                    return None
            else:
                sys.stderr.write("ERROR: Variable is not in global frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Global frame is not set\n")
            exit(54)

    def _get_value(self, item):
        try:
            if(item in self.frame_dict.keys()):
                return self.frame_dict[item]
            else:
                sys.stderr.write("ERROR: Variable is not in global frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Global frame is not set\n")
            exit(54)

    def _actualize(self, item, value):
        try:
            if(item in self.frame_dict.keys()):
                self.frame_dict[item] = value
            else:
                sys.stderr.write("ERROR: Variable is not in global frame.\n")
                exit(55)
        except:
            sys.stderr.write("ERROR: Global frame is not set\n")
            exit(54)

#Data stack a call stack
class Stack():

    def __init__(self):
        self._stack = list()

    def _push(self, item):
        self._stack.insert(0, item)

    def _pop(self):
        if not self._is_empty():
            return self._stack.pop(0)
        else:
            sys.stderr.write("ERROR: Stack is empty\n")
            exit(56)

    def _is_empty(self):
        if len(self._stack) == 0:
            return True
        else:
            return False

class LabelDict():
    def __init__(self):
        self.label_table = dict()

    def _push_label(self, item, value):
        if item not in self.label_table.keys():
            self.label_table[item] = value
        elif ( (item in self.label_table.keys()) & (value == self.label_table[item]) ):
            pass
        else:
            sys.stderr.write("Label already exists\n")
            exit(57)

    def _get_label_ip(self, item):
        if item in self.label_table.keys():
            return self.label_table[item]
        else:
            sys.stderr.write("Label doesnt exists\n")
            exit(52)

class InstructionDict():

    opcode_dict = dict()
    opcode_dict['MOVE'] = [2,'var','symb']
    opcode_dict['CREATEFRAME'] = [0]
    opcode_dict['PUSHFRAME'] = [0]
    opcode_dict['POPFRAME'] = [0]
    opcode_dict['DEFVAR'] = [1,'var']
    opcode_dict['CALL'] = [1,'label']
    opcode_dict['RETURN'] = [0]
    opcode_dict['PUSHS'] = [1, 'symb']
    opcode_dict['POPS'] = [1, 'var']
    opcode_dict['ADD'] = [3, 'var', 'symb', 'symb']
    opcode_dict['SUB'] = [3, 'var', 'symb', 'symb']
    opcode_dict['MUL'] = [3, 'var', 'symb', 'symb']
    opcode_dict['IDIV'] = [3, 'var', 'symb', 'symb']
    opcode_dict['LT'] = [3, 'var', 'symb', 'symb']
    opcode_dict['GT'] = [3, 'var', 'symb', 'symb']
    opcode_dict['EQ'] = [3, 'var', 'symb', 'symb']
    opcode_dict['AND'] = [3, 'var', 'symb', 'symb']
    opcode_dict['OR'] = [3, 'var', 'symb', 'symb']
    opcode_dict['NOT']= [2, 'var', 'symb']
    opcode_dict['INT2CHAR'] = [2, 'var', 'symb']
    opcode_dict['STRI2INT'] = [3, 'var', 'symb', 'symb']
    opcode_dict['READ'] = [2, 'var', 'type']
    opcode_dict['WRITE'] = [1, 'symb']
    opcode_dict['CONCAT'] = [3, 'var', 'symb', 'symb']
    opcode_dict['STRLEN'] = [2, 'var', 'symb']
    opcode_dict['GETCHAR'] = [3, 'var', 'symb', 'symb']
    opcode_dict['SETCHAR'] = [3, 'var', 'symb', 'symb']
    opcode_dict['TYPE'] = [2, 'var', 'symb']
    opcode_dict['LABEL'] = [1, 'label']
    opcode_dict['JUMP'] = [1, 'label']
    opcode_dict['JUMPIFEQ'] = [3, 'label', 'symb', 'symb']
    opcode_dict['JUMPIFNEQ'] = [3, 'label', 'symb', 'symb']
    opcode_dict['EXIT'] = [1, 'symb']
    opcode_dict['DPRINT'] = [1, 'symb']
    opcode_dict['BREAK'] = [0]

    def __init__(self):
        pass

#Trida pro zpracovani instrukci
class Instruction(InstructionDict):

    def __init__(self):
        super(InstructionDict, self).__init__()
# Z nactenych instukci v @instructions postupne kontroluje spravnost operacnich kodu
#  a nasledne zkontorluje pocet a odpovidajici typy jednotlivych argumentu Instrukce
    def Processing(self, instructions):
        #zkontroluje opcode,
        for i in range(0, len(instructions)):
            if instructions[i][0] in self.opcode_dict:
                instruction = instructions[i]
                expected_count = self.opcode_dict[instructions[i][0]][0]
                instructions[i] = self._get_attributes(instruction, expected_count)
            else:
            #incorrect XML opcode
                sys.stderr.write("Invalid opcode in instruction: " + str((i+1)) + ", opcode: "+ str(instructions[i][0]) + "\n")
                exit(32)
        return instructions

    def _get_attributes(self, instruction, expected_count):

        if(len(instruction)-1 == expected_count):
            tmplist = list()
            tmplist.insert(0, instruction[0])
            #serad argumenty
            for i in range(1, expected_count+1):
                if(instruction[i].tag == "arg1"):
                    tmplist.insert(1, [instruction[i].get('type'), instruction[i].text])
                if(instruction[i].tag == "arg2"):
                    tmplist.insert(2, [instruction[i].get('type'), instruction[i].text])
                if(instruction[i].tag == "arg3"):
                    tmplist.insert(3, [instruction[i].get('type'), instruction[i].text])
            #nahrad odkazy na argumenty dvojici [typ, hodnota]
            instruction = tmplist
            return instruction

        if((len(instruction) == 0) & (expected_count == 0)):
            tmplist = list()
            tmplist.insert(0, instruction[0])
            instruction = tmplist
            return instruction
        else:
            #incorrect XML opcode
            sys.stderr.write("Invalid count of arguments, instruction " + str(instruction[0]) + "\n")
            exit(32)

#Kazdy atribut jednotlivych instrukci zkontroluje pomoci regularnich vyrazu a ulozi
#atributy do listu ve v tvaru [hodnota, typ], jenz nasledne ulozi do listu atributu.
class Attribute(InstructionDict):

    def __init__(self):
        super(InstructionDict, self).__init__()
        self.attributes = list()
        self.list_of_attributes = list()

    def Processing(self, instructions):

        for instruction in instructions:
            self.attributes = []

            for i in range(1, len(instruction)):
                pointer_to_dict = self.opcode_dict[instruction[0]][i]
                type = instruction[i][0]
                value = instruction[i][1]

                if(pointer_to_dict == "var"):
                    self._var(type, value)
                elif(pointer_to_dict == "symb"):
                    if(type == "string"):
                        value = str(value)
                    self._symb(type, value)
                elif(pointer_to_dict == "label"):
                    self._label(type, value)
                elif(pointer_to_dict == "type"):
                    self._type(type, value)
                else:
                    sys.stderr.write("Invalid type of argument\n")
                    exit(32)

                self.attributes.append(instruction[i])

            self.list_of_attributes.append(self.attributes)

        return self.list_of_attributes


    def _var(self, type, value):
        #frame@special_characters or alphanumeric characters
        check = re.search('(TF|LF|GF)@([\-\_\$\&\%\*\!\?\w]+)$', value)
        self._check(check)

    def _symb(self, type, value):
        #frame@special_characters or alphanumeric characters
        if(type == "var"):
            check = re.search('(TF|LF|GF)@([\-\_\$\&\%\*\!\?\w]+)$', value)
            self._check(check)

        elif(type == "int"):
            check = re.search('([+-]?\d+)$', value)
            self._check(check)


        elif(type == "bool"):
            check = re.search('(true|false)$', value)
            self._check(check)

        elif(type == "string"):
            #special_characters or alphanumeric characters or special escape sequences \[0-9][0-9][0-9]
            check = re.search('([\$\%\*\!\<\>\&\'\"\/\-\_]*(\\[0-9][0-9][0-9])*\w*)', value)
            self._check(check)

        elif(type == "nil"):
            check = re.search('(nil)$', value)
            self._check(check)

    def _label(self, type, value):
        check = re.search('(\w+)$', value)
        self._check(check)

    def _type(self, type, value):
        check = re.search('(int|string|bool)$', value)
        self._check(check)

    def _check(self,check):
        if(check == None):
            sys.stderr.write("Invalid value of argument\n")
            exit(32)
        else:
            return

#Ridici trida interpretu. Vola funkce pro zpracovani instrukci, jejich parametru a
# nasledne vykonava fuknce pro jednotlive instrukce.
class Processor():

    def __init__(self, source, input):
        self.instructions = Instruction()
        self.attributes = Attribute()
        self.globalframe = GlobalFrame()
        self.localframe = LocalFrame()
        self.temporaryframe = TemporaryFrame()
        self.datastack = Stack()
        self.callstack = Stack()
        self.labeltable = LabelDict()
        self.source = source
        self.input = input

    def Interpret(self):
        self._processing()
        #hledani navesti (prvni pruchod)
        for IP in range(0, len(self.instructions)):
            instruction = self.instructions[IP]
            if(instruction[0] == "LABEL"):
                self._label(IP)


        #pro kazdou instrukci rozhodni co je a vykonej ji pomoci patricne funkce
        IP = 0
        while IP < len(self.instructions):
            instruction = self.instructions[IP]
            method_name = "".join(['self._', instruction[0].lower(), '(', str(IP),')'])
            #zpracovani skokovych instrukci a skoky na instrukce dle navesti a jejich pozici v kodu
            if((instruction[0] in ["JUMP", "JUMPIFEQ", "JUMPIFNEQ", "CALL", "RETURN"]) ):
                IP = eval(method_name)
            else:
                eval(method_name)
                IP = IP + 1

    def _processing(self):
        parseXML = ParseXML()
        instructions = parseXML.Parse(self.source)

        self.instructions = self.instructions.Processing(instructions)
        self.attributes = self.attributes.Processing(instructions)

    def _get_value_and_type(self, frame, name):
        type = ""
        value = ""

        if(frame == "GF"):
            type = self.globalframe._get_type(name)
            value = self.globalframe._get_value(name)
        elif(frame == "LF"):
            type = self.localframe._get_type(name)
            value = self.localframe._get_value(name)
        elif(frame == "TF"):
            type = self.temporaryframe._get_type(name)
            value = self.temporaryframe._get_value(name)
        else:
            sys.stderr.write("Wrond type of argument in instruction\n")
            exit(53)

        item = [value, type]
        return item


    def _get_frame_and_name(self, value):
        return re.search('(TF|LF|GF)@([\-\_\$\&\%\*\!\?\w]+)$', value)

#Jednotlive funkce pro kazdou instrukci.

    #Práce s rámci, volání funkcí
    def _move(self, IP):
        item = list()

        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_source = self.attributes[IP][1][0]
        source = self.attributes[IP][1][1]

        if((type_of_source == "string") & (source == None)):
            source = ""

        check = self._get_frame_and_name(dest)
        frame = check.group(1)
        name = check.group(2)

        item = [source, type_of_source]

        if(frame == "GF"):
            self.globalframe._actualize(name, item)
        elif(frame == "LF"):
            self.localframe._actualize(name, item)
        elif(frame == "TF"):
            self.temporaryframe._actualize(name, item)

        else:
            sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
            exit(53)

    def _createframe(self, IP):
        self.temporaryframe._create()

    def _pushframe(self, IP):
        item = self.temporaryframe._pop()
        self.localframe._push(item)
        self.temporaryframe._clear()

    def _popframe(self, IP):
        item = self.localframe._pop()
        self.temporaryframe._push(item)

    def _defvar(self, IP):
        value = self.attributes[IP][0][1]
        check = self._get_frame_and_name(value)
        frame = check.group(1)
        name = check.group(2)

        if(frame == "GF"):
            self.globalframe._push_item(name)
        elif(frame == "LF"):
            self.localframe._push_item(name)
        elif(frame == "TF"):
            self.temporaryframe._push_item(name)
        else:
            sys.stderr.write("Invalid argument\n")
            exit(53)

    def _call(self, IP):
        type = self.attributes[IP][0][0]
        value = self.attributes[IP][0][1]

        if(type == "label"):
            self.callstack._push(IP)
            return self.labeltable._get_label_ip(value)
        else:
            sys.stderr.write("Wrong type of 1st argument in " + str(IP) + " instruction.\n")
            exit(53)

    def _return(self, IP):
        inst_p = self.callstack._pop()
        inst_p = inst_p + 1
        return inst_p


    #Práce s datovým zásobníkem
    def _pushs(self, IP):
        item = list()

        type_of_symb1 = self.attributes[IP][0][0]
        symb1 = self.attributes[IP][0][1]

        op1_type = ""
        op1_value = ""

        if(type_of_symb1 == "var"):
            check = self._get_frame_and_name(symb1)
            frame = check.group(1)
            name = check.group(2)

            value_type = self._get_value_and_type(frame, name)
            op1_value = value_type[0]
            op1_type = value_type[1]
        elif(type_of_symb1 in ["int", "string", "bool", "nil"]):
            op1_type = type_of_symb1
            op1_value = symb1
        else:
            sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
            exit(53)

        item = [op1_value, op1_type]

        self.datastack._push(item)

    def _pops(self, IP):
        item = self.datastack._pop()
        dest = self.attributes[IP][0][1]

        check = self._get_frame_and_name(dest)
        frame = check.group(1)
        name = check.group(2)

        if(frame == "GF"):
            self.globalframe._actualize(name, item)

        elif(frame == "LF"):
            self.localframe._actualize(name, item)

        elif(frame == "TF"):
            self.temporaryframe._actualize(name, item)

        else:
            sys.stderr.write("Wrond frame in " + str(IP) + ". instruction\n")
            exit(53)

    #Aritmetické, relační, booleovské a konverzní instrukce
    def _math_operations(self, IP, operation):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        type_of_symb2 = self.attributes[IP][2][0]
        symb2 = self.attributes[IP][2][1]

        op1_type = ""
        op1_value = ""
        op2_type = ""
        op2_value = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op1_value = value_type[0]
                op1_type = value_type[1]
            elif(type_of_symb1 in ["int"]):
                op1_type = type_of_symb1
                op1_value = symb1
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(type_of_symb2 == "var"):
                check = self._get_frame_and_name(symb2)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op2_value = value_type[0]
                op2_type = value_type[1]
            elif(type_of_symb2 in ["int"]):
                op2_type = type_of_symb2
                op2_value = symb2
            else:
                sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                exit(53)

            result = 0
            item = []

            try:
                o = int(op1_value[0])
                i = int(op2_value[0])
            except:
                sys.stderr.write("Invalid value\n")
                exit(56)

            if(operation == "add"):
                result = int(op1_value[0]) + int(op2_value[0])
                item = [result, "int"]
            elif(operation == "sub"):
                result = int(op1_value[0]) - int(op2_value[0])
                item = [result, "int"]
            elif(operation == "mul"):
                result = int(op1_value[0]) * int(op2_value[0])
                item = [result, "int"]
            elif(operation == "idiv"):
                if(int(op2_value[0]) == 0):
                    sys.stderr.write("Divide by zero!")
                    exit(57)
                else:
                    result = int(op1_value[0]) / int(op2_value[0])
                    item = [result, "int"]

            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)


    def _add(self, IP):
        self._math_operations(IP, "add")


    def _sub(self, IP):
        self._math_operations(IP, "sub")


    def _mul(self, IP):
        self._math_operations(IP, "mul")


    def _idiv(self, IP):
        self._math_operations(IP, "idiv")


    def _relational_operations(self, IP, operation):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        type_of_symb2 = self.attributes[IP][2][0]
        symb2 = self.attributes[IP][2][1]

        op1_type = ""
        op1_value = ""
        op2_type = ""
        op2_value = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op1_value = value_type[0]
                op1_type = value_type[1]
            elif(type_of_symb1 in ["int", "string", "bool", "nil"]):
                op1_type = type_of_symb1
                op1_value = symb1[0]
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(type_of_symb2 == "var"):
                check = self._get_frame_and_name(symb2)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op2_value = value_type[0]
                op2_type = value_type[1]
            elif(type_of_symb2 in ["int", "string", "bool", "nil"]):
                op2_type = type_of_symb2
                op2_value = symb2[0]
            else:
                sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                exit(53)

            result = 0
            item = []

            if(operation == "lt"):
                if((op1_type == "nil") | (op2_type == "nil")):
                    sys.stderr.write("Type NIL cannot be compared by operation LT.\n")
                    exit(53)
                if(op1_type == op2_type):
                    if(op1_value < op2_value):
                        result = "true"
                    else:
                        result = "false"
                    item = [result, "bool"]
            elif(operation == "gt"):
                if((op1_type == "nil") | (op2_type == "nil")):
                    sys.stderr.write("Type NIL cannot be compared by operation GT.\n")
                    exit(53)
                if(op1_type == op2_type):
                    if(op1_value > op2_value):
                        result = "true"
                    else:
                        result = "false"
                    item = [result, "bool"]
            elif(operation == "eq"):
                if(op1_type == op2_type):
                    if(op1_value == op2_value):
                        result = "true"
                    else:
                        result = "false"
                    item = [result, "bool"]


            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)


    def _lt(self, IP):
        self._relational_operations(IP, "lt")

    def _gt(self, IP):
        self._relational_operations(IP, "gt")

    def _eq(self, IP):
        self._relational_operations(IP, "eq")

    def _logical_operations(self, IP, operation):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]


        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        if(operation != "not"):
            type_of_symb2 = self.attributes[IP][2][0]
            symb2 = self.attributes[IP][2][1]


        op1_type = ""
        op1_value = ""
        op2_type = ""
        op2_value = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)


            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op1_value = value_type[0]
                op1_type = value_type[1]

                if(op1_type != "bool"):
                    sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                    exit(53)

            elif(type_of_symb1 == "bool"):
                op1_type = type_of_symb1
                op1_value = symb1[0]
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(operation != "not"):
                if(type_of_symb2 == "var"):
                    check = self._get_frame_and_name(symb2)
                    frame = check.group(1)
                    name = check.group(2)

                    value_type = self._get_value_and_type(frame, name)
                    op2_value = value_type[0]
                    op2_type = value_type[1]

                    if(op2_type != "bool"):
                        sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                        exit(53)
                elif(type_of_symb2 == "bool"):
                    op2_type = type_of_symb2
                    op2_value = symb2[0]
                else:
                    sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                    exit(53)

            result = 0
            item = []

            if(operation == "and"):
                if( (op1_value[0] == "true") & (op2_value[0] == "true") ):
                    result = "true"
                else:
                    result = "false"
                item = [result, "bool"]
            elif(operation == "or"):
                if( (op1_value[0] == "true") | (op2_value[0] == "true") ):
                    result = "true"
                else:
                    result = "false"
                item = [result, "bool"]
            elif(operation == "not"):
                if(op1_value == "true"):
                    result = "false"
                else:
                    result = "true"
                item = [result, "bool"]


            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)


    def _and(self, IP):
        self._logical_operations(IP, "and")


    def _or(self, IP):
        self._logical_operations(IP, "or")


    def _not(self, IP):
        self._logical_operations(IP, "not")


    def _int2char(self, IP):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        op1_type = ""
        op1_value = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)

                if value_type[1] != "int":
                    sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
                    exit(53)
                op1_value = value_type[0]
                op1_type = value_type[1]
            elif(type_of_symb1 in ["int"]):
                op1_type = type_of_symb1
                op1_value = symb1[0]
            else:
                sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
                exit(53)

            result = 0
            item = []
            if((int(op1_value[0]) >= 0) & (int(op1_value[0]) <= 1114111)):
                result = chr(int(op1_value[0]))
                item = [result, "string"]
            else:
                sys.stderr.write("Invalid value of 1st argument in " + str(IP) + ". instruction\n")
                exit(58)

            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)


    def _stri2int(self, IP):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        type_of_symb2 = self.attributes[IP][2][0]
        symb2 = self.attributes[IP][2][1]

        op1_type = ""
        op1_value = ""
        op2_type = ""
        op2_value = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op1_value = value_type[0]
                op1_type = value_type[1]
            elif(type_of_symb1 in ["string"]):
                op1_type = type_of_symb1
                op1_value = symb1[0]
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(type_of_symb2 == "var"):
                check = self._get_frame_and_name(symb2)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op2_value = value_type[0]
                op2_type = value_type[1]
            elif(type_of_symb2 in ["int"]):
                op2_type = type_of_symb2
                op2_value = symb2[0]
            else:
                sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                exit(53)

            result = 0
            item = []

            try:
                op2_value = int(op2_value[0])
            except:
                sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(op2_value < len(op1_value[0])):
                result = ord(op1_value[0][op2_value])
                item = [result, "int"]
            else:
                sys.stderr.write("Invalid value of 2nd argument in " + str(IP) + ". instruction\n")
                exit(58)

            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)

    #Vstupně-výstupní instrukce
    def _read(self, IP):
        type_of_dest = self.attributes[IP][0][0]
        type_of_symb = self.attributes[IP][1][1]

        if(type_of_dest == "var"):
            dest = self.attributes[IP][0][1]
            check = self._get_frame_and_name(dest)
            frame = check.group(1)
            name = check.group(2)

            try:
                file = open(self.input)
                sys.stdin = file
            except:
                pass

            input_value = ""

            try:
                input_value = input()
            except:
                pass


            input_type = ""


            if(type_of_symb == "int"):
                try:
                    input_type = "int"
                    input_value = int(input_value)
                except ValueError:
                    sys.stderr.write("Invalid READ input\n")
                    exit(57)

            elif(type_of_symb == "string"):
                    input_type = "string"
                    input_value = str(input_value)
            elif(type_of_symb == "bool"):
                try:
                    input_value = str(input_value)
                    input_type == "bool"
                except ValueError:
                    sys.stderr.write("Invalid READ input\n")
                    exit(57)

                if(input_value.lower() == "true"):
                    input_value = "true"
                else:
                    input_value = "false"

            item = [str(input_value), str(input_type)]

            if(frame == "GF"):
                symb = self.globalframe._actualize(name, item)
                symb = str(symb)
            elif(frame == "LF"):
                symb = self.localframe._actualize(name, item)
                symb = str(symb)
            elif(frame == "TF"):
                symb = self.temporaryframe._actualize(name, item)
                symb = str(symb)
            else:
                sys.stderr.write("Wrond frame of argument\n")
                exit(53)


    def _write(self, IP):
        type = self.attributes[IP][0][0]

        if(type == "var"):
            value = self.attributes[IP][0][1]
            check = self._get_frame_and_name(value)
            frame = check.group(1)
            name = check.group(2)

            value_type = self._get_value_and_type(frame, name)
            type = value_type[1]
            try:
                symb = str(value_type[0][0])
            except:
                sys.stderr.write("Invalid value\n")
                exit(57)



        elif((type != "type") | (type != "label")):
            symb = self.attributes[IP][0][1]
        else:
            sys.stderr.write("Wrond type of argument\n")
            exit(53)

        if(type == "nil"):
            print("", end= '')
        elif(type == "bool"):
            print(symb.lower(), end='')
        else:
        #nahradi escape sekvence validnimi bilymi znaky
            symb = re.sub(r"\\([0-9][0-9][0-9])", lambda sign: chr(int(sign.group(1))), symb)
            print(symb, end = '')


    #Práce s řetězci
    def _string_operations(self, IP, operation):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        type_of_symb2 = self.attributes[IP][2][0]
        symb2 = self.attributes[IP][2][1]

        var_type = ""
        var_value = ""
        op1_value = ""
        op1_type = ""
        op2_value = ""
        op2_type = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            if(dest_frame == "GF"):
                var_type = self.globalframe._get_type(dest_name)
                var_value = self.globalframe._get_value(dest_name)
            elif(dest_frame == "LF"):
                var_type = self.localframe._get_type(dest_name)
                var_value = self.localframe._get_value(dest_name)
            elif(dest_frame == "TF"):
                var_type = self.temporaryframe._get_type(dest_name)
                var_value = self.temporaryframe._get_value(dest_name)
            else:
                sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                if(frame == "GF"):
                    op1_type = self.globalframe._get_type(name)
                    op1_value = self.globalframe._get_value(name)
                elif(frame == "LF"):
                    op1_type = self.localframe._get_type(name)
                    op1_value = self.localframe._get_value(name)
                elif(frame == "TF"):
                    op1_type = self.temporaryframe._get_type(name)
                    op1_value = self.temporaryframe._get_value(name)
                else:
                    sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                    exit(53)

            elif((type_of_symb1 == "string") | (type_of_symb1 == "int")):
                op1_type = type_of_symb1
                op1_value = symb1[0]
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(type_of_symb2 == "var"):
                check = self._get_frame_and_name(symb2)
                frame = check.group(1)
                name = check.group(2)

                if(frame == "GF"):
                    op2_type = self.globalframe._get_type(name)
                    op2_value = self.globalframe._get_value(name)
                elif(frame == "LF"):
                    op2_type = self.localframe._get_type(name)
                    op2_value = self.localframe._get_value(name)
                elif(frame == "TF"):
                    op2_type = self.temporaryframe._get_type(name)
                    op2_value = self.temporaryframe._get_value(name)
                else:
                    sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                    exit(53)

            elif((type_of_symb2 == "string") | (type_of_symb2 == "int")):
                op2_type = type_of_symb2
                op2_value = symb2[0]

            else:
                sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                exit(53)

            result = ""
            item = []

            if(operation == "concat"):
                if((op1_type == "string") & (op2_type == "string")):
                    result = op1_value[0] + op2_value[0]
                    item = [result, "string"]
                else:
                    sys.stderr.write("Wrond type of arguments in " + str(IP) + ". instruction\n")
                    exit(53)
            elif(operation == "getchar"):
                if((op1_type == "string") & (op2_type == "int")):
                    index = int(op2_value[0])
                    if(index < len(op1_value[0])):
                        result = op1_value[0][index]
                        item = [result, "string"]
                    else:
                        sys.stderr.write("Wrong index of getchar operation\n")
                        exit(58)
                else:
                    sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                    exit(53)

            elif((operation == "setchar") & (var_type == "string")):
                if((op1_type == "int") & (op2_type == "string")):
                    index = int(op1_value[0])
                    if( (index < len(op2_value[0])) & (len(op2_value[0]) > 0) ):
                        result = var_value[0][:index] + op2_value[0][0] + var_value[0][index+1:]
                        item = [result, "str"]
                    else:
                        sys.stderr.write("Wrong index of setchar operation\n")
                        exit(58)
                else:
                    sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                    exit(53)


            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)

    def _concat(self, IP):
        self._string_operations(IP, "concat")

    def _strlen(self, IP):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        var_type = ""
        var_value = ""
        op1_value = ""
        op1_type = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            if(dest_frame == "GF"):
                var_type = self.globalframe._get_type(dest_name)
                var_value = self.globalframe._get_value(dest_name)
            elif(dest_frame == "LF"):
                var_type = self.localframe._get_type(dest_name)
                var_value = self.localframe._get_value(dest_name)
            elif(dest_frame == "TF"):
                var_type = self.temporaryframe._get_type(dest_name)
                var_value = self.temporaryframe._get_value(dest_name)
            else:
                sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
                exit(53)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                if(frame == "GF"):
                    op1_type = self.globalframe._get_type(name)
                    op1_value = self.globalframe._get_value(name)
                elif(frame == "LF"):
                    op1_type = self.localframe._get_type(name)
                    op1_value = self.localframe._get_value(name)
                elif(frame == "TF"):
                    op1_type = self.temporaryframe._get_type(name)
                    op1_value = self.temporaryframe._get_value(name)
                else:
                    sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                    exit(53)

            elif(type_of_symb1 == "string"):
                op1_value = symb1
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            item = []

            if(op1_value == None):
                result = 0
                item = [result, "int"]
            else:
                result = len(op1_value)
                item = [result, "int"]


            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)

    def _getchar(self, IP):
        self._string_operations(IP, "getchar")

    def _setchar(self, IP):
        self._string_operations(IP, "setchar")

    #Práce s typy
    def _type(self, IP):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        op1_type = ""
        op1_value = ""

        if(type_of_dest == "var"):
            check = self._get_frame_and_name(dest)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)


            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op1_value = value_type[0]
                op1_type = value_type[1]
            elif(type_of_symb1 in ["int", "string", "bool", "nil"]):
                op1_type = type_of_symb1
                op1_value = symb1
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

            item = []

            item = [str(op1_type), str(op1_type)]

            if(dest_frame == "GF"):
                self.globalframe._actualize(dest_name, item)
            elif(dest_frame == "LF"):
                self.localframe._actualize(dest_name, item)
            elif(dest_frame == "TF"):
                self.temporaryframe._actualize(dest_name, item)

    #Instrukce pro řízení toku programu
    def _label(self, IP):
        type = self.attributes[IP][0][0]
        value = self.attributes[IP][0][1]

        if(type == "label"):
           self.labeltable._push_label(value, IP)
        else:
           sys.stderr.write("Wrong type of 1st argument in" + str(IP) + ". instruction\n")
           exit(53)

    def _jump(self, IP):
        value = self.attributes[IP][0][1]
        return self.labeltable._get_label_ip(value)

    def _cond_jump(self, IP, operation):
        type_of_dest = self.attributes[IP][0][0]
        dest = self.attributes[IP][0][1]

        type_of_symb1 = self.attributes[IP][1][0]
        symb1 = self.attributes[IP][1][1]

        type_of_symb2 = self.attributes[IP][2][0]
        symb2 = self.attributes[IP][2][1]

        op1_type = ""
        op1_value = ""
        op2_type = ""
        op2_value = ""

        if(type_of_dest == "label"):
            pass
        else:
            sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
            exit(53)

        if(type_of_symb1 == "var"):
            check = self._get_frame_and_name(symb1)
            frame = check.group(1)
            name = check.group(2)

            if(frame == "GF"):
                op1_type = self.globalframe._get_type(name)
                op1_value = self.globalframe._get_value(name)
                op1_value = op1_value[0]
            elif(frame == "LF"):
                op1_type = self.localframe._get_type(name)
                op1_value = self.localframe._get_value(name)
                op1_value = op1_value[0]
            elif(frame == "TF"):
                op1_type = self.temporaryframe._get_type(name)
                op1_value = self.temporaryframe._get_value(name)
                op1_value = op1_value[0]
            else:
                sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
                exit(53)

        elif(type_of_symb1 in ["int", "string", "bool", "nil"]):
            op1_type = type_of_symb1
            op1_value = symb1

        else:
            sys.stderr.write("Wrond type of 2nd argument in " + str(IP) + ". instruction\n")
            exit(53)

        if(type_of_symb2 == "var"):
            check = self._get_frame_and_name(symb2)
            frame = check.group(1)
            name = check.group(2)

            if(frame == "GF"):
                op2_type = self.globalframe._get_type(name)
                op2_value = self.globalframe._get_value(name)
                op2_value = op2_value[0]
            elif(frame == "LF"):
                op2_type = self.localframe._get_type(name)
                op2_value = self.localframe._get_value(name)
                op2_value = op2_value[0]
            elif(frame == "TF"):
                op2_type = self.temporaryframe._get_type(name)
                op2_value = self.temporaryframe._get_value(name)
                op2_value = op2_value[0]
            else:
                sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
                exit(53)

        elif(type_of_symb2 in ["int", "string", "bool", "nil"]):
            op2_type = type_of_symb2
            op2_value = symb2

        else:
            sys.stderr.write("Wrond type of 3rd argument in " + str(IP) + ". instruction\n")
            exit(53)

        if(operation == "jumpifeq"):
            if(op1_type == op2_type):
                if(op1_value == op2_value):
                    return self.labeltable._get_label_ip(dest)
                else:
                    inst = IP + 1
                    return inst
            else:
                sys.stderr.write("Comparison between different types\n")
                exit(53)

        elif(operation == "jumpifneq"):
            if(op1_type == op2_type):
                if(str(op1_value) == str(op2_value)):
                    inst = IP + 1
                    return inst
                else:
                    return self.labeltable._get_label_ip(dest)
            else:
                sys.stderr.write("Comparison between different types\n")
                exit(53)

    def _jumpifeq(self, IP):
        return self._cond_jump(IP, "jumpifeq")

    def _jumpifneq(self, IP):
        return self._cond_jump(IP, "jumpifneq")

    def _exit(self, IP):
        type = self.attributes[IP][0][0]
        value = self.attributes[IP][0][1]

        if type == "int":
            value = int(value)
            if ((value >= 0) & (value <= 49)):
                exit(value)
            else:
                sys.stderr.write("Invalid value\n")
                exit(57)

        elif(type == "var"):
            check = self._get_frame_and_name(value)
            frame = check.group(1)
            name = check.group(2)

            if(frame == "GF"):
                type = self.globalframe._get_type(name)
                value = self.globalframe._get_value(name)
            elif(frame == "LF"):
                type = self.localframe._get_type(name)
                value = self.localframe._get_value(name)
            elif(frame == "TF"):
                type = self.temporaryframe._get_type(name)
                value = self.temporaryframe._get_value(name)
            else:
                sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
                exit(53)

            if type == "int":
                if("-" not in value[0]):
                    value = int(value[0])
                    if ((value >= 0) & (value <= 49)):
                        exit(value)
                else:
                    sys.stderr.write("Invalid value in 1st argument in " + str(IP) + ". instruction\n")
                    exit(57)

        else:
            sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
            exit(53)



    #Ladící instrukce
    def _dprint(self, IP):
        type_of_symb1 = self.attributes[IP][0][0]
        symb1 = self.attributes[IP][0][1]

        op1_type = ""
        op1_value = ""

        if(type_of_symb1 == "var"):
            check = self._get_frame_and_name(symb1)
            dest_frame = check.group(1)
            dest_name = check.group(2)

            value_type = self._get_value_and_type(dest_frame, dest_name)

            if(type_of_symb1 == "var"):
                check = self._get_frame_and_name(symb1)
                frame = check.group(1)
                name = check.group(2)

                value_type = self._get_value_and_type(frame, name)
                op1_value = value_type[0]
                op1_type = value_type[1]
            elif(type_of_symb1 in ["string"]):
                op1_type = type_of_symb1
                op1_value = symb1
            else:
                sys.stderr.write("Wrond type of 1st argument in " + str(IP) + ". instruction\n")
                exit(53)

            sys.stderr.write(str(op1_value[0])+ "\n")

    def _break(self, IP):
        sys.stderr.write("Actual instruction: " + str(IP) + ".\n")



#Parameter --help
def PrintHelp():
    print("Napoveda ke skriptu interpret.py\n")
    print("Skript nacte XML reprezentaci programu ze zadaneho souboru pomoci STDIO,\n pote interpretuje a nasledne na STDOUT vypise odpovidajici vystup programu.\n")
    print("52 - chyba pri semantickych kontrolach vstupniho kodu v IPPcode19 (napr. pouziti nedefinovaneho navesti")
    print("53 - behova chyba interpretace – spatne typy operandu")
    print("54 - behova chyba interpretace – pristup k neexistujici promenne (ramec existuje)")
    print("55 - behova chyba interpretace – ramec neexistuje (napr. cteni z prazdneho zasobniku ramcu)")
    print("56 - behova chyba interpretace – chybejici hodnota (v promenne, na datovem zasobniku, nebo v zasobniku volani)")
    print("57 - behova chyba interpretace – spatna hodnota operandu (napr. deleni nulou, spatna navratova hodnota instrukce EXIT)")
    print("58 - behova chyba interpretace – chybna prace s retezcem")

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


    processor = Processor(source_f, input_f)
    processor.Interpret()
