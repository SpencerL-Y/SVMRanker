procedure main()
{
  var x: int;
  var y: int;
  var random: int;
  while (((x>0)&&(y>0)))
  {
  random := __VERIFIER_nondet_int();
  if ((random<42))
  {
    x := (x-1);
    random := __VERIFIER_nondet_int();
    y := random;  } else {
    y := (y-1);  }
  }

}