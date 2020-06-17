procedure main()
{
  var x: int;
  var y: int;
  while ((x>=2))
  {
  x := (x-1);
  y := (y+x);
  while (((y>=x)&&(__VERIFIER_nondet_int()!=0)))
  {
  y := (y-1);  }

  x := (x-1);
  y := (y-x);  }

}