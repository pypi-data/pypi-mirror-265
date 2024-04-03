import pandas as pd
from mypy_extensions import VarArg
import numpy as np
from uncertainties import ufloat

from dataclasses import dataclass, field
from typing import List, Dict, Callable, TypeAlias, Iterable, Any


scalar: TypeAlias = int | float
array: TypeAlias = np.ndarray | pd.Series
numerical: TypeAlias = scalar | array


@dataclass(repr=True)
class FitResult:
    function: Callable[[numerical, VarArg(scalar)], numerical] = field(repr=False)
    parameter_names: List[str]
    parameter_values: np.ndarray
    parameter_sigmas: np.ndarray
    reduced_chi_squared: float | None = field(default=None)

    def eval(self, x: numerical) -> float | np.ndarray:
        """Calculated values of the fitted function"""
        result = self.function(x, *self.parameter_values)
        if isinstance(result, Iterable):
            return np.array(result)
        else:
            return float(result)

    def as_dict(self, chi_square: bool = False) -> dict[str, Any | float]:
        result: dict = dict()
        for name, x, sigma in zip(self.parameter_names, self.parameter_values, self.parameter_sigmas):
            result[name] = ufloat(x, sigma)

        if chi_square:
            result["reduced_chi_squared"] = self.reduced_chi_squared

        return result

    def set_reduced_chi_squared(self, x: array, y: array, sigma: array) -> float:
        chi_squared = ((self.eval(x) - y)**2/sigma**2).sum()
        result: float = chi_squared / (len(x) - len(self.parameter_names))
        self.reduced_chi_squared = result
        return result
