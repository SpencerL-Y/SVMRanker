int main(){
    double x0, x1, x2, oldx0;
    while (5.0*x0*x0 + 4.0*x2*x2 <=40.0*x1 && x1+x2<= 0.0-1.0) {
    	oldx0 = x0;
        x0 = x0 +x1; x1 = oldx0+x2; x2 = x2-x2*x2-1.0/(x2*x2);
    }
}
