procedure main()
{
  var x: int;
  var y: int;
  if (((x>=0)&&(y>=0)))
  {
    while ((((x-y)>2)||((y-x)>2)))
    {
    if ((x<y))
    {
      x := (x+1);    } else {
      y := (y+1);    }
    }
  }

}