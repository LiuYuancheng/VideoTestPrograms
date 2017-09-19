#include <stdio.h>
#include <stdlib.h>

int main(int argc,char *argv[])
{
	char *p = getenv("MYSH");
	if(NULL == p)
	 {
		 printf("MYSH no exist\n");
		 exit(0);
	 }
	 printf("MYSH address is %p content %s\n",p,p);
	 return 0;
}
