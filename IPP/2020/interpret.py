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
            exit(55)

class Frame():

    def __init__(self):
        self.frame = dict()

    def put_item(self, key, value):
        self.frame[key] = value

    def get_item(self, key):
        if key in self.frame.keys():
            return self.frame[key]
        else:
            return None

    def get_frame(self):
        return self.frame



class Processor():

    def __init__(self, GF, LF, TF):
        self.GF = GF
        self.LF = LF
        self.TF = TF

    def _move(self):
        pass
    def _createframe(self):
        pass
    def _pushframe(self):
        pass
    def _popframe(self):
        pass
    def _defvar(self):
        pass
    def _call(self):
        pass
    def _return(self):
        pass
    def _pushs(self):
        pass
    def _pops(self):
        pass
    def _add(self):
        pass
    def _sub(self):
        pass
    def _mul(self):
        pass
    def _idiv(self):
        pass
    def _lt(self):
        pass
    def _gt(self):
        pass
    def _eq(self):
        pass
    def _and(self):
        pass
    def _or(self):
        pass
    def _not(self):
        pass
    def _int2char(self):
        pass
    def _stri2int(self):
        pass
    def _read(self):
        pass
    def _write(self):
        pass
    def _concat(self):
        pass
    def _strlen(self):
        pass
    def _getchar(self):
        pass
    def _setchar(self):
        pass
    def _type(self):
        pass
    def _label(self):
        pass
    def _jump(self):
        pass
    def _jumpifeq(self):
        pass
    def _jumpifneq(self):
        pass
    def _exit(self):
        pass
    def _dprint(self):
        pass
    def _break(self):
        pass

class Interpret():

    def __init__(self, source_f, input_f):
        self.source_f = source_f
        self.input_f = input_f
        self.GF = Frame()
        self.LF = Frame()
        self.TF = Frame()
        self.instruction_dict = InstructionDict()
        self.processor = Processor(self.GF, self.LF, self.TF)

    def main(self):
        parser = ParseXML()
        instructions = parser.parse(self.source_f)
        instructions = self.syntax(instructions)
        self.runtime(instructions)

    def op_code_switch(self, op_code):
            if 'MOVE' == op_code:
                self.processor._move()
            elif 'CREATEFRAME' == op_code:
                self.processor._createframe()
            elif 'PUSHFRAME' == op_code:
                self.processor._pushframe()
            elif 'POPFRAME' == op_code:
                self.processor._popframe()
            elif 'DEFVAR' == op_code:
                self.processor._defvar()
            elif 'CALL' == op_code:
                self.processor._call()
            elif 'RETURN' == op_code:
                self.processor._return()
            elif 'PUSHS' == op_code:
                self.processor._pushs()
            elif 'POPS' == op_code:
                self.processor._pops()
            elif 'ADD' == op_code:
                self.processor._add()
            elif 'SUB' == op_code:
                self.processor._sub()
            elif 'MUL' == op_code:
                self.processor._mul()
            elif 'IDIV' == op_code:
                self.processor._idiv()
            elif 'LT' == op_code:
                self.processor._lt()
            elif 'GT' == op_code:
                self.processor._gt()
            elif 'EQ' == op_code:
                self.processor._eq()
            elif 'AND' == op_code:
                self.processor._and()
            elif 'OR' == op_code:
                self.processor._or()
            elif 'NOT' == op_code:
                self.processor._not()
            elif 'INT2CHAR' == op_code:
                self.processor._int2char()
            elif 'STRI2INT' == op_code:
                self.processor._stri2int()
            elif 'READ' == op_code:
                self.processor._read()
            elif 'WRITE' == op_code:
                self.processor._write()
            elif 'CONCAT' == op_code:
                self.processor._concat()
            elif 'STRLEN' == op_code:
                self.processor._strlen()
            elif 'GETCHAR' == op_code:
                self.processor._getchar()
            elif 'SETCHAR' == op_code:
                self.processor._setchar()
            elif 'TYPE' == op_code:
                self.processor._type()
            elif 'LABEL' == op_code:
                self.processor._label()
            elif 'JUMP' == op_code:
                self.processor._jump()
            elif 'JUMPIFEQ' == op_code:
                self.processor._jumpifeq()
            elif 'JUMPIFNEQ' == op_code:
                self.processor._jumpifneq()
            elif 'EXIT' == op_code:
                self.processor._exit()
            elif 'DPRINT' == op_code:
                self.processor._dprint()
            elif 'BREAK' == op_code:
                self.processor._break()

            return

    def runtime(self, instructions):
        for instruction in instructions.values():
            self.op_code_switch(instruction[1])


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
