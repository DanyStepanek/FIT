
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/

#include "Token.h"

#define LIST_SIZE  50 // vychozi delka pole Tokenu

typedef struct Tlist{
	int size;				//velikost pole
	int top;				//ukazatel na posledni obsazeny index
	Token **arr;			//ukazatel na pole ukazatelu typu Token
}Tlist;

/*
	Inicializace strukutury, alokace pro ukazatel Tlist* a pro ukazatel Token ** (velikost LIST_SIZE)
	
	@return - ukazatel typu Tlist
			- NULL
			- nastaveni hodnot top = -1, size = LIST_SIZE
*/
Tlist * init_Tlist();

/*
	Vklada hodnotu stringu na prvni volnou pozici v poli tokenu, vytvari novy Token (ten vytvari no RString)
	Pokud je pole jiz plne, dojde k realokaci. 
	
	@param Tlist *t - ukazatel na inicializovany listTokenu
	@param char *string - ukazatel na ukladany string
	@param int size - velikost ukladaneho stringu
	@return 0 - OK
			-1 - Chyba
			-2 - Chyba pri realokaci pole 
*/
int insertNext_Tlist(Tlist *t, char *string, int size);

/*
	Uvolni alokovanou pamet pro cely list, vcetne vsech Tokenu a RStringu.
	Dealokuje pamet pro:
		volani fce pro vsechny prvky v poli free_Token(), ta vola free_RString()
		ukazatel Tlist*
		ukazatel  Token**
		
*/
void free_Tlist(Tlist* t);