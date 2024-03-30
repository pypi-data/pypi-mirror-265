import inspect
import pytest


class BasePage:
    def __init__(self):
        self.return_orig_val = False

    def __getattribute__(self, item):
        val = object.__getattribute__(self, item)
        if isinstance(val, dict) and not self.return_orig_val:
            for func in [pytest.be.element, pytest.driver.find_element]:
                try:
                    inspect.getcallargs(func, **val)
                    return func(**val)
                except TypeError:
                    continue
        if item not in ['__class__', 'val']:
            self.return_orig_val = False
        return val

    @property
    def val(self):
        self.return_orig_val = True
        return self

    def get_orig_val(self, attr):
        self.return_orig_val = True
        val = getattr(self, attr)
        self.return_orig_val = False
        return val