#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

int i, length; 
unsigned int xormask = 0xbe; 

int bof(FILE *badfile)
{
    char buffer[12];
	bof1(1); 
	// vulnerable with buffer overflow attack
    length = fread(buffer, sizeof(char), 52, badfile);
    //printf("length = %d\n", length);
    for(i=0; i<length; i++){
    //printf("i= %d\n", i);
    buffer[i] ^= xormask; 
    }
    bof2(1);
    return 1;
}
int bof1(int a){
	return a;
}

int bof2(int a){
	return a; 
}

int main(int argc, char **argv)
{
    FILE *badfile;
	 
    badfile = fopen("badfile", "r");
    bof(badfile);
    printf("Returned Properly\n");
    fclose(badfile);
    return 1;
}#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

int i, length; 
unsigned int xormask = 0xbe; 

int bof(FILE *badfile)
{
    char buffer[12];
	// vulnerable with buffer overflow attack
    length = fread(buffer, sizeof(char), 52, badfile);
    printf("length = %d\n", length);

    for(i=0; i<length; i++){
    //printf("i= %d\n", i);
    buffer[i] ^= xormask; 
    }
    return 1;
}

int main(int argc, char **argv)
{
    FILE *badfile;
    badfile = fopen("badfile", "r");
    bof(badfile);

    printf("Returned Properly\n");

    fclose(badfile);
    return 1;
}
