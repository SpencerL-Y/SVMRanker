//Loops.py 6
int main() {
    double x0, x1, x2;
    while (x0 + x1 >= x2 * x2*x2*x2 - x2*x2 +1.0 && x0 *x0 >= x2) {
        x0 = x0 +x1; x1 = -x2-1.0; x2 =  x2*x2 - 2.0 * x2;
    }
}
