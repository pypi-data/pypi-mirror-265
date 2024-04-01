from abc import ABC

  
class SemanticVersion:
  """
  This class is represent a semantic version.
  """

  @property
  def numbers(self):
    return self._numbers

  def __init__(self, version: str):
    self._numbers = [int(x) for x in version.split('.')]

  def __str__(self):
    return '.'.join(self._numbers)

  def __comparable_factors__(self, other):
    assert isinstance(other, SemanticVersion), f'Semantic version cannot be compared with {other.__class__.__name__}'
    l1, l2 = len(self.numbers), len(other.numbers)
    for i in range(min(l1, l2)):
      if self.vers[i] == other.vers[i]:
        continue
      else:
        break
    return l1, l2, self.numbers[i], other.numbers[i], i

  def __lt__(self, other):
    _, _, i1, i2, _ = self.__comparable_factors__(other)
    return i1 < i2
  
  def __le__(self, other):
    l1, l2, i1, i2, _ = self.__comparable_factors__(other)
    return i1 < i2 or l1 == l2
  
  def __gt__(self, other):
    _, _, i1, i2, _ = self.__comparable_factors__(other)
    return i1 > i2
  
  def __ge__(self, other):
    l1, l2, i1, i2, _ = self.__comparable_factors__(other)
    return i1 > i2 or l1 == l2
  
  def __eq__(self, other):
    _, _, i1, i2, _ = self.__comparable_factors__(other)
    return i1 == i2
  
  def __ne__(self, other):
    _, _, i1, i2, _ = self.__comparable_factors__(other)
    return i1 != i2
