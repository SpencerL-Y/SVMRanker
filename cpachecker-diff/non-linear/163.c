//Loops.py 18
int main() {
    double x0, x1, x2;
    double oldx0 = 0;
    while (0.0<=x0 && x1-2.0*x0>=x2 && x2>=1.0) {
    	oldx0 = x0;
        x0 = 0.0 - x0*x0 - 4.0*x1*x1 + x2*x2; x1 = 0.0 - oldx0*x1 - x2*x2; x2 = x2*x2;
    }
}
