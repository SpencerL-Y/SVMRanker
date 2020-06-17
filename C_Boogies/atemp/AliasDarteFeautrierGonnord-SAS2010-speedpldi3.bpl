procedure main()
{
  var i: int;
  var j: int;
  var m: int;
  var n: int;
  if (((m>0)&&(n>m)))
  {
    i := 0;
    j := 0;
    while ((i<n))
    {
    if ((j<m))
    {
      j := (j+1);    } else {
      j := 0;
      i := (i+1);    }
    }
  }

}