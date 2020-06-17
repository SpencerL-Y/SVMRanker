procedure main()
{
  var a: int;
  var x: int;
  var max: int;
  if ((max>0))
  {
    a := 0;
    x := 1;
    while ((x<max))
    {
    if ((__VERIFIER_nondet_int()!=0))
    {
      a := (a+1);    } else {
      a := (a-1);    }

    x := (x+1);    }
  }

}