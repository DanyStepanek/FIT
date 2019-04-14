
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/

/*
	RString
	abstraktni datovy typ, pro ulozeni hodnoty nacteneho string
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct rstring{
	int size;
	int aloc;
	char * string;
}RString;

/*
	Alokace pameti o velikosti size, pro retezec c, vraci ukazatel na RString
	@param int size - velikost ukladaneho stringu
	@return - RStrint * - pokud vse probehlo v poradku
			- NULL nedoslo k alokaci pameti 
*/
RString * init_RString();

/*
	Uvolni alokovanou pamet RString.string
	@param RString * s - dealokace ukazate s, i s->string, s->size = s->aloc = 0;
	
*/
void free_RString(RString * s);

/*
	Do jiz vytvoreneho RString!! vklada string c o velikosti length
	@param RString *s - ukazatel na INICIALIZOVANY RString
	@param char *c - ukazatel na ukladany string
	@param int length - delka ukladaneho retezce
*/
int fill_RString(RString *s, char* c, int length);