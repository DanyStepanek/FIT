#include "symtable.h"

#define VALUE_LENGTH 30

unsigned long djb2(char *str, int slength)
{
        unsigned long h = 5381;
        int c;
        int i = 0;

        while (i < slength){
           	c = *str++;
            h = ((h << 5) + h) + c; /* h * 33 + c */
        	i++;
        }	
        return h;
}	


void Node_init(Node **node){
	*node = NULL;
}



Data* toData(Token *token){
	
	Data *newData = malloc(sizeof(struct Data));
	
	if(newData == NULL){
		fprintf(stderr, "Allocation failed(symbol table)\n");
		return NULL;
	}
	
	
	newData->value = (char*) malloc((VALUE_LENGTH));
	if(newData->value == NULL)
		return NULL;
	
	newData->length = 0;
	newData->id = token->id;
	newData->value[0] = '\0';
	//newNode->key = djb2(newNode->data, newNode->length);
	
	return newData;
}

void Node_create(Node** root, int cat, Token* token){

	if(*root == NULL){			//prazdny uzel

	//	printf("Tvorba\n");

		Node *newPtr = malloc(sizeof(struct Node));		//alokace pameti pro uzel (ne pro jeho data!)

		if(newPtr == NULL){
			fprintf(stderr, "Node_insert chyba alokace pameti (symtable.c:14)\n");
			return;
		}
		
			//(*root)->data = malloc(sizeof(struct Data));
			newPtr->data = toData(token);
			
			int size = strlen(token->value->string);

			if(newPtr->data != NULL){
				newPtr->data->defined = false;
				newPtr->l_ptr = NULL;
				newPtr->r_ptr = NULL;
				newPtr->data->category = cat;
				newPtr->key = djb2(token->value->string, size);
			//printf(" root: %d id, %d catagory\n",root->id, root->category);
				(*root) = newPtr;
			}
			else { 
				fprintf(stderr, "Node_insert chyba alokace pameti (symtable.c:26)\n");
				return;
			}

		 

		return;
	}
	else {



		int size = strlen(token->value->string);
		unsigned int key = djb2(token->value->string, size);
		
		
		if((*root)->key == key) {					//aktualizace uzlu
			(*root)->data->id = token->id;
			(*root)->data->category = cat;
			(*root)->data->length = size;
					
		}else if((*root)->key < key){			//v pravo 
			
			Node_create(&(*root)->r_ptr, cat, token);

		}else if((*root)->key > key){			//v levo
			
			Node_create(&(*root)->l_ptr, cat, token);

		}
		
	}

//	printf(" root: %d id, %d catagory\n",root->id, root->category);


}


void Node_actualize(Node** root, int cat, Token* token){

		int size = strlen(token->value->string);
		if(size >= (*root)->data->length)
			(*root)->data->value = (char*) realloc((*root)->data->value, size);
		
		(*root)->data->id = token->id;
		strcpy((*root)->data->value, token->value->string);
		(*root)->data->category = cat;
		(*root)->data->length = size;
		(*root)->data->defined = true;
					
			
}



void print_tree(Node** root){
	static int i = 0;


	if(*root != NULL){
		//printf("NOT NULL");
		printf("%d) root: %lu id, %d category, %d dat.type, %s name\n", i, (*root)->key, (*root)->data->category, (*root)->data->id, (*root)->data->value);
		i++;
		print_tree(&(*root)->l_ptr);
		print_tree(&(*root)->r_ptr);
		//i = 0;
	}else{
		//printf("NULL\n");
	}
}


Node* find_Node(Node** node, char* name){

	unsigned long id = djb2(name, strlen(name));

	if(*node != NULL){

		if(id == (*node)->key){	//nalezly jsme hledany uzel
			return *node;

		}else{

			if( id > (*node)->key){			//pruchod v pravo
				return find_Node(&(*node)->r_ptr, name);
			}
			
			if( id < (*node)->key){			//pruchod v pravo
				return find_Node(&(*node)->l_ptr, name);
			}
		}

	}

	return NULL;
}

void Data_delete(Node** node){
//	printf("mazu\n");
				
	if((*node)->data != NULL){
		if((*node)->data->category == 2){					//jedna se funkci

		dynamic_string_free((*node)->data->params);
		}
		free((*node)->data->value);
		free((*node)->data);
		
	}

	

}

void ReplaceByMostRight(Node* replaced, Node** root){
	
	if(root != NULL){
		
		Node* tmpPtr;
		
		if((*root)->r_ptr == NULL){
			
			replaced->key = (*root)->key;
			replaced->data = (*root)->data;
			tmpPtr = (*root);
			(*root) = (*root)->l_ptr;
			free(tmpPtr);
					
		}else{
			ReplaceByMostRight(replaced, &(*root)->r_ptr);
		}
	}
}

void Node_delete(Node** node, char* name){

	Node *tmp = NULL;
	//Node** dataTmp = NULL;
	unsigned long id = djb2(name, strlen(name));

	if((*node) != NULL){

		
		if(id == (*node)->key){			//shoda

			tmp = (*node);			//docasne ulozeni mazaneho prvku
			
			
			if((*node)->l_ptr == NULL && (*node)->r_ptr == NULL){		//uzel nema zadne syny
				
				//printf("CHILDLES FOUND\n");

				Data_delete(node);
				(*node) = NULL;
				free(tmp);						//uvolneni uzlu
				
				return;

			}else if((*node)->l_ptr == NULL && (*node)->r_ptr != NULL){	// pouze pravy podstrom

				// printf("R CHILD\n");

				(*node)  = (*node)->r_ptr;
				free(tmp);

			}else if((*node)->l_ptr != NULL && (*node)->r_ptr == NULL){	//pouze levy podstrom

				// printf("L CHILD\n");
				(*node)  = (*node)->l_ptr;
				free(tmp);

			}else if((*node)->l_ptr != NULL && (*node)->r_ptr != NULL){	// oba podstromy

				//printf("LR CHILD\n");

				ReplaceByMostRight((*node), &(*node)->l_ptr);
			//	Node_delete(&(*node)->l_ptr,name);

			}


		}else{
			//printf("ziju\n");
			

			if(id > (*node)->key){
				
				if((*node)->r_ptr != NULL){
					Node_delete(&(*node)->r_ptr, name);	
				
				}
			}else if( id < (*node)->key){
				if((*node)->l_ptr != NULL){
				
					Node_delete(&(*node)->l_ptr, name);	
				
				}
			}

		}

	}
}

void Tree_delete(Node** root){
	if(*root != NULL){

		
		Tree_delete(&(*root)->l_ptr);
		Tree_delete(&(*root)->r_ptr);
	//	Node_delete(root, (*root)->data->value);
		free((*root)->data->value);
		free((*root)->data);
		free(*root);
		
		(*root) = NULL;

	}
}