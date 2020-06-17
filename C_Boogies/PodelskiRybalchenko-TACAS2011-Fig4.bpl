procedure main()
{
  var x: int;
  var y: int;
  while (((x>0)&&(y>0)))
  {
  if ((__VERIFIER_nondet_int()!=0))
  {
    x := (x-1);
    y := __VERIFIER_nondet_int();  } else {
    y := (y-1);  }
  }

}