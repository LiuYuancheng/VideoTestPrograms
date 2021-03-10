#include <stdio.h>
#include <stdlib.h>

int main(int argc,char *argv[])
{
	setuid(0);
	system("ls");
	exit(0);
}
