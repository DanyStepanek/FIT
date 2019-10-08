
//generator jazyka ifj18code
//generator kodu

#include "generator.h"
#include <ctype.h>


#define DYNAMIC_STRING_LENGTH 100

#define ADD_PART(_input)													\
						if(!(dynamic_string_add_const_str(&code, (_input)))) return false

DString code;	//output part of code in IFJ18code

bool generate_header(){

	ADD_PART(".IFJcode18\n");

	ADD_PART("DEFVAR GF@%input_prompt\n");
	ADD_PART("MOVE GF@%input_prompt string@?\\032\n");

	ADD_PART("DEFVAR GF@%tmp1\n");
	ADD_PART("DEFVAR GF@%tmp2\n");
	ADD_PART("DEFVAR GF@%tmp3\n");

	ADD_PART("DEFVAR GF@%ret_val\n");

	ADD_PART("JUMP $$main\n");

	return true;
}



void generator_clear_stream(){
	
	
		dynamic_string_free(&code);
		
}

void generator_output_stream(FILE *outputfile){
	
	fputs(code.string, outputfile);
	generator_clear_stream();
	
}

bool generate_main_header(){
	
	ADD_PART("LABEL $$main\n");
	ADD_PART("CREATEFRAME\n");
	ADD_PART("DEFVAR\n");
	ADD_PART("PUSHFRAME\n");
	
	return true;
}

bool generate_main_end(){
	
	ADD_PART("\nPOPFRAME");
	ADD_PART("\nCLEARS");
	ADD_PART("\nEXIT\n");
	return true;
		
}

bool generator_start(){
	
	if(!dynamic_string_init(&code)) 
		return false;
	if(!(generate_header()))
		return false;
	if(!(generate_main_header()))
		return false;
	
	
	return true;
}

bool generate_move(char* P1, char* P2){
	
	ADD_PART("\nMOVE\t");	ADD_PART(P1);  ADD_PART(" ");		ADD_PART(P2);	ADD_PART("\n");
	return true;
}

bool generate_createframe(){
	ADD_PART("\nCREATEFRAME");
	return true;
}

bool generate_pushframe(){
	ADD_PART("\nPUSHFRAME");
	return true;
}

bool generate_popframe(){
	ADD_PART("\nPOPFRAME");
	return true;
}


bool generate_defvar(char* P1){
	ADD_PART("DEFVAR");	ADD_PART(P1);
	return true;
}

bool generate_call(char* );
bool generate_return();

bool generate_pushs(char* );
bool generate_pops(char* );
bool generate_clears(){
	ADD_PART("CLEARS\n");
	return true;
}

bool generate_part(char* P1){
	ADD_PART(P1);
	return true;
}

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
bool generate_write(char* P1){
	ADD_PART("WRITE\t");	ADD_PART(P1);
	
	return true;
}

bool generate_new_line(){
	ADD_PART("\n");
	
	return true;
}	
	
bool generate_concat(char* , char* , char* );
bool generate_strlen(){
	ADD_PART("\nLABEL $length");	ADD_PART("\nPUSHFRAME");	ADD_PART("\nDEFVAR LF@ret_val");
	ADD_PART("\nSTRLEN LF@ret_val LF@%0");	ADD_PART("\nPOPFRAME");	ADD_PART("\nRETURN");

return true;
}

bool generate_getchar(char* , char* );
bool generate_setchar(char* , char* );

bool generate_type(char* , char* );

bool generate_label(char* P1){
	ADD_PART("LABEL $$");	ADD_PART(P1);
	return true;
}

bool generate_jump(char* );
bool generate_jumpifeq(char* , char* , char* );
bool generate_jumpifneq(char* , char* , char* );

bool generate_jumpifeqs(char* , char* , char* );
bool generate_jumpifneqs(char* , char* , char* );
bool generate_exit(char* );

bool generate_break();
bool generate_dprint(char* );


