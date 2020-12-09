//#rNonTerminationDerivable
/*
 * Date: 2014-03-17
 * Author: heizmann@informatik.uni-freiburg.de
 *
 * From Amir M. Ben-Amram and Samir Genaim,
 * Ranking Functions for Linear-Constraint Loops.
 * POPL 2013
 *
 * Does not terminate over the reals.
 * Has linear ranking function f(x1,x2)=x1+x2-1 over the integers.
 * Loop is not integral.
 */

procedure main() returns () {
    var x, y: real;
    while (x > 0) {
        x := x - y;
        y := y + 1;
    }
}