extern void __VERIFIER_error() __attribute__ ((__noreturn__));

/*
 * Recursive computation of fibonacci numbers.
 * 
 * Author: Matthias Heizmann
 * Date: 2013-07-13
 * 
 */




int fibonacci(int n) {
    if (n < 1) {
        return 0;
    } else if (n == 1) {
        return 1;
    } else {
        return fibonacci(n-1) + fibonacci(n-2);
    }
}


int main() {
    int x = 0;
	if(x < 1)
		return 0;
    int result = fibonacci(x);
    if (result >= 1) {
        return 0;
    } else {
        ERROR: __VERIFIER_error();
    }
}
    

