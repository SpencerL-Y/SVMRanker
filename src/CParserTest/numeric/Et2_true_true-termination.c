// public class Et2 {
    // public static void main(String[] args) {
		// Random.args = args;
	    // int a =  Random.random(); 
	   	// int b =  Random.random();	
	   	// loop(a,b);
   	// }
	// public static void loop(int a, int b){   	
	   	// if (b > 0) {
	   		// int r =  Random.random();		
	   		// b = a - 1 - r;
	   	    // a = a - 1 - r;
	   	    // loop(a,b);
	   	// }
    // }
// }


void loop(int a,int b);
int random(void);

int main() {
	int x = 0;
	int y = 0;
	int z = 0;
	loop(random(),random());

}

int random() {
	int x = 0;
	if (x < 0)
		return -x;
	else
		return x;
}

void loop(int a, int b){   	
	   	if (b > 0) {
	   		int r =  random();		
	   		b = a - 1 - r;
	   	    a = a - 1 - r;
	   	    loop(a,b);
	   	}
}
