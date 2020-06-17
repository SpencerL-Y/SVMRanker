procedure main()
{
  var m: int;
  var n: int;
  var v1: int;
  var v2: int;
  if (((n>=0)&&(m>0)))
  {
    v1 := n;
    v2 := 0;
    while ((v1>0))
    {
    if ((v2<m))
    {
      v2 := (v2+1);
      v1 := (v1-1);    } else {
      v2 := 0;    }
    }
  }

}