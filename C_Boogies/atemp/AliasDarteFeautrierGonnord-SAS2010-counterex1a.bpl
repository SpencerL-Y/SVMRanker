procedure main()
{
  var x: int;
  var y: int;
  var n: int;
  var b: int;
  while ((((x>=0)&&(0<=y))&&(y<=n)))
  {
  if ((b==0))
  {
    y := (y+1);
    if ((__VERIFIER_nondet_int()!=0))
    {
      b := 1;    }
  } else {
    y := (y-1);
    if ((__VERIFIER_nondet_int()!=0))
    {
      x := (x-1);
      b := 0;    }
  }
  }

}