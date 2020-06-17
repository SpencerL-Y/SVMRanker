procedure main()
{
  var x: int;
  var y: int;
  var tmp: int;
  var xtmp: int;
  while (((y>0)&&(x>0)))
  {
  tmp := y;
  xtmp := x;
  while (((xtmp>=y)&&(y>0)))
  {
  xtmp := (xtmp-y);  }

  y := xtmp;
  x := tmp;  }

}