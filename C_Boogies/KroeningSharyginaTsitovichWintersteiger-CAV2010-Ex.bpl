procedure main()
{
  var i: int;
  while ((i<255))
  {
  if ((__VERIFIER_nondet_int()!=0))
  {
    i := (i+1);  } else {
    i := (i+2);  }
  }

}