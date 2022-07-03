//Loops.py 8
int main() {
    double x0, x1;
    while (x1*x1 >= x0*x0 - x0 + 1.0) {
        x0 = x0*x0 + x1 + 1.0; x1 = -x1+1.0;
    }
}
