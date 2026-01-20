function __VERIFIER_nondet_int() returns (int);
procedure main()
{
  var x: int;
  var y: int;
  x := __VERIFIER_nondet_int();
  y := __VERIFIER_nondet_int();
  while (((x > 0) && (y > 0)))
  {
  if ((__VERIFIER_nondet_int() != 0))
  {
    x := (x - 1);
    y := (2 * y);  } else {
    y := (y - 1);  }
  }

}