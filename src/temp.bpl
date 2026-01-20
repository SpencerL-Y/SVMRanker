function unknown_uint() returns (int);
const SIZE: int;
axiom SIZE == 20000001;
procedure main()
{
  var n: int;
  var i: int;
  var k: int;
  var j: int;
  var l: int;
  l := 0;
  n := unknown_uint();
  if (!((n <= SIZE)))
  {
  }

  i := 0;
  j := 0;
  k := 0;
  l := 0;
  while ((l < n))
  {
  if (((l mod 3) == 0))
  {
    i := (i + 1);  } else {
    if (((l mod 2) == 0))
    {
      j := (j + 1);    } else {
      k := (k + 1);    }
  }

  l := (l + 1);  }

}