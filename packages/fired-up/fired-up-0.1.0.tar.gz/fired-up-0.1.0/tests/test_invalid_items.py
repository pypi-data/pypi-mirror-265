from fired_up import FiredUp

def test_simple_variable():
  item = 123
  try:
    FiredUp(
      item1=item,
      command="item1"
    )
    assert False
  except ValueError:
    pass
