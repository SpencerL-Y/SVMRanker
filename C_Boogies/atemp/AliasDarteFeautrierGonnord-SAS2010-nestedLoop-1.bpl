procedure main()
{
  var i: int;
  var j: int;
  var k: int;
  var m: int;
  var n: int;
  var N: int;
  if ((((0<=n)&&(0<=m))&&(0<=N)))
  {
    i := 0;
    while ((i<n))
    {
    j := 0;
    while ((j<m))
    {
    j := (j+1);
    k := i;
    while ((k<(N-1)))
    {
    k := (k+1);    }

    i := k;    }

    i := (i+1);    }
  }

}