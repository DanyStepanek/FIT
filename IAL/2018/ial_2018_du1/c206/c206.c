
/* c206.c **********************************************************}
{* Téma: Dvousměrně vázaný lineární seznam
**
**                   Návrh a referenční implementace: Bohuslav Křena, říjen 2001
**                            Přepracované do jazyka C: Martin Tuček, říjen 2004
**                                            Úpravy: Kamil Jeřábek, září 2018
**
** Implementujte abstraktní datový typ dvousměrně vázaný lineární seznam.
** Užitečným obsahem prvku seznamu je hodnota typu int.
** Seznam bude jako datová abstrakce reprezentován proměnnou
** typu tDLList (DL znamená Double-Linked a slouží pro odlišení
** jmen konstant, typů a funkcí od jmen u jednosměrně vázaného lineárního
** seznamu). Definici konstant a typů naleznete v hlavičkovém souboru c206.h.
**
** Vaším úkolem je implementovat následující operace, které spolu
** s výše uvedenou datovou částí abstrakce tvoří abstraktní datový typ
** obousměrně vázaný lineární seznam:
**
**      DLInitList ...... inicializace seznamu před prvním použitím,
**      DLDisposeList ... zrušení všech prvků seznamu,
**      DLInsertFirst ... vložení prvku na začátek seznamu,
**      DLInsertLast .... vložení prvku na konec seznamu,
**      DLFirst ......... nastavení aktivity na první prvek,
**      DLLast .......... nastavení aktivity na poslední prvek,
**      DLCopyFirst ..... vrací hodnotu prvního prvku,
**      DLCopyLast ...... vrací hodnotu posledního prvku,
**      DLDeleteFirst ... zruší první prvek seznamu,
**      DLDeleteLast .... zruší poslední prvek seznamu,
**      DLPostDelete .... ruší prvek za aktivním prvkem,
**      DLPreDelete ..... ruší prvek před aktivním prvkem,
**      DLPostInsert .... vloží nový prvek za aktivní prvek seznamu,
**      DLPreInsert ..... vloží nový prvek před aktivní prvek seznamu,
**      DLCopy .......... vrací hodnotu aktivního prvku,
**      DLActualize ..... přepíše obsah aktivního prvku novou hodnotou,
**      DLSucc .......... posune aktivitu na další prvek seznamu,
**      DLPred .......... posune aktivitu na předchozí prvek seznamu,
**      DLActive ........ zjišťuje aktivitu seznamu.
**
** Při implementaci jednotlivých funkcí nevolejte žádnou z funkcí
** implementovaných v rámci tohoto příkladu, není-li u funkce
** explicitně uvedeno něco jiného.
**
** Nemusíte ošetřovat situaci, kdy místo legálního ukazatele na seznam 
** předá někdo jako parametr hodnotu NULL.
**
** Svou implementaci vhodně komentujte!
**
** Terminologická poznámka: Jazyk C nepoužívá pojem procedura.
** Proto zde používáme pojem funkce i pro operace, které by byly
** v algoritmickém jazyce Pascalovského typu implemenovány jako
** procedury (v jazyce C procedurám odpovídají funkce vracející typ void).
**/

#include "c206.h"

int errflg;
int solved;

void DLError() {
/*
** Vytiskne upozornění na to, že došlo k chybě.
** Tato funkce bude volána z některých dále implementovaných operací.
**/	
    printf ("*ERROR* The program has performed an illegal operation.\n");
    errflg = TRUE;             /* globální proměnná -- příznak ošetření chyby */
    return;
}

void DLInitList (tDLList *L) {
/*
** Provede inicializaci seznamu L před jeho prvním použitím (tzn. žádná
** z následujících funkcí nebude volána nad neinicializovaným seznamem).
** Tato inicializace se nikdy nebude provádět nad již inicializovaným
** seznamem, a proto tuto možnost neošetřujte. Vždy předpokládejte,
** že neinicializované proměnné mají nedefinovanou hodnotu.
**/
    
	L->First = NULL;
	L->Act = NULL;
	L->Last = NULL;

}

void DLDisposeList (tDLList *L) {
/*
** Zruší všechny prvky seznamu L a uvede seznam do stavu, v jakém
** se nacházel po inicializaci. Rušené prvky seznamu budou korektně
** uvolněny voláním operace free. 
**/
	tDLElemPtr tmpPtr;
	while (L->First != NULL){
		tmpPtr = L->First->rptr;
		free(L->First);
		L->First = tmpPtr;
	}
	L->Act = NULL;
	L->Last = NULL;

}

void DLInsertFirst (tDLList *L, int val) {
/*
** Vloží nový prvek na začátek seznamu L.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
	tDLElemPtr NewElement = malloc(sizeof(struct tDLElem));
	if (NewElement == NULL)	//Memchecking
		DLError();
	
	NewElement->data = val;
	NewElement->lptr = NULL;
	NewElement->rptr = L->First;
/* Osetreni pripadu, kdy v seznamu uz nejaku prvek byl */
	if (L->First != NULL)		
		L->First->lptr = NewElement;
	else
		L->Last = NewElement;

	L->First = NewElement;	
	
}

void DLInsertLast(tDLList *L, int val) {
/*
** Vloží nový prvek na konec seznamu L (symetrická operace k DLInsertFirst).
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/ 	
	tDLElemPtr NewElement = malloc(sizeof(struct tDLElem));
	if (NewElement == NULL)	//Memchecking
		DLError();
	
	NewElement->data = val;
	NewElement->lptr = L->Last;
	NewElement->rptr = NULL;
/* Osetreni pripadu, kdy v seznamu uz nejaku prvek byl */
	if (L->Last != NULL)
		L->Last->rptr = NewElement;
	else
		L->First = NewElement;

	L->Last = NewElement;	

}

void DLFirst (tDLList *L) {
/*
** Nastaví aktivitu na první prvek seznamu L.
** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
** aniž byste testovali, zda je seznam L prázdný.
**/
	L->Act = L->First;

}

void DLLast (tDLList *L) {
/*
** Nastaví aktivitu na poslední prvek seznamu L.
** Funkci implementujte jako jediný příkaz (nepočítáme-li return),
** aniž byste testovali, zda je seznam L prázdný.
**/
	L->Act = L->Last;	
	
}

void DLCopyFirst (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu prvního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci DLError().
**/
	if (L->First == NULL)
		DLError();
	else
		*val = L->First->data;
	
}

void DLCopyLast (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu posledního prvku seznamu L.
** Pokud je seznam L prázdný, volá funkci DLError().
**/
	if (L->Last == NULL)
		DLError();
	else
		*val = L->Last->data;	
	
}

void DLDeleteFirst (tDLList *L) {
/*
** Zruší první prvek seznamu L. Pokud byl první prvek aktivní, aktivita 
** se ztrácí. Pokud byl seznam L prázdný, nic se neděje.
**/
	tDLElemPtr tmpPtr;
	
	if (L->First != NULL){
		if (L->First == L->Act)
			L->Act = NULL;
		
		tmpPtr = L->First->rptr;
		tmpPtr->lptr = L->First->lptr;
		free(L->First);
		L->First = tmpPtr;
		L->First->lptr = tmpPtr->lptr;
	}
	
 
}	

void DLDeleteLast (tDLList *L) {
/*
** Zruší poslední prvek seznamu L. Pokud byl poslední prvek aktivní,
** aktivita seznamu se ztrácí. Pokud byl seznam L prázdný, nic se neděje.
**/ 
	tDLElemPtr tmpPtr;
	
	if (L->Last != NULL){
		if (L->Last == L->Act)
			L->Act = NULL;
		
		tmpPtr = L->Last->lptr;
		tmpPtr->rptr = L->Last->rptr;
		free(L->Last);
		L->Last = tmpPtr;
		L->Last->rptr = tmpPtr->rptr;	
	
	}

}

void DLPostDelete (tDLList *L) {
/*
** Zruší prvek seznamu L za aktivním prvkem.
** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
** posledním prvkem seznamu, nic se neděje.
**/
	tDLElemPtr tmpPtr;	

	if (L->Act != NULL && L->Act->rptr != NULL){
		tmpPtr = L->Act->rptr;	//ukazuje na dalsi prvek(chceme ho zrusit)
		if (tmpPtr->rptr != NULL){
			L->Act->rptr = tmpPtr->rptr;	//aktivni ukazuje na prvek za rusenym
			L->Act->rptr->lptr = L->Act;
		}
		else  {
			L->Act->rptr = NULL;
			L->Last = L->Act;
		}

		free(tmpPtr);
		
	}

}

void DLPreDelete (tDLList *L) {
/*
** Zruší prvek před aktivním prvkem seznamu L .
** Pokud je seznam L neaktivní nebo pokud je aktivní prvek
** prvním prvkem seznamu, nic se neděje.
**/
	tDLElemPtr tmpPtr;

	if (L->Act != NULL && L->Act->lptr != NULL){
		tmpPtr = L->Act->lptr;
		if (tmpPtr->lptr != NULL){
			L->Act->lptr = tmpPtr->lptr;
			L->Act->lptr->rptr = L->Act;
		}	
		else {
			L->Act->lptr = NULL;
			L->First = L->Act;	
		}

		free(tmpPtr);
	}

}

void DLPostInsert (tDLList *L, int val) {
/*
** Vloží prvek za aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
	if (L->Act != NULL){
		tDLElemPtr NewElement = malloc(sizeof(struct tDLElem));
		if (NewElement == NULL)	//Memchecking
			DLError();
		
		NewElement->data = val;
		NewElement->rptr = L->Act->rptr;	//Novy prvek ukazuje na prvek za aktivnim.
		NewElement->lptr = L->Act;			//Novy prvek ukazuje zpet na aktivni prvek.
		L->Act->rptr = NewElement;			//Aktivni prvek ukazuje na nasledujici (novy) prvek.
	}

}

void DLPreInsert (tDLList *L, int val) {
/*
** Vloží prvek před aktivní prvek seznamu L.
** Pokud nebyl seznam L aktivní, nic se neděje.
** V případě, že není dostatek paměti pro nový prvek při operaci malloc,
** volá funkci DLError().
**/
	if (L->Act != NULL){
		tDLElemPtr NewElement = malloc(sizeof(struct tDLElem));
		if (NewElement == NULL)	//Memchecking
			DLError();	
		
		NewElement->data = val;
		NewElement->lptr = L->Act->lptr;	//Novy prvek ukazuje na prvek pred aktivnim.
		NewElement->rptr = L->Act;			//Novy prvek ukazuje na aktivni prvek.
		L->Act->lptr = NewElement;			//Aktivni prvek ukazuje na predesly (novy) prvek.
	}

}

void DLCopy (tDLList *L, int *val) {
/*
** Prostřednictvím parametru val vrátí hodnotu aktivního prvku seznamu L.
** Pokud seznam L není aktivní, volá funkci DLError ().
**/
	if (L->Act == NULL)
		DLError();
	else
		*val = L->Act->data;		
	
	

}

void DLActualize (tDLList *L, int val) {
/*
** Přepíše obsah aktivního prvku seznamu L.
** Pokud seznam L není aktivní, nedělá nic.
**/
	if (L->Act != NULL)
		L->Act->data = val;	
	

}

void DLSucc (tDLList *L) {
/*
** Posune aktivitu na následující prvek seznamu L.
** Není-li seznam aktivní, nedělá nic.
** Všimněte si, že při aktivitě na posledním prvku se seznam stane neaktivním.
**/
	if (L->Act != NULL)
		L->Act = L->Act->rptr;
	
}


void DLPred (tDLList *L) {
/*
** Posune aktivitu na předchozí prvek seznamu L.
** Není-li seznam aktivní, nedělá nic.
** Všimněte si, že při aktivitě na prvním prvku se seznam stane neaktivním.
**/
	if (L->Act != NULL)
		L->Act = L->Act->lptr;

}

int DLActive (tDLList *L) {
/*
** Je-li seznam L aktivní, vrací nenulovou hodnotu, jinak vrací 0.
** Funkci je vhodné implementovat jedním příkazem return.
**/
	
	return (L->Act != NULL);	
}

/* Konec c206.c*/
