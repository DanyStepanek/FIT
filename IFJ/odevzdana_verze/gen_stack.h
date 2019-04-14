

#ifndef GEN_STACK_H_INCLUDED
#define GEN_STACK_H_INCLUDED

#include "rstring.h"

typedef struct genStack{
	struct genitem* top;
}genStack;

typedef struct genitem{
	RString * str1;
	RString* str2;
	RString* str3;
	int dat_type;
	struct genitem* next;
} genItem;


void init_genStack(genStack*);
void push_genStack(genStack*, char* str1, char* str2, char* str3, int dat_type);
genItem* top_genStack(genStack*);
void pop_genStack(genStack*);
void print_genStack(genStack*);
void reverse_genStack(genStack*, genStack*);
//void copy_genStack(genStack*, genStack*);
void empty_genStack(genStack*);
#endif 
