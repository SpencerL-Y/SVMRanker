procedure main()
{
  var x: int;
  var y: int;
  var z: int;
  while ((((x>0)&&(y>0))&&(z>0)))
  {
  if ((y>x))
  {
    y := z;
    x := __VERIFIER_nondet_int();
    z := (x-1);  } else {
    z := (z-1);
    x := __VERIFIER_nondet_int();
    y := (x-1);  }
  }

}