int main() {
    double x0, x1;
    double oldx0 = 0.0;
    while (x0 >= 0.0 && x1-2.0*x0 >= 1.0) {
    	oldx0 = x0;
        x0 = 0.0 - x0*x0 -4.0*x1*x1 + 1.0;
        x1 = 0.0 - oldx0*x1 - 1.0;
    }
}
