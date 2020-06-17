procedure main()
{
  var id: int;
  var maxId: int;
  var tmp: int;
  if (((0<=id)&&(id<maxId)))
  {
    tmp := (id+1);
    while (((tmp!=id)&&(__VERIFIER_nondet_int()!=0)))
    {
    if ((tmp<=maxId))
    {
      tmp := (tmp+1);    } else {
      tmp := 0;    }
    }
  }

}