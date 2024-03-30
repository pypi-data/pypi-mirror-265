"""

  conventions and supporting tools for using Fire in a more natural-ish
  language style

"""
__version__ = "0.1.0"

import sys
import functools

import fire

class Clipboards():
  """
  
  simple multi-clipboard support
  
  """
  def __init__(self):
    self._boards = []
    next(self)

  def __next__(self):
    self._boards.append({"default": self["default"]})

  def __setitem__(self, key, value):
    self._boards[-1][key] = value

  def __getitem__(self, key):
    try:
      return self._boards[-1][key]
    except (KeyError, IndexError):
      pass
    return None

  # unused ?
  # def __str__(self):
  #   return str(self._boards)

class Group():
  """
  
  baseclass for command groups
  
  """

  def __init__(self, _parent=None):
    self._parent = _parent
    self._local_shared = {
      "clipboard" : Clipboards(),
      "globals"   : {},
      "exit"      : self
    }
    # is we don't have a parent, we're the top of the food chain and we should
    # start the post_construct_init cycle
    if not self._parent:
      self.__post_construct_init__()

  def __post_construct_init__(self):
    pass

  @property
  def _globals(self):
    return self._shared["globals"]

  @property
  def _shared(self):
    if self._parent:
      return self._parent._shared
    return self._local_shared

  def then(self):
    return self._shared["exit"]

  def copy(self, value, name="default", advance=False):
    self._shared["clipboard"][name] = value
    if advance:
      next(self._shared["clipboard"])
    return self

  def paste(self, name="default"):
    return self._shared["clipboard"][name]

def keep(method):
  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    result = method(self, *args, **kwargs)
    if result is not self:
      self.copy(result, advance=True)
    return self
  return wrapper

def Menu(**kwargs):
  return (MenuGroup, kwargs)

class MenuGroup(Group):
  """
  
  a menu is a set of groups or other menus
  
  """

  def __init__(self, _parent=None, **kwargs):
    self.handlers = kwargs # keep track of command-handlers

    # create command handlers
    for group, handler in self.handlers.items():

      # unpack optional formatted tuple(handler, arguments)
      if type(handler) is tuple:
        handler, args = handler
      else:
        args = {}

      if isinstance(handler, type):
        # make sure all "public" methods return self to allow for chaining
        for attr in handler.__dict__:
          if callable(getattr(handler, attr)) and attr[0] != "_":
            setattr(handler, attr, keep(getattr(handler, attr)))
        self.__dict__[group] = handler(_parent=self, **args)
      elif callable(handler):
        # simple functions
        self.__dict__[group] = (lambda f: lambda: self.copy(f(), advance=True))(handler)
      else:
        raise ValueError(f"Classes or other Menu'. Got '{type(handler)}'.")

    # all set, now activate it as a group
    super().__init__(_parent=_parent)

  def __post_construct_init__(self):
    for name in self.handlers.keys():
      try:
        self.__dict__[name].__post_construct_init__()
      except AttributeError:
        pass

class FiredUp(MenuGroup):
  
  def __init__(self, name=None, command=None, all_results=False, **kwargs):
    if "--all" in sys.argv:
      sys.argv.remove("--all")
      all_results = True

    if all_results:
      def paste_result(obj):
        return [board["default"] for board in obj._shared["clipboard"]._boards[:-1] ]
    else:
      def paste_result(obj):
        try:
          return obj.paste()
        except AttributeError:
          return obj
    
    super().__init__(**kwargs)
    
    try:
      fire.Fire(self, name=name, command=command, serialize=paste_result)
    except KeyboardInterrupt: # pragma: no cover
      pass
