/********************************************************************
 *	IFJ projekt: "Implementace prekladace                       *
 *				  imperativniho jazyka IFJ18."      *
 *	Author(s): Daniel Stepanek (xstepa61)                       *
 *	Date: 11.10.2018                                            *
 *	VUT FIT Brno 2BIT                                           *
 *                                                                  *
 *******************************************************************/
 
#ifndef SCANNER_H_INCLUDED
#define SCANNER_H_INCLUDED

#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
#include<string.h>
#include<limits.h>
#include<stdbool.h>

#include "tlist.h"
#include "err_code.h"


#define BUFFER_SIZE 100



FILE *file;
char *buffer;
Token *token;	//token for parser
int lines;


enum defaultWords{
	DEF,	//0
	DO,	
	ELSE,
	END,
	IF,
	NOT,
	NIL,
	THEN,
	WHILE,
	BEGINC,	//begin multiline comment
	ENDC,	//end multiline comment
	BEGIN,
	INPUTI,
	INPUTF,
	INPUTS,
	PRINT,
	LENGTH,
	SUBSTR,
	ORD,
	CHR,
	RETURN
	
};




//Functions definitons
Token* createToken(char *, int );
int get_token( );

#endif










