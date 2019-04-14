/************************************************************************
 *	IFJ projekt: "Implementace prekladace                       	*
 *				  imperativniho jazyka IFJ18."      	*
 *	Author(s): David Triska (xtrisk05) 	*
 *	Date: 1.12.2018                                            	*
 *	VUT FIT Brno 2BIT                                           	*
 *                                                                  	*
 ************************************************************************/
#ifndef TOKENSTACK_H_INCLUDED
#define TOKENSTACK_H_INCLUDED

#include "token.h"

typedef struct tokenStack{
	struct tokenStackElem* top;
}tokenStack;

typedef struct tokenStackElem{
	Token * data;
	struct tokenStackElem* next;
}ElemStack;


void init_TokStack(tokenStack*);
void push_TokStack(tokenStack*, Token*);
Token* top_TokStack(tokenStack*);
void pop_TokStack(tokenStack*);
void print_TokStack(tokenStack*);
void reverse_TokStack(tokenStack*, tokenStack*);
void copy_TokStack(tokenStack*, tokenStack*);
void empty_TokStack(tokenStack*);
#endif
