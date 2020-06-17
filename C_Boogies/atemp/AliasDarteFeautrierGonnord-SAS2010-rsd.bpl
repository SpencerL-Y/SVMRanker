procedure main()
{
  var r: int;
  var da: int;
  var db: int;
  var temp: int;
  if ((r>=0))
  {
    da := (2*r);
    db := (2*r);
    while ((da>=r))
    {
    if ((__VERIFIER_nondet_int()!=0))
    {
      da := (da-1);    } else {
      temp := da;
      da := (db-1);
      db := da;    }
    }
  }

}