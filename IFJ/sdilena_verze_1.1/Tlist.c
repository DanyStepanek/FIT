
/*
	IFJ Projekt 2018
	autor: David Triska
	login: xtrisk05
*/
#include "Tlist.h"

Tlist * init_Tlist(){
	Tlist *t = malloc(sizeof(Tlist));			//alokace mista pro ukazatel Tlist
	t->arr = malloc(sizeof(Token)*LIST_SIZE);	//alokace mista pro ukazatel *Token pro pole o velikosti LIST_SIZE

	if(t != NULL && t->arr != NULL){  // kontrola alokace pameti
			t->size = LIST_SIZE;
			t->top = -1;
	}
	
	return t;		


}

int insertNext_Tlist(Tlist* t, char *c, int size){

	if(t != NULL && c != NULL){			// kontrola platnosti vstupnich ukazatelu
			
		Token * token = init_Token();    //inicializace noveho Tokenu
		if(token != NULL){

			if(t->top == t->size){		//kontrola dostatecne pameti v poli
				Token ** recArrT = realloc(t->arr,sizeof(Tlist)*t->size*2);
				if(recArrT != NULL){
					t->arr = recArrT;
					t->size = t->size*2; 		//nova max velikost pole
				}else {
					return -2; 		// navratova hodnota -2 znaci chybu pri realokci 
				}
			}

			t->top += 1;					
			t->arr[t->top] = token;			//prirazeni Tokenu do pole
			
			if(fill_Token(t->arr[t->top], c, size) == 0){ // naplneni a kontrola spravneho vlozeni 
				return 0;
			} else{
				return -1;
			}
			
		}else{
			return -1;
		}
		
	}else{
		return -1;
	}

}

void free_Tlist(Tlist * t){
	if(t != NULL){
		for(int i = 0; i <= t->top; i++){
			free_Token(t->arr[i]);
		}

		free(t->arr);
		free(t);	
	}
	
}