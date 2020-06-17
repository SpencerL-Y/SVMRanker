procedure main()
{
  var x: int;
  var y: int;
  var oldx: int;
  var oldy: int;
  while (((x>0)&&(y>0)))
  {
  oldx := x;
  oldy := y;
  if ((__VERIFIER_nondet_int()!=0))
  {
    x := (oldx-1);
    y := oldx;  } else {
    x := (oldy-2);
    y := (oldx+1);  }
  }

}