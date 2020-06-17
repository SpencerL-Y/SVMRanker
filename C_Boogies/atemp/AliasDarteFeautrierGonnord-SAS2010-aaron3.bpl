procedure main()
{
  var x: int;
  var y: int;
  var z: int;
  var tx: int;
  while (((x>=y)&&(x<=(tx+z))))
  {
  if (__VERIFIER_nondet_int())
  {
    z := (z-1);
    tx := x;
    x := __VERIFIER_nondet_int();  } else {
    y := (y+1);  }
  }

}