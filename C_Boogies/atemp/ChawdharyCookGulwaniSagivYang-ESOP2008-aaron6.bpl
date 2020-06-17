procedure main()
{
  var x: int;
  var tx: int;
  var y: int;
  var ty: int;
  var n: int;
  if (((x+y)>=0))
  {
    while (((((x<=n)&&(x>=((2*tx)+y)))&&(y>=(ty+1)))&&(x>=(tx+1))))
    {
    if ((__VERIFIER_nondet_int()!=0))
    {
      tx := x;
      ty := y;
      x := __VERIFIER_nondet_int();
      y := __VERIFIER_nondet_int();    } else {
      tx := x;
      x := __VERIFIER_nondet_int();    }
    }
  }

}