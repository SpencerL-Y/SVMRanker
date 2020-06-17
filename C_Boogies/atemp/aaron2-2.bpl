procedure main()
{
  var x: int;
  var y: int;
  var tx: int;
  while (((x>=y)&&(tx>=0)))
  {
  if ((__VERIFIER_nondet_int()!=0))
  {
    x := ((x-1)-tx);  } else {
    y := ((y+1)+tx);  }
  }

}