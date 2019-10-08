/********************************************************************
 *	IFJ projekt: "Implementace prekladace                       	*
 *				  imperativniho jazyka IFJ18."      				*
 *	Author(s): Daniel Stepanek (xstepa61)                       	*
 *	Date: 29.11.2018                                            	*
 *	VUT FIT Brno 2BIT                                           	*
 *                                                                  *
 *******************************************************************/


#ifndef GENERATOR_H_INCLUDED
#define GENERATOR_H_INCLUDED

#include<stdlib.h>
#include<stdio.h>
#include<stdbool.h>


#include "err_code.h"
#include "parser.h"
#include "dynamic_string.h"



bool generator_start();
void generator_clear_stream();
void generator_output_stream(FILE *);
bool generate_main_end();


bool generate_move(char* , char* );
bool generate_createframe();
bool generate_pushframe();
bool generate_popframe();
bool generate_defvar(char* );
bool generate_call(char* );
bool generate_return();

bool generate_pushs(char* );
bool generate_pops(char* );
bool generate_clears();

bool generate_add(char* , char* , char* );
bool generate_sub(char* , char* , char* );
bool generate_mul(char* , char* , char* );
bool generate_div(char* , char* , char* );
bool generate_idiv(char* , char* , char* );

bool generate_adds(char* , char* , char* );
bool generate_subs(char* , char* , char* );
bool generate_muls(char* , char* , char* );
bool generate_divs(char* , char* , char* );
bool generate_idivs(char* , char* , char* );

bool generate_lt(char* , char* , char* );
bool generate_gt(char* , char* , char* );
bool generate_eq(char* , char* , char* );

bool generate_lts(char* , char* , char* );
bool generate_gts(char* , char* , char* );
bool generate_eqs(char* , char* , char* );

bool generate_and(char* , char* , char* );
bool generate_or(char* , char* , char* );
bool generate_not(char* , char* , char* );

bool generate_ands(char* , char* , char* );
bool generate_ors(char* , char* , char* );
bool generate_nots(char* , char* , char* );

bool generate_int2float(char* , char* );
bool generate_float2int(char* , char* );
bool generate_int2char(char* , char* );
bool generate_stri2int(char* , char* , char* );

bool generate_int2floats(char* , char* );
bool generate_float2ints(char* , char* );
bool generate_int2chars(char* , char* );
bool generate_stri2ints(char* , char* , char* );

bool generate_read(char* , char* );
bool generate_write(char* );
bool generate_new_line();
bool generate_part(char* );

bool generate_concat(char* , char* , char* );
bool generate_strlen();
bool generate_getchar(char* , char* );
bool generate_setchar(char* , char* );

bool generate_type(char* , char* );

bool generate_label(char* );
bool generate_jump(char* );
bool generate_jumpifeq(char* , char* , char* );
bool generate_jumpifneq(char* , char* , char* );

bool generate_jumpifeqs(char* , char* , char* );
bool generate_jumpifneqs(char* , char* , char* );
bool generate_exit(char* );

bool generate_break();
bool generate_dprint(char* );










#endif
