import os

import rpy2
import numpy as np
import pandas as pd

from .converter import converter

class R(object):
    """
    A wrapper for rpy2, which somewhat mimics the ipython magic functions.
    Basically, it handles the automatic conversion of some python objects to R objects.
    Further, it allows you to automatically push python objects, call code and get converted objects back to python.
    
    Example usage:
    --------------
    
    r = biu.R()
    x = pd.DataFrame([[1,2,3],[4,5,6]])
    r.push(x=x)
    r('y = x * 2')
    y = r.get('y')
    
    Or, altogether:
    ---------------
    y = r('y=x*2', push=dict(x=x), get='y')
    
    Doing a lot at the same time:
    -----------------------------
    
    y, z = r('''
        y = x * 2
        z = x + 2
        ''', push=dict(x=x), get=['y', 'z'])
    
    
    """
    _converter = None
    
    def __init__(self):
        """
        Initialize the rpy2 wrapper
        """
        self._converter  = converter()
        self.push(message="Hilmar doesn't know how to program...")
    #edef
    
    def add_converter(self, obj_type, convert_func):
        """
        Add a converter to the object, if there is one missing.
        
        parameters:
        -----------
        obj_type: the type of the object that this converter relates to
        convert_func: function. The function that should be applied
        """

        self._converter.py2rpy.register(obj_type, convert_func)
    #edef
        
    def push(self, **kwargs):
        """
        Push values to R, based on the current converter
        
        parameters:
        -----------
        kwargs: Dictionary of values
        
        Example usage:
        --------------
        
        r.push(x=10, y='pool', ages=[10, 50, 100])
        """
        
        if kwargs is None:
            return None
        #fi
        
        for (k,v) in kwargs.items():
            with rpy2.robjects.conversion.localconverter(self._converter) as cv:
                rpy2.robjects.r.assign(k, v)
            #ewith
        #efor
    #edef
        
    def get(self, name, *pargs):
        """
        Get a value from R, based on the current converter
        
        parameters:
        -----------
        name: return this variable from the R instance
        *pargs, if specified, return a tuple of name + those in pargs
        
        returns:
        --------
        Either a converted R object, or
        if pargs is specified, then a tuple of values
        """
        with rpy2.robjects.conversion.localconverter(self._converter):
            if len(pargs)  == 0:
                return rpy2.robjects.globalenv.find(name)
            else:
                return [ rpy2.robjects.globalenv.find(n) for n in ([name] + list(pargs)) ]
            #fi
        #ewith
            
    #edef
    
    def exec(self, cmd, push=None, get=True):
        """
        Call R code, pushing values, and returning values if necessary
        
        parameters:
        -----------
        cmd: The R code you want to execute
        push: Dictionary of name:value pairs that you want to introduce to R session
        get: List of R object values that you want to get back
        
        returns:
        ---------
        if get is False, it returns nothing.
        If get is True, it returns the returned value from the R code.
        if get is not None, it returns a value, as specified by the get() function.
        """
        if push is None:
            push = {}
        #fi
        
        self.push(**push)
        
        res = rpy2.robjects.r(cmd)
        
        if isinstance(get, bool) and get:
            return self._converter.rpy2py(res)
        elif isinstance(get, bool) and (not get):
            return None
        elif isinstance(get, str):
            return self.get(get)
        else:
            return self.get(*get)
        #fi
    #edef
    
    def __call__(self, cmd, push=None, get=True):
        """
        Call R code, pushing values, and returning values if necessary
        
        parameters:
        -----------
        cmd: The R code you want to execute
        push: Dictionary of name:value pairs that you want to introduce to R session
        get: List of R object values that you want to get back
        
        returns:
        ---------
        if get is False, it returns nothing.
        If get is True, it returns the returned value from the R code.
        if get is not None, it returns a value, as specified by the get() function.
        """
        return self.exec(cmd, push, get)
    #edef
    
    def __str__(self):
        return "<BIU Rpy2 wrapper. See usage examples on github.>"
    #edef
    
    def __repr__(self):
        """
        Prepare a string representation of the class
        """
        return str(self)
    #edef
#eclass