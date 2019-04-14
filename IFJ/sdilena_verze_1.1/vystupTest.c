

#include "Scanner.h"

int main(){

	//inicializace struktury pro ukladani nactenych tokenu
	Tlist * t = init_Tlist();

	//testovane napleni
	for(int i = 0; i <= 250; i++){
		insertNext_Tlist(t, "test3", 6);
	}
	//vypis pouze ulozene hodnoty stringu
	for(int i = 0; i <= t->top; i++){

		printf("%d: %s\n", i, t->arr[i]->value->string);

	}
	
	
	//dealokace veskere alokovane pameti pouzite v Tlist
	free_Tlist(t);

	return 0;
}