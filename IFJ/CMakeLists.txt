cmake_minimum_required(VERSION 3.15)
project(IFJ2019 C)

set(CMAKE_C_STANDARD 11)

include_directories(.)

add_executable(IFJ2019
        dynamic_string.c
        dynamic_string.h
        err_code.c
        err_code.h
        expression.c
        expression.h
        generator.c
        generator.h
        generator_j.c
        generator_j.h
        list.c
        list.h
        main.c
        other_functions.c
        other_functions.h
        parser.c
        parser.h
        scanner.c
        scanner.h
        stack.c
        stack.h
        symtable.c
        symtable.h)
