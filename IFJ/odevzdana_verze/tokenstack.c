#include "tokenstack.h"


void init_TokStack(tokenStack* stack){

	stack->top = NULL;

}

void push_TokStack(tokenStack* stack, Token* inTok){

	ElemStack* newEl = malloc(sizeof(ElemStack));
		
	if(newEl == NULL){
		fprintf(stderr, "TokenSTUCK chyba alokace, push_TokStack():12 \n");
		return;
	}

	newEl->data = init_Token();
	fill_Token(newEl->data, inTok->value->string, inTok->value->size, inTok->id);
	newEl->next = NULL;

	if(stack->top == NULL){
		stack->top = newEl;
	}else{

		newEl->next = stack->top;
		stack->top = newEl;

	}

}

void pop_TokStack(tokenStack* stack){

	if(stack->top != NULL){

		ElemStack* help = stack->top;

		if(help->next == NULL){
			free_Token(help->data);
			free(help);
			stack->top = NULL;
		
		}else{

			stack->top = help->next;
			free_Token(help->data);
			free(help);
		}

	}

}

Token* top_TokStack(tokenStack*stack){

	if( stack->top != NULL){
		return stack->top->data;
	}else{
		return NULL;
	}


}

void empty_TokStack(tokenStack* stack){
	
	while(stack->top != NULL){
		pop_TokStack(stack);
	}
}


void print_TokStack(tokenStack* s){

	ElemStack* help = s->top;
	int i = 0;
	while(help != NULL){
		printf("%d) Vypis zasobniku: %s value, %d idType\n", i, help->data->value->string, help->data->id);
		help = help->next;
		i++;
	}


}

void reverse_TokStack(tokenStack* in, tokenStack* out){

	Token * tok;
	while(in->top != NULL){

		tok = top_TokStack(in);
		pop_TokStack(in);
		push_TokStack(out, tok);
		free_Token(tok);
	}


}

void copy_TokStack(tokenStack* in, tokenStack* out){

	tokenStack tmp; init_TokStack(&tmp);
	Token* token;

	while(in->top != NULL){
		token = top_TokStack(in);
		push_TokStack(out, token);
		push_TokStack(&tmp, token);
		pop_TokStack(in);
		free_Token(token);
	}

	reverse_TokStack(&tmp, in);
	//empty_TokStack(&tmp);
}

