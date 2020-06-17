procedure main()
{
  var x: int;
  var y: int;
  while (((x>0)&&(y>0)))
  {
  old_x := x;
  old_y := y;
  if (__VERIFIER_nondet_int())
  {
    x := (old_x-1);
    y := old_x;  } else {
    x := (old_y-2);
    y := (old_x+1);  }
  }

}