// public class Et4 {
    // public static void main(String[] args) {
		// Random.args = args;
	    // int a =  Random.random(); 
	   	// int b =  Random.random();	
	    // int c =  Random.random();
	    // loop(a,b,c);
	// }
	// public static void loop(int a, int b, int c) {	
	   	// if ( (b - c >= 1) && (a == c)) {
	   		// int r =  Random.random();
	   		// b = 10;
	   		// c = c + 1 + r;		
	   	    // a = c;
	   	    // loop(a,b,c);
	   	// }
    // }
// }


void loop(int a,int b,int c);
int random(void);

int main() {
	int x = 0;
	int y = 0;
	int z = 0;
	loop(random(),random(),random());

}

int random() {
	int x = 0;
	if (x < 0)
		return -x;
	else
		return x;
}

void loop(int a, int b, int c) {	
	   	if ( (b - c >= 1) && (a == c)) {
	   		int r =  random();
	   		b = 10;
	   		c = c + 1 + r;		
	   	    a = c;
	   	    loop(a,b,c);
	   	}
    }

