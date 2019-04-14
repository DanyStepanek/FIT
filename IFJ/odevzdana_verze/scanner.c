

#include "scanner.h"

#define LEXICAL_ERROR 20

typedef enum{
	sSTART,
	sNUMBER,
	sNUMBER_DOUBLE,
	sIDENTIFIER,
	sKEYWORD,
	sOPERATOR,
	sSTRING,
	sEOL,
	sEOF,
	sLINE_COMMENT,
	sBLOCK_COMMENT,
	sERROR

} State;

int isKeyWord(char *str){
	if(strcmp("def",str)==0)
		return DEF;
	if(strcmp("do",str)==0)
		return DO;
	if(strcmp("else",str)==0)
		return ELSE;
	if(strcmp("end",str)==0)
		return END;
	if(strcmp("if",str)==0)
		return IF;
	if(strcmp("not",str)==0)
		return NOT;
	if(strcmp("nil",str)==0)
		return NIL;
	if(strcmp("then",str)==0)
		return THEN;
	if(strcmp("while",str)==0)
		return WHILE;
	if(strcmp("=begin",str)==0)
		return BEGINC;
	if(strcmp("=end",str)==0)
		return ENDC;
	if(strcmp("begin",str)==0)
		return BEGIN;
	if(strcmp("inputi",str)==0)
		return INPUTI;
	if(strcmp("inputf",str)==0)
		return INPUTF;
	if(strcmp("inputs",str)==0)
		return INPUTS;
	if(strcmp("print",str)==0)
		return PRINT;
	if(strcmp("length",str)==0)
		return LENGTH;
	if(strcmp("substr",str)==0)
		return SUBSTR;
	if(strcmp("ord",str)==0)
		return ORD;
	if(strcmp("chr",str)==0)
		return CHR;
	if(strcmp("return",str)==0)
		return RETURN;
	
	
	return -1;	//if "str" is not a keyword
}

int variables(char *buffer){
	int keyword = -1;

	//keyword checking
	keyword = isKeyWord(buffer);
	enum defaultWords key = keyword;
	
	switch (key){

	case 0:
		buffer = "def";
		break;
	case 1:
		buffer = "do";
		break;
	case 2:
		buffer = "else";
		break;
	case 3:
		buffer = "end";
		break;
	case 4:
		buffer = "if";
		break;
	case 5:
		buffer = "not";
		break;
	case 6:
		buffer = "nil";
		break;
	case 7:
		buffer = "then";
		break;
	case 8:
		buffer = "while";
		break;
	case 9:
		buffer = "=begin";
		break;
	case 10:
		buffer = "=end";
		break;
	case 11:
		buffer = "begin";
		break;
	case 12:
		buffer = "inputi";
		break;
	case 13:
		buffer = "inputf";
		break;
	case 14:
		buffer = "inputs";
		break;
	case 15:
		buffer = "print";
		break;
	case 16:
		buffer = "length";
		break;
	case 17:
		buffer = "substr";
		break;
	case 18:
		buffer = "ord";
		break;
	case 19:
		buffer = "chr";
		break;
	case 20:
		buffer = "return";
		break;
		
	}

	return keyword;
		
}

Token* createToken(char *buffer, int t){
	int size = 0;
	token = init_Token();
	
	for(int i=0;buffer[i]!='\0';i++){
		size++;
	}
		
	fill_Token(token, buffer, size, t);

	return 0;
}


int get_token(){
	
	bool sign_double = false;	//voluntary sign (number_double)
	bool e_E_dot = false;	//if number is double
	
	int buf_len = BUFFER_SIZE;
	char curr_char = '\0';
	static char prev_char;
	int control = sSTART;
	int i = 0;
	
	while(1){
		
		if(control == sSTART && prev_char != curr_char)
			curr_char = prev_char;
		else
			curr_char = getchar();
	
		switch(control){
			//CREATE NEW TOKEN
			case sSTART:
				
				if(lines == 0)	lines++;
				
				if(islower(curr_char) || curr_char == '_'){
					prev_char = curr_char;
					buffer[i++] = curr_char;
					control = sIDENTIFIER;
				}
	
				else if(isdigit(curr_char)){
					prev_char = curr_char;
					buffer[i++] = curr_char;
					control = sNUMBER;
				}
			
				else if(curr_char == '"'){
						control = sSTRING;
				}
				
				else if(curr_char == '#'){	
					prev_char = curr_char;
					control = sLINE_COMMENT;
				}
				
				else if(ispunct(curr_char) && curr_char != '_' && curr_char != '#' && curr_char != '"'){
					prev_char = curr_char;
					buffer[i++] = curr_char;
					control = sOPERATOR;
				}
				
				else if(curr_char == EOF){
					control = sEOF;
				}
				
				else if(curr_char == '\n'){
				
					control = sEOL;
				}
				
				else if(isspace(curr_char)){
					prev_char = curr_char;
					control = sSTART;
				}
				
				else {
					call_error(LEXICAL_ERROR,sERROR);
					return -lines;
				}
			
			break;
				
	
			case sNUMBER:
				if(isdigit(curr_char)){
					buffer[i++] = curr_char;
					prev_char = curr_char;
				
				}
				else if(curr_char == 'e' || curr_char == 'E' || curr_char == '.'){
					buffer[i++] = curr_char;
					control = sNUMBER_DOUBLE;
					e_E_dot = true;
				}	
				else if(curr_char == '\n' || (isspace(curr_char)) || ispunct(curr_char)){
					buffer[i] = '\0';
					
					if((atof(buffer)) > INT_MAX){
						call_error(LEXICAL_ERROR, sNUMBER);
						return -lines;
					}
					
					createToken(buffer, sNUMBER);
				//	printf("vytvoril jsem token %s \n",token->value->string);
					prev_char = curr_char;
								
					return sNUMBER;
				}
				else {	//LEXICAL_ERROR
					call_error(LEXICAL_ERROR, sNUMBER);
					return -lines;
				}	
					
			break;
			
			case sNUMBER_DOUBLE:
				if(isdigit(curr_char)){
					buffer[i++] = curr_char;
					prev_char = curr_char;
				}
				else if((curr_char == '+' || curr_char == '-' ) && sign_double == false && e_E_dot == true){
					sign_double = true;
					buffer[i++] = curr_char;
				}		
				else if((curr_char == '\n' || (isspace(curr_char)) || ispunct(curr_char)) &&
							(prev_char != 'e' || prev_char != 'E' || prev_char != '.')){
					buffer[i] = '\0';
					createToken(buffer, sNUMBER_DOUBLE);
				//	printf("vytvoril jsem token %s \n",token->value->string);
					prev_char = curr_char;
					return sNUMBER_DOUBLE;
				}
				else {	//LEXICAL_ERROR
					call_error(LEXICAL_ERROR,sNUMBER_DOUBLE);
					return -lines;
				}	
								
			break;
			
			case sIDENTIFIER:
					if(curr_char != '\n' && !(isspace(curr_char)) && !(ispunct(curr_char))){
						buffer[i++] = curr_char;
			
					}
					else if(curr_char == '_'){
						buffer[i++] = curr_char;
					}
					else {
						buffer[i] = '\0';
						//	printf("vytvoril jsem token %s \n",token->value->string);
						prev_char = curr_char;
					
						int isKeyword = variables(buffer);
			
						if(isKeyword == -1 ){
							createToken(buffer, sIDENTIFIER);
							return sIDENTIFIER;
						}	
						else {
							createToken(buffer, sKEYWORD);
							return sKEYWORD;
						}
		
						
					}
			break;
			
			case sOPERATOR:
				if((prev_char == '<' || prev_char == '>') && curr_char == '=' && i <= 1)
					buffer[i++] = curr_char;
				else if(prev_char == '=' && (curr_char == '=' || curr_char == '!') && i <= 1){
					buffer[i++] = curr_char;
				}	
				else if(prev_char == '!' && (curr_char == '=') && i <= 1){
					buffer[i++] = curr_char;
				}	
				else if(!(ispunct(curr_char)) || curr_char == '"'){
					buffer[i] = '\0';
					createToken(buffer, sOPERATOR);
				//	printf("vytvoril jsem token %s \n",token->value->string);
					prev_char = curr_char;
					return sOPERATOR;
				}	
				else {
					call_error(LEXICAL_ERROR,sOPERATOR);
					return -lines;
				}	
				
				
			break;
			
			case sSTRING:
				if(curr_char != '"' && curr_char != '\n')
					buffer[i++] = curr_char;
				else if(curr_char == '"'){
					buffer[i] = '\0';
					createToken(buffer, sSTRING);
				//	printf("vytvoril jsem token %s \n",token->value->string);
					
					prev_char = '\0';
					
					return sSTRING;
				}
				else if(curr_char == '\n'){
					call_error(2,sSTRING);
					return -lines;
				}	
									
			break;
			
			case sEOF:
				if(curr_char == EOF){
					createToken("EOF",sEOF);
				//	printf("vytvoril jsem token %s \n",token->value->string);
					
					return sEOF;
				}
			break;
			
			case sEOL:			
					createToken("EOL",sEOL);
				//	printf("vytvoril jsem token %s \n",token->value->string);
					prev_char = curr_char;
					lines++;
					return sEOL;
				
				
			break;
			
			case sLINE_COMMENT:
				if(curr_char == '\n'){
					prev_char = curr_char;
					control = sSTART;
				}
				else if(curr_char == EOF)
					control = sEOF;
			
			break;
			
			case sBLOCK_COMMENT:

			break;
		
		}	//end of switch
		

		if((i+1) >= buf_len){
			buffer = realloc(buffer,sizeof(char)*50 + buf_len);
						buf_len += 50;
		}			
	
	}	//end of while
	
	
	return sSTART;
}
