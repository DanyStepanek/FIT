

#include "gen_stack.h"

void init_genStack(genStack* stack){

	stack->top = NULL;

}

void push_genStack(genStack* stack, char* str1, char* str2, char* str3, int dat_type){

	genItem * newItem = malloc(sizeof(genItem));

	if(newItem == NULL){
		fprintf(stderr, "Chyba alokace pameti, gen_stack\n");
		exit(99);
	}else{
		newItem->str1 = init_RString();
		fill_RString(newItem->str1, str1, strlen(str1));

		newItem->str2 = init_RString();
		fill_RString(newItem->str2, str2, strlen(str2));
		
		newItem->str3 = init_RString();
		fill_RString(newItem->str3, str3, strlen(str3));

		newItem->dat_type = dat_type;
		newItem->next = NULL;

		if(stack->top == NULL){
			stack->top = newItem;
		}else{
			newItem->next = stack->top;
			stack->top = newItem;
		}

	}

}

void pop_genStack(genStack* stack){

	if(stack->top != NULL){

		genItem* tmp = stack->top;

		if(tmp->next == NULL){
		
			free_RString(tmp->str1);
			free_RString(tmp->str2);
			free_RString(tmp->str3);
			free(tmp);

			stack->top = NULL;
		
		}else{

			stack->top = tmp->next;

			free_RString(tmp->str1);
			free_RString(tmp->str2);
			free_RString(tmp->str3);
			free(tmp);

		}

	}

}

genItem* top_genStack(genStack* stack){

	if(stack->top != NULL){
		genItem* item = malloc(sizeof(genItem));

		int dat_type = stack->top->dat_type;
		char* str1 = stack->top->str1->string;
		char* str2 = stack->top->str2->string;
		char* str3 = stack->top->str3->string;

		if(item == NULL){
			fprintf(stderr, "Chyba alokace pameti, gen_stack\n");
			exit(99);
		}else{
			
			item->str1 = init_RString();
			fill_RString(item->str1, str1, strlen(str1));

			item->str2 = init_RString();
			fill_RString(item->str2, str2, strlen(str2));
		
			item->str3 = init_RString();
			fill_RString(item->str3, str3, strlen(str3));

			item->dat_type = dat_type;
			//item->next = NULL;
	
		}
		
		return item;

	}
	
	
	return NULL;
}

void empty_genStack(genStack* stack){

	while(stack->top != NULL){
		pop_genStack(stack);
	}

}

void reverse_genStack(genStack* in, genStack* out){

	// // genItem* item = malloc(sizeof(genItem));

	int dat_type;
	char* str1;
	char* str2;
	char* str3;

	// if(item == NULL){
	// 	fprintf(stderr, "Chyba alokace pameti, gen_stack\n");
	// 	exit(99);
	// }else{
		
	// 	while(in->top != NULL){

	// 		dat_type =  in->top->dat_type;;
	// 		str1  = in->top->str1->string;
	// 		str2  = in->top->str2->string;
	// 		str3  = in->top->str3->string;

	// 		item->str1 = init_RString();
	// 		fill_RString(item->str1, str1, strlen(str1));

	// 		item->str2 = init_RString();
	// 		fill_RString(item->str2, str2, strlen(str2));
		
	// 		item->str3 = init_RString();
	// 		fill_RString(item->str3, str3, strlen(str3));

	// 		item->dat_type = dat_type;

	// 		pop_genStack(in);
	// 		push_genStack(out, );

	// 		free_RString(item->str1);
	// 		free_RString(item->str2);
	// 		free_RString(item->str3);
	// 		free(item);

	// 	}

	// }


	while(in->top != NULL){


		dat_type =  in->top->dat_type;;
		str1  = in->top->str1->string;
		str2  = in->top->str2->string;
		str3  = in->top->str3->string;

		push_genStack(out, str1, str2, str3, dat_type);
		pop_genStack(in);

	}
}