#include "parser.h"


#define RELEASE free_Token(token)
#define CONTENT token->value->string
#define parser_CONTENT p_data->token.value->string

//types used below
#define	NIL	0
#define 	NUMBER	1
#define 	NUMBER_DOUBLE	2
#define 	IDENTIFIER	3 
#define 	KEYWORD	4
#define 	OPERATOR	5
#define 	STRING	6
#define 	EOL	7
#define 	tEOF	8

#define	CONSTANT	0
#define	VARIABLE	1
#define	FUNCTION	2

#define	LEXICAL_ERROR 20
#define	SYNTAX_ERROR 40
#define	SEMANTIC_ERROR 60
#define	INTERNAL_ERROR 80


//add one token to output code
#define	ADD_CODE(P1)	generate_part(P1)

#define	GET_TOKEN	\
		type = get_token();	\
		if(type == LEXICAL_ERROR || type < 0) exit(LEXICAL_ERROR);	\
		strcpy(p_data->token.value->string, token->value->string);	\
		RELEASE;	
		
#define	CHECK_TYPE(type)	\
	if(token->id != (type)) return SYNTAX_ERROR	;
	
#define	CHECK_DECLARATION(node,name)	\
		if((find_Node(node,name)) == NULL)		return SEMANTIC_ERROR;


//Rules
#define E 0	//equal
#define R 1	//reduce
#define S 2	//shift
#define F 3	//failure



int precedence_table[8][8] = {//+-. */,  \ ,  r, (,  ),   i  , $
												{ R , S, S, R, S, R, S, R},	// +-
												{ R , R, R, R, S, R, S, R},	//	*/
												{ R , S, R, R, S, R, S, R},	//	\ /
												{ S , S, S, F, S, R, S, R},	//	== <> < <= > >=
												{ S , S, S, S, S, E, S, F},	//	(
												{ R , R, R, R, F, R, F, R},	//	)
												{ R , R, R, R, F, R, F, R},	//	id, integer, double, string
												{ S , S, S, S, S, F, S, F}	//	special sign "$"
};


typedef struct parser_data{

	Node* global_frame;	//pointer to global symbol table
	Node* local_frame;		//pointer to local symbol table
		
	Token token;	
	
	char* actual_func;
	
	bool function;		// in function or not
	bool while_stat;	//while or if <stat>
	bool if_stat;
	bool defined;		//defined id
	bool declare;		//declared id
} Parser_data;



Parser_data* init_parse_data(Parser_data *p_data){
	
	p_data = malloc(sizeof(struct parser_data));
	p_data->actual_func = calloc(1000,sizeof(char));
	p_data->token.value = init_RString();
	p_data->token.value->string = calloc(1000, sizeof(char));
	Node_init(&(p_data->global_frame));
	Node_init(&(p_data->local_frame));
	p_data->function = false;
	p_data->while_stat = false;
	p_data->if_stat = false;
	p_data->declare = false;
	
	return p_data;
}

void free_parse_data(Parser_data *p_data){
	
	free(p_data->token.value->string);
	free(p_data->token.value);
	Tree_delete(&(p_data->global_frame));
	Tree_delete(&(p_data->local_frame));
	free(p_data->actual_func);
	free(p_data);
	p_data = NULL;
}

tokenStack* init_token_stack(tokenStack* stack){
	
	stack = malloc(sizeof(struct tokenStack));
	init_TokStack(stack);
	
	
	return stack;
}

void free_token_stack(tokenStack* stack){

	empty_TokStack(stack);
	free(stack);
}

/*********************************************************************/

int prog_(Parser_data* );
int assign_(Parser_data* );
int write_(Parser_data* );
int stat_(Parser_data* );
int type_(Parser_data* );
int expr_(Parser_data* );
int item_(Parser_data* );
void generateInstruction(int , char* , char* );


/*********************Global variables*****************************/

char* var;
char* label;
char* symb1;
char* symb2;
int type;
tokenStack* global_stack;
tokenStack* local_stack;
tokenStack* tmp_stack;


/********************Syntax analysis******************************/


int type_(Parser_data* p_data){

	Node* tmpNode;
	
	if((tmpNode = find_Node(&p_data->global_frame, CONTENT))!= NULL){
		if(tmpNode->data->defined)
			return tmpNode->data->id;
		else return NIL;
	}
	else {
		call_error(SEMANTIC_ERROR, SEMANTIC_ERROR);
		exit(4);
	}	
	
	

}

int expr_(Parser_data* p_data){

	
	push_TokStack(local_stack, &p_data->token);
	GET_TOKEN;
	
	switch(type){
		
		case NUMBER: case NUMBER_DOUBLE: case IDENTIFIER:
					
			push_TokStack(local_stack, &p_data->token);
			
			GET_TOKEN;
			
			if((p_data->if_stat) && strcmp(p_data->token.value->string, "then") == 0){
	
				push_TokStack(local_stack, &p_data->token);
				
				return type;
				
			}
			else if((p_data->if_stat)){
	
				push_TokStack(local_stack, &p_data->token);
				expr_(p_data);
				
								
			}
			else if((p_data->while_stat) && strcmp(p_data->token.value->string, "do") == 0){
				
				push_TokStack(local_stack, &p_data->token);
				
				return type;
			
			}			
			else if((p_data->while_stat)){
	
				push_TokStack(local_stack, &p_data->token);
				expr_(p_data);
				
								
			}
			else if(type == EOL && ((!p_data->if_stat) || (!p_data->while_stat))){
				//generate_move
				
			}
			else if(type == EOL){
				if(p_data->function)
					empty_TokStack(local_stack);
				else
					empty_TokStack(global_stack);
				//generate_move()
				
			}
			else if(type == OPERATOR){
				push_TokStack(local_stack, &p_data->token);
			
				GET_TOKEN;
					if((strcmp(top_TokStack(local_stack)->value->string,"/") == 0) && atoi(p_data->token.value->string) == 0){
						call_error(SEMANTIC_ERROR,SEMANTIC_ERROR);
						exit(4);	//div by zero
					}	

				expr_(p_data);
				
			}
			else if(strcmp(p_data->token.value->string, "=")==0){
				push_TokStack(local_stack, &p_data->token);
				GET_TOKEN;
				stat_(p_data);
			}
			
	//		else {
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
				
//			}
			
		break;
		
		
		case KEYWORD:
			if((strcmp(p_data->token.value->string, "def")!= 0) || (strcmp(p_data->token.value->string, "if")!= 0) ||
				(strcmp(p_data->token.value->string, "while")!= 0) || (strcmp(p_data->token.value->string, "return")!= 0) ||
				(strcmp(p_data->token.value->string, "print")!= 0)){
					
				stat_(p_data);
			
			
			}		
	//		else {
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
//			}
			
		break;
		
		
//		default:
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
		
		
		
		
	}


	return 0;
}

int write_(Parser_data *p_data){

		GET_TOKEN;
		
		if(type != EOL && (strcmp(parser_CONTENT, "(") != 0)){
			
			push_TokStack(local_stack, &p_data->token);
			item_(p_data);
			
			GET_TOKEN;
			if(type == EOL || (strcmp(parser_CONTENT, ")") == 0)){
				//generate_write()
				return 0;
			}	
			else if((strcmp(parser_CONTENT, ",") != 0)){
				push_TokStack(local_stack, &p_data->token);
				write_(p_data);
			
			}
		}
		else if((strcmp(parser_CONTENT, "(") != 0)){
			push_TokStack(local_stack, &p_data->token);
			write_(p_data);
		
		}
		else {
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
		}
	return 0;
}


int prog_(Parser_data * p_data){

	do {	
		
		GET_TOKEN;
		
		switch(type){
			
			case KEYWORD: case IDENTIFIER:
				stat_(p_data);
			break;
			
			case EOF: case EOL:
			
			break;
			
//			default:
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
			
			
		}	//end of switch
				

		
	}  while (type != tEOF);

	return 0;
}

int item_(Parser_data* p_data){

	
	switch(type){
		
		case KEYWORD:
			if(strcmp(p_data->actual_func,"inputi")== 0){
				//read integer
			}	
			else if(strcmp(p_data->actual_func,"inputf")== 0){
				//read float
			}
			else if(strcmp(p_data->actual_func,"inputs")== 0){
				//read string
			}
		break;
		
		case IDENTIFIER:
			return type_(p_data);
		break;
		
		case NUMBER: case NUMBER_DOUBLE: case STRING:
		//generate_item()
			return type;
		break;
		
//		default:
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
		
	}
	
	return 0;
}

int assign_(Parser_data* p_data){
	
	Node * tmpNode;
	

	switch(type){
		
		case KEYWORD: 
			if((strcmp(p_data->token.value->string, "def")!= 0) || (strcmp(p_data->token.value->string, "if")!= 0) ||
				(strcmp(p_data->token.value->string, "while")!= 0) || (strcmp(p_data->token.value->string, "return")!= 0) ||
				(strcmp(p_data->token.value->string, "print")!= 0)){
					
				GET_TOKEN;
				stat_(p_data);
					
			}
			else {
//				call_error(SYNTAX_ERROR, SYNTAX_ERROR);
//				exit(2);
			}
			
		break;
		
		case IDENTIFIER:	case NUMBER:	case NUMBER_DOUBLE:
			generate_part(" ");
			if(type == NUMBER){
				if((tmpNode = find_Node(&p_data->global_frame, p_data->token.value->string))!= NULL){
					Node_actualize(&tmpNode, type, &p_data->token);
				}
	
				generate_part("int@");
				generate_part(parser_CONTENT);
				
				GET_TOKEN;
				if(type == EOL){
				generate_part("\n");
				}
				else if(type == OPERATOR){
					assign_(p_data);
				}
				
			}	
			else if(type == NUMBER_DOUBLE){
				if((tmpNode = find_Node(&p_data->global_frame, p_data->token.value->string))!= NULL){
					Node_actualize(&tmpNode, type, &p_data->token);
				}
				
				generate_part("double@");
			
				generate_part(parser_CONTENT);
				
				GET_TOKEN;
				if(type == EOL){
				generate_part("\n");
				}
		
			}
			else if(type == OPERATOR){
			generate_part("\n");
				GET_TOKEN;
				expr_(p_data);
				
			}
			else if(strcmp(p_data->token.value->string, "=")==0){
				generate_part(parser_CONTENT);
				GET_TOKEN;
				stat_(p_data);
			}
	//		else{
	//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//			exit(2);
				
//			}
		break;
		
///		default:	//eol eof operator
//			call_error(SYNTAX_ERROR, SYNTAX_ERROR);
//			exit(2);
			
	
	}
	
	return 0;
	
}
/************BUILT-IN FUNCTION*************************************/

int length(Parser_data* p_data){
	GET_TOKEN;
			if(strcmp(parser_CONTENT, "(") == 0){
				GET_TOKEN;
				if(type == IDENTIFIER){
						
					Node * tmpNode;
			
					if(p_data->function){
						if((tmpNode = find_Node(&p_data->local_frame, p_data->token.value->string))!= NULL){
							if(tmpNode->data->id == STRING){
							//gen_length
							return 0;
							}	
								else{
								call_error(SEMANTIC_ERROR,SEMANTIC_ERROR);
								exit(4);
								}
						}
							else{
								call_error(SEMANTIC_ERROR,SEMANTIC_ERROR);
								exit(4);
								}
					
					}
					else{
						if((tmpNode = find_Node(&p_data->global_frame, p_data->token.value->string))!= NULL){
							if(tmpNode->data->id == STRING){
								return 0;
							}	
							else{
								call_error(SEMANTIC_ERROR,SEMANTIC_ERROR);
								exit(4);
								}
						}
						else{
							call_error(SEMANTIC_ERROR,SEMANTIC_ERROR);
							exit(4);
						}
					}
				
				}
			
			}
			else if(type == STRING){
					
					GET_TOKEN;
					if(strcmp(parser_CONTENT, ")") == 0)
						return 0;
					else{
//						call_error(SYNTAX_ERROR,SYNTAX_ERROR);
//						exit(2);
					}
			}
			else{
				call_error(SEMANTIC_ERROR,SEMANTIC_ERROR);
				exit(4);
			}
		
	return 0;
}
	

int stat_(Parser_data* p_data){

	if(type == KEYWORD){
		
			//<stat> -> def id <param>
		if(strcmp(parser_CONTENT, "def") == 0){
			//generate_substr()
			GET_TOKEN;
			p_data->function = true;
			
			Node * tmpNode;
				
			if((tmpNode = find_Node(&p_data->global_frame, p_data->token.value->string))!= NULL){
					Node_create(&p_data->global_frame, type, &p_data->token);
			}
		
			stat_(p_data);
		
		}
		//<stat> -> input<item>
		else if((strcmp(parser_CONTENT, "inputi") == 0) || (strcmp(parser_CONTENT, "inputf") == 0) ||
		   (strcmp(parser_CONTENT, "inputs") == 0)){
			//generate_read()
			strcpy(p_data->actual_func, parser_CONTENT);
			item_(p_data);
		}
		
		//<stat> -> print<item> <item_list>
		else if(strcmp(parser_CONTENT, "print") == 0){
			
		//	strcpy(p_data->actual_func, parser_CONTENT);	
			
		//	write_(p_data);	
			
			

		
		}
		//<stat> ->  length<item>
		else if(strcmp(parser_CONTENT, "length") == 0){
			strcpy(p_data->actual_func, parser_CONTENT);
			length(p_data);
			generate_strlen();
			
		}
		//<stat> -> substr<param>
		else if(strcmp(parser_CONTENT, "substr") == 0){
			//generate_substr()


		}
		//<stat> -> ord<item>
		else if(strcmp(parser_CONTENT, "ord") == 0){
			strcpy(p_data->actual_func, parser_CONTENT);
			//generate_ord()
			

		}
		//<stat> -> chr<item>
		else if(strcmp(parser_CONTENT,  "chr") == 0){
			strcpy(p_data->actual_func, parser_CONTENT);
			GET_TOKEN;
			item_(p_data);
			//generate_chr()

		}
		//<stat> -> if<expr> then EOL <st_list> else EOL <st_list> end EOL
		else if(strcmp(parser_CONTENT, "if") == 0){
			Token* tmpToken = init_Token();
			p_data->if_stat = true;
			if(p_data->function){
				push_TokStack(local_stack, &p_data->token);
				GET_TOKEN;
				push_TokStack(local_stack, &p_data->token);
				
				GET_TOKEN;				
				expr_(p_data);
			
				if((tmpToken = top_TokStack(local_stack))!= NULL)
					if((strcmp(tmpToken->value->string, "then")) != 0){
	//					call_error(SYNTAX_ERROR,SYNTAX_ERROR);
	//					exit(2);
					}
			}
			else {
				push_TokStack(global_stack, &p_data->token);
				GET_TOKEN;
				push_TokStack(global_stack, &p_data->token);
				
				GET_TOKEN;
				expr_(p_data);
			
			if((tmpToken = top_TokStack(global_stack))!= NULL)
				if((strcmp(tmpToken->value->string, "then")) != 0){
				
	//				call_error(SYNTAX_ERROR,SYNTAX_ERROR);
//					exit(2);
				}
					
			}
			
			

		}
		//<stat> -> while<expr> do EOL <st_list> end EOL
		else if(strcmp(parser_CONTENT, "while") == 0){
			Token* tmpToken;
			p_data->while_stat = true;
			if(p_data->function){
				push_TokStack(local_stack, &p_data->token);
				GET_TOKEN;
				push_TokStack(local_stack, &p_data->token);
				
				GET_TOKEN;				
				expr_(p_data);
			
				if((tmpToken = top_TokStack(local_stack))!= NULL){
					if((strcmp(tmpToken->value->string, "then")) != 0){
	//					call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//					exit(2);
					}
					
				}
				else {
	//				call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//				exit(2);
				}
			
			}
			else {
				push_TokStack(global_stack, &p_data->token);
				GET_TOKEN;
				push_TokStack(global_stack, &p_data->token);
				
				GET_TOKEN;
				expr_(p_data);
			
				if((tmpToken = top_TokStack(global_stack))!= NULL){
					if((strcmp(tmpToken->value->string, "then")) != 0){
	//					call_error(SYNTAX_ERROR, SYNTAX_ERROR);
	//					exit(2);
					}
				}
				else {
					call_error(SYNTAX_ERROR, SYNTAX_ERROR);
					exit(2);
				}


			}
		}
			//<stat> -> return <expr>
		else if(strcmp(parser_CONTENT, "return") == 0){
			//generate_substr()


		}
		//<stat> -> end
		else if(strcmp(parser_CONTENT, "end") == 0){
			
			if((!p_data->if_stat) && (!p_data->while_stat)){
				if(p_data->function){
					empty_TokStack(local_stack);
					p_data->function = false;
				}
				else {
					empty_TokStack(global_stack);
				}
			}
			else {
				p_data->if_stat = false;
				p_data->while_stat = false;
			}
		
		}
		
		
	}	//end of keyword
	else if(type == IDENTIFIER){
		
		Node * tmpNode;
		
			
			if(p_data->function){
				if((tmpNode = find_Node(&p_data->local_frame, p_data->token.value->string))!= NULL)
					Node_create(&p_data->local_frame, type, &p_data->token);
					
				push_TokStack(local_stack, &p_data->token);
				
			}
			else{
				if((tmpNode = find_Node(&p_data->global_frame, p_data->token.value->string))!= NULL)
					Node_create(&p_data->global_frame, type, &p_data->token);
				
				push_TokStack(global_stack, &p_data->token);
				
				
			}
			
			
		
		GET_TOKEN;
		
		//<stat> -> id = <assign>	
		if(strcmp(p_data->token.value->string, "=")== 0){
			generate_part("\nMOVE\t");
			if(p_data->function){
				generate_part("LF@");
				generate_part(top_TokStack(local_stack)->value->string);
			}
			else {
				generate_part("GF@");
				generate_part(top_TokStack(global_stack)->value->string);
			}
			
			GET_TOKEN;
			assign_(p_data);
		}	
		
	}
		
	
	
	
	return 0;
}

int syntax(){
	
	global_stack = init_token_stack(global_stack);
	local_stack = init_token_stack(local_stack);
	tmp_stack = init_token_stack(tmp_stack);
	
	var = (char*) malloc(100);
	label = (char*) malloc(100);
	symb1 = (char*) malloc(100);
	symb2 = (char*) malloc(100);
	type = 0;

	
	
	Parser_data *p_data = NULL;
	p_data = init_parse_data(p_data);
	
	
	
	if(!generator_start()) return -1;

	
	//<prog> -> begin
	if((prog_(p_data))!= 0){
		call_error(SYNTAX_ERROR, INTERNAL_ERROR);
		
		free(var);
		free(symb1);
		free(symb2);
		free(label);
	
	
		free_parse_data(p_data);
	
		free_token_stack(global_stack);
		free_token_stack(local_stack);
		free_token_stack(tmp_stack);
	
		generate_main_end();
		generator_clear_stream();
		return 2;
	}
	else {

		free(var);
		free(symb1);
		free(symb2);
		free(label);
		
		free_parse_data(p_data);
		
		free_token_stack(global_stack);
		free_token_stack(local_stack);
		free_token_stack(tmp_stack);
		
		generate_main_end();

		return 0;
	}



}

	
	

