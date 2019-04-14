
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/

#ifndef TOKEN_H_INCLUDED
#define TOKEN_H_INCLUDED

#include "rstring.h"


typedef struct token{
	int id;
	RString *value;
}Token;


/*
	Inicializace tokenu, volani init_RString, alokace pameti pro ukazatel na token
*/
Token * init_Token();

/*
	Vlozeni hodnoty do tokenu, t->value->string
	@param Token*token - ukazatel na jiz INICIALIZOVANY token
	@param char* value - ukazatel na ukladanou hodnotu
	@param int length - delka ukladaneho retezce
	@return 0 - vlozeni probehlo v poradku
			-1 - chyba
*/
int fill_Token(Token* , char* , int ,int );

/*
	Uvolni alokovanou pamet, volani funkce free_RString
*/
void free_Token(Token *);

#endif
