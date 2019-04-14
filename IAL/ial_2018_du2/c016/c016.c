
/* c016.c: **********************************************************}
{* Téma:  Tabulka s Rozptýlenými Položkami
**                      První implementace: Petr Přikryl, prosinec 1994
**                      Do jazyka C prepsal a upravil: Vaclav Topinka, 2005
**                      Úpravy: Karel Masařík, říjen 2014
**                              Radek Hranický, 2014-2018
**
** Vytvořete abstraktní datový typ
** TRP (Tabulka s Rozptýlenými Položkami = Hash table)
** s explicitně řetězenými synonymy. Tabulka je implementována polem
** lineárních seznamů synonym.
**
** Implementujte následující procedury a funkce.
**
**  HTInit ....... inicializuje tabulku před prvním použitím
**  HTInsert ..... vložení prvku
**  HTSearch ..... zjištění přítomnosti prvku v tabulce
**  HTDelete ..... zrušení prvku
**  HTRead ....... přečtení hodnoty prvku
**  HTClearAll ... zrušení obsahu celé tabulky (inicializace tabulky
**                 poté, co již byla použita)
**
** Definici typů naleznete v souboru c016.h.
**
** Tabulka je reprezentována datovou strukturou typu tHTable,
** která se skládá z ukazatelů na položky, jež obsahují složky
** klíče 'key', obsahu 'data' (pro jednoduchost typu float), a
** ukazatele na další synonymum 'ptrnext'. Při implementaci funkcí
** uvažujte maximální rozměr pole HTSIZE.
**
** U všech procedur využívejte rozptylovou funkci hashCode.  Povšimněte si
** způsobu předávání parametrů a zamyslete se nad tím, zda je možné parametry
** předávat jiným způsobem (hodnotou/odkazem) a v případě, že jsou obě
** možnosti funkčně přípustné, jaké jsou výhody či nevýhody toho či onoho
** způsobu.
**
** V příkladech jsou použity položky, kde klíčem je řetězec, ke kterému
** je přidán obsah - reálné číslo.
*/

#include "c016.h"

int HTSIZE = MAX_HTSIZE;
int solved;

/*          -------
** Rozptylovací funkce - jejím úkolem je zpracovat zadaný klíč a přidělit
** mu index v rozmezí 0..HTSize-1.  V ideálním případě by mělo dojít
** k rovnoměrnému rozptýlení těchto klíčů po celé tabulce.  V rámci
** pokusů se můžete zamyslet nad kvalitou této funkce.  (Funkce nebyla
** volena s ohledem na maximální kvalitu výsledku). }
*/

int hashCode ( tKey key ) {
	int retval = 1;
	int keylen = strlen(key);
	for ( int i=0; i<keylen; i++ )
		retval += key[i];
	return ( retval % HTSIZE );
}

/*
** Inicializace tabulky s explicitně zřetězenými synonymy.  Tato procedura
** se volá pouze před prvním použitím tabulky.
*/

void htInit ( tHTable* ptrht ) {
	
	for(int i=0;i<HTSIZE;i++)
		(*ptrht)[i] = NULL;
}

/* TRP s explicitně zřetězenými synonymy.
** Vyhledání prvku v TRP ptrht podle zadaného klíče key.  Pokud je
** daný prvek nalezen, vrací se ukazatel na daný prvek. Pokud prvek nalezen není, 
** vrací se hodnota NULL.
**
*/

tHTItem* htSearch ( tHTable* ptrht, tKey key ) {
//Osetreni zda tabulka existuje
	if(ptrht == NULL)
		exit(1);

	int id = hashCode(key); //z klice vytvori index do tabulky
	tHTItem *item;
	if((item = (*ptrht)[id])!= NULL){
		if(!strcmp(item->key, key))
			return item;
		while(item->ptrnext != NULL){	//prochazeni synonym
			item = item->ptrnext;
			if(!strcmp(item->key, key))
				return item;
		}	
	}
		return NULL;
}

/* 
** TRP s explicitně zřetězenými synonymy.
** Tato procedura vkládá do tabulky ptrht položku s klíčem key a s daty
** data.  Protože jde o vyhledávací tabulku, nemůže být prvek se stejným
** klíčem uložen v tabulce více než jedenkrát.  Pokud se vkládá prvek,
** jehož klíč se již v tabulce nachází, aktualizujte jeho datovou část.
**
** Využijte dříve vytvořenou funkci htSearch.  Při vkládání nového
** prvku do seznamu synonym použijte co nejefektivnější způsob,
** tedy proveďte.vložení prvku na začátek seznamu.
**/

void htInsert ( tHTable* ptrht, tKey key, tData data ) {
	if(ptrht == NULL)
		exit(1);

	int id = hashCode(key);
	tHTItem *item;
	
	//Pokud tabulka jiz obsahuje polozku s danym klicem
	if((item = htSearch(ptrht, key))!= NULL)
		item->data = data;
	else {
		tHTItem *NewItem = malloc(sizeof(struct tHTItem));
		if(NewItem == NULL)
			exit(1);

		//Vytvoreni nove polozky tabulky
		int k_len = strlen(key)+1;
		NewItem->key = malloc(sizeof(char)*k_len);
		strcpy(NewItem->key, key);
		NewItem->data = data;
		NewItem->ptrnext = NULL;
		//Pokud v tabulce jeste neni polozka s danym klicem
		if((item = htSearch(ptrht, key))== NULL){
			NewItem->ptrnext = (*ptrht)[id];
			(*ptrht)[id] = NewItem;
		}
	}
}


/*
** TRP s explicitně zřetězenými synonymy.
** Tato funkce zjišťuje hodnotu datové části položky zadané klíčem.
** Pokud je položka nalezena, vrací funkce ukazatel na položku
** Pokud položka nalezena nebyla, vrací se funkční hodnota NULL
**
** Využijte dříve vytvořenou funkci HTSearch.
*/

tData* htRead ( tHTable* ptrht, tKey key ) {
	if(ptrht == NULL)
		exit(1);	
	
	tHTItem *item = htSearch(ptrht, key);
	if(item != NULL)	
		return &(item->data);
	else
		return NULL;

}

/*
** TRP s explicitně zřetězenými synonymy.
** Tato procedura vyjme položku s klíčem key z tabulky
** ptrht.  Uvolněnou položku korektně zrušte.  Pokud položka s uvedeným
** klíčem neexistuje, dělejte, jako kdyby se nic nestalo (tj. nedělejte
** nic).
**
** V tomto případě NEVYUŽÍVEJTE dříve vytvořenou funkci HTSearch.
*/

void htDelete ( tHTable* ptrht, tKey key ) {
	if(ptrht == NULL)
		exit(1);

	int id = hashCode(key);
	tHTItem *item;	//pomocny ukazatel na polozku
	
	if((*ptrht)[id]!= NULL){
		if(!strcmp((*ptrht)[id]->key, key)){	//pokud se shoduje jiz prvni polozka(synonymum)
			item = (*ptrht)[id]->ptrnext;
			free((*ptrht)[id]->key);
			free((*ptrht)[id]);
			(*ptrht)[id] = item;
		}
		else if((*ptrht)[id]->ptrnext != NULL){	//pokud se prvni neshoduje ale jsou synonyma
			tHTItem *preItem = (*ptrht)[id];	//pomocna promenna pro uchovani ukazatelu
			item = (*ptrht)[id]->ptrnext;
			while(item != NULL){				//dokud jsou dalsi synonyma
				if(!strcmp(item->key, key)){
					preItem->ptrnext = item->ptrnext;
					free(item->key);
					free(item);
					exit(0);
				
				}	
				preItem = item;	
				item = item->ptrnext;
			}	//konec while
		}	//konec else if
	} //konec if

}

/* TRP s explicitně zřetězenými synonymy.
** Tato procedura zruší všechny položky tabulky, korektně uvolní prostor,
** který tyto položky zabíraly, a uvede tabulku do počátečního stavu.
*/

void htClearAll ( tHTable* ptrht ) {
	if(ptrht == NULL)
		exit(0);
		
	tHTItem *item, *postItem = NULL;
	for(int i=0;i < HTSIZE;i++){
			item = (*ptrht)[i];			//ukazatel na aktualni polozku
		while(item != NULL){
			postItem = item->ptrnext;	//ukazatel na dalsi polozku
			free(item->key);
			free(item);
			item = postItem;
		}
		(*ptrht)[i] = NULL;
	}
}
