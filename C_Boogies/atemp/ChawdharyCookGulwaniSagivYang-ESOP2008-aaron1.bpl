procedure main()
{
  var i: int;
  var j: int;
  var an: int;
  var bn: int;
  i := __VERIFIER_nondet_int();
  j := __VERIFIER_nondet_int();
  an := __VERIFIER_nondet_int();
  bn := __VERIFIER_nondet_int();
  while (((((an>=i)&&(bn>=j))||((an>=i)&&(bn<=j)))||((an<=i)&&(bn>=j))))
  {
  if (((an>=i)&&(bn>=j)))
  {
    if ((__VERIFIER_nondet_int()!=0))
    {
      j := (j+1);    } else {
      i := (i+1);    }
  } else {
    if (((an>=i)&&(bn<=j)))
    {
      i := (i+1);    } else {
      if (((an<=i)&&(bn>=j)))
      {
        j := (j+1);      }
    }
  }
  }

}