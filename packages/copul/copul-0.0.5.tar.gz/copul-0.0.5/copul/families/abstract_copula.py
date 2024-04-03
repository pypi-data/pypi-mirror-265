import copy
import inspect
import itertools
import logging
import pathlib
import pickle
import random
import types
import warnings
from abc import ABC, abstractmethod

import numpy as np
import scipy
import scipy.optimize as opt
import sympy
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
from sympy.utilities.exceptions import SymPyDeprecationWarning

from copul import chatterjee
from copul.sympy_wrapper import SymPyFunctionWrapper

log = logging.getLogger(__name__)


class AbstractCopula(ABC):
    params = None
    u, v = sympy.symbols("u v", positive=True)
    intervals = None
    err_counter = 0
    log_cut_off = 4

    def __init__(self, **kwargs):
        self._are_class_vars(kwargs)
        for k, v in kwargs.items():
            if isinstance(v, str):
                v = getattr(self.__class__, v)
            setattr(self, k, v)
        self.params = [param for param in self.params if str(param) not in kwargs]

    def __str__(self):
        return self.__class__.__name__

    def __call__(self, **kwargs):
        new_copula = copy.copy(self)
        new_copula._are_class_vars(kwargs)
        for k, v in kwargs.items():
            if isinstance(v, str):
                v = getattr(self.__class__, v)
            setattr(new_copula, k, v)
        new_copula.params = [param for param in self.params if str(param) not in kwargs]
        return new_copula

    def _are_class_vars(self, kwargs):
        class_vars = set(dir(self))
        assert set(kwargs).issubset(
            class_vars
        ), f"keys: {set(kwargs)}, free symbols: {class_vars}"

    @property
    @abstractmethod
    def cdf(self) -> SymPyFunctionWrapper:
        pass

    @property
    @abstractmethod
    def is_absolutely_continuous(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_symmetric(self) -> bool:
        pass

    def rvs(self, n=1):
        """Sample a value from the copula"""
        func2_ = sympy.lambdify([self.u, self.v], self.cond_distr_2().func, ["numpy"])
        results = np.array([self._sample_val(func2_) for _ in range(n)])
        print(self.err_counter)
        return results

    def _sample_val(self, function):
        v = random.uniform(0, 1)
        t = random.uniform(0, 1)

        def func2(u: object) -> object:
            return function(u, v) - t

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            try:
                result = opt.root_scalar(
                    func2, x0=0.5, bracket=[0.000000001, 0.999999999]
                )
            except (ZeroDivisionError, ValueError, TypeError) as e:
                log.debug(f"{self.__class__.__name__}; {type(e).__name__}: {e}")
                self.err_counter += 1
                return self._get_visual_solution(func2), v
            if not result.converged:
                if not result.iterations:
                    print(self.__class__.__name__)
                self.err_counter += 1
                return self._get_visual_solution(func2), v
        return result.root, v

    @staticmethod
    def _get_visual_solution(func):
        x = np.linspace(0.001, 0.999, 1000)
        try:
            y = func(x)
        except ValueError:
            y = np.array([func(x_i) for x_i in x])
        return x[y.argmin()]

    @property
    def pdf(self):
        return sympy.simplify(sympy.diff(self.cond_distr_2(), self.u))

    def cond_distr_1(self) -> SymPyFunctionWrapper:
        return SymPyFunctionWrapper(sympy.diff(self.cdf, self.u))

    def cond_distr_2(self) -> SymPyFunctionWrapper:
        return SymPyFunctionWrapper(sympy.diff(self.cdf, self.v))

    def xi(self):
        print("xi")
        cond_distri_1 = sympy.simplify(self.cond_distr_1())
        print("cond_distr_1 sympy: ", cond_distri_1)
        print("cond_distr_1: ", sympy.latex(cond_distri_1))
        # sample_int = sympy.simplify(sympy.integrate(cond_distri_1, self.u))
        # print("sample_int sympy: ", sample_int)
        # print("sample_int: ", sympy.latex(sample_int))
        squared_cond_distr_1 = self._squared_cond_distr_1(self.u, self.v)
        print("squared_cond_distr_1 sympy: ", squared_cond_distr_1)
        print("squared_cond_distr_1: ", sympy.latex(squared_cond_distr_1))
        int_1 = self._xi_int_1(self.v)
        print("int_1 sympy: ", int_1)
        print("int_1: ", sympy.latex(int_1))
        int_2 = self._xi_int_2()
        print("int_2 sympy: ", int_2)
        print("int_2: ", sympy.latex(int_2))
        xi = self._xi()
        print("xi sympy: ", xi)
        print("xi: ", sympy.latex(xi))
        return SymPyFunctionWrapper(xi)

    def rho(self):
        print("rho")
        if isinstance(self.cdf, SymPyFunctionWrapper):
            cdf = sympy.simplify(self.cdf.func)
        else:
            cdf = self.cdf
        print("cdf sympy: ", cdf)
        print("cdf latex: ", sympy.latex(cdf))
        int_1 = self._rho_int_1()
        print("int_1 sympy: ", int_1)
        print("int_1 latex: ", sympy.latex(int_1))
        rho = self._rho()
        print("rho sympy: ", rho)
        print("rho latex: ", sympy.latex(rho))
        return rho

    def _rho(self):
        return sympy.simplify(12 * self._rho_int_2() - 3)

    def tau(self):
        print("tau")
        if isinstance(self.cdf, SymPyFunctionWrapper):
            integrand = self.cdf.func * self.pdf
        else:
            integrand = self.cdf * self.pdf
        print("integrand sympy: ", integrand)
        print("integrand latex: ", sympy.latex(integrand))
        int_1 = self._tau_int_1()
        print("int_1 sympy: ", int_1)
        print("int_1 latex: ", sympy.latex(int_1))
        int_2 = self._tau_int_2()
        print("int_2 sympy: ", int_2)
        print("int_2 latex: ", sympy.latex(int_2))
        tau = self._tau()
        print("tau sympy: ", tau)
        print("tau latex: ", sympy.latex(tau))
        return tau

    def _tau(self, *args):
        return 4 * self._tau_int_2() - 1

    def _xi(self):
        return sympy.simplify(6 * self._xi_int_2() - 2)

    def _xi_int_2(self):
        integrand = self._xi_int_1(self.v)
        return sympy.simplify(sympy.integrate(integrand, (self.v, 0, 1)))

    def _rho_int_2(self):
        return sympy.simplify(sympy.integrate(self._rho_int_1(), (self.v, 0, 1)))

    def _tau_int_2(self):
        return sympy.simplify(sympy.integrate(self._tau_int_1(), (self.v, 0, 1)))

    def _xi_int_1(self, v):
        squared_cond_distr_1 = self._squared_cond_distr_1(self.u, v)
        return sympy.simplify(sympy.integrate(squared_cond_distr_1, (self.u, 0, 1)))

    def _rho_int_1(self):
        return sympy.simplify(sympy.integrate(self.cdf.func, (self.u, 0, 1)))

    def _tau_int_1(self):
        return sympy.simplify(sympy.integrate(self.cdf.func * self.pdf, (self.u, 0, 1)))

    def _squared_cond_distr_1(self, u, v):
        return sympy.simplify(self.cond_distr_1().func ** 2)

    def plot(self, **kwargs):
        if not kwargs:
            return self.plot_cdf()
        for function_name, function in kwargs.items():
            free_symbol_dict = {str(s): getattr(self, str(s)) for s in self.params}
            if not free_symbol_dict:
                return self._plot3d(function, title=f"{function_name}", zlabel="")
            elif len([*free_symbol_dict]) == 1:
                param_str = [*free_symbol_dict][0]
                param_ = free_symbol_dict[param_str]
                interval = self.intervals[str(param_)]
                lower_bound = float(max(-10, interval.left))
                if interval.left_open:
                    lower_bound += 0.01
                upper_bound = float(min(interval.right, 10))
                if interval.right_open:
                    upper_bound -= 0.01
                x = np.linspace(lower_bound, upper_bound, 100)
                y = np.array([function.subs(str(param_), x_i) for x_i in x])
                try:
                    plt.plot(x, y, label=f"{function_name}")
                except TypeError as e:
                    if "complex" not in str(e):
                        raise e
                    y_list = [
                        function.subs(str(param_), x_i).evalf().as_real_imag()[0]
                        for x_i in x
                    ]
                    y = np.array(y_list)
                    plt.plot(x, y, label=f"{function_name}")
        plt.legend()
        plt.title(f"{self.__class__.__name__} {', '.join([*kwargs])}")
        plt.grid(True)
        pathlib.Path("images").mkdir(exist_ok=True)
        fig1 = plt.gcf()
        plt.show()
        plt.draw()
        fig1.savefig(f"images/{self.__class__.__name__}.png")
        # sympy.plot(function, (param, lower_bound, upper_bound))

    def plot_cdf(self, data=None):
        if data is None:
            return self._plot3d(
                self.cdf,
                title=f"{type(self).__name__} Copula",
                zlabel="CDF",
                zlim=(0, 1),
            )
        else:
            self._plot_cdf_from_data(data)

    @staticmethod
    def _plot_cdf_from_data(data):
        # Estimate the 2D histogram (which we'll use as a CDF)
        bins = [50, 50]  # Number of bins in each dimension
        hist, xedges, yedges = np.histogram2d(
            data[:, 0], data[:, 1], bins=bins, density=True
        )

        # Calculate the CDF from the histogram
        cdf = np.cumsum(np.cumsum(hist, axis=0), axis=1)
        cdf /= cdf[-1, -1]

        # Create a grid for plotting
        x, y = np.meshgrid(
            (xedges[1:] + xedges[:-1]) / 2, (yedges[1:] + yedges[:-1]) / 2
        )

        # Plot the 3D CDF
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(x, y, cdf, cmap="viridis")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("CDF")
        plt.show()

    def plot_pdf(self):
        free_symbol_dict = {str(s): getattr(self, str(s)) for s in self.params}
        pdf = self(**free_symbol_dict).pdf
        return self._plot3d(pdf, title=f"{type(self).__name__} Copula", zlabel="PDF")

    def _plot3d(self, func, title, zlabel, zlim=None):
        parameters = inspect.signature(func).parameters
        if isinstance(func, types.MethodType) and len(parameters) == 0:
            func = func()
        if isinstance(func, SymPyFunctionWrapper):
            f = sympy.lambdify((self.u, self.v), func.func)
        elif isinstance(func, sympy.Expr):
            f = sympy.lambdify((self.u, self.v), func)
        else:
            f = func

        # Create a meshgrid
        x = np.linspace(0.01, 0.99, 100)
        y = np.linspace(0.01, 0.99, 100)
        # Compute Z values for each pair of (X, Y)
        Z = np.zeros((len(y), len(x)))  # Initialize a matrix for Z values
        for i in range(len(x)):
            for j in range(len(y)):
                Z[j, i] = f(x[i], y[j])

        # Create a 3D plot
        X, Y = np.meshgrid(x, y)

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Plot the surface
        ax.plot_surface(X, Y, Z, cmap="viridis")
        ax.set_xlabel("u")
        ax.set_ylabel("v")
        ax.set_zlabel(zlabel)
        if zlim is not None:
            ax.set_zlim(*zlim)
        plt.title(title)
        plt.show()

    def plot_chatterjee(
        self,
        n_obs=10_000,
        n_params=20,
        params=None,
        plot_var=False,
        log_cut_off=None,
        ylim=(-1, 1),
    ):
        log.info(f"Plotting Chatterjee graph for {type(self).__name__} copula")
        mixed_params = self._mix_params(params) if params is not None else {}
        if log_cut_off is not None:
            self.log_cut_off = log_cut_off
            log_scale = True
        else:
            log_scale = False
        if not mixed_params:
            filename_suffix = ""
            self._plot_correlation_for(
                n_obs, n_params, self, plot_var, log_scale=log_scale
            )
            const_params = {*self.intervals} - set(
                {str(param) for param in self.params}
            )
            legend_suffix = ""
            for p in const_params:
                legend_suffix += ", "
                param = getattr(self, str(p))
                if isinstance(param, (property, sympy.Symbol)):
                    legend_suffix += f"$\\{p}=\\{param}$"
                else:
                    legend_suffix += f"$\\{p}={param}$"
                legend_suffix = " (with " + legend_suffix[2:] + ")"
                # replace ), with ,
                legend_suffix = legend_suffix.replace("),", ",")
        else:
            filename_suffix = "_xi"
        for mixed_param in mixed_params:
            new_copula = self(**mixed_param)
            label = ", ".join(
                f"$\\{k}=\\{v}$" if isinstance(v, (property, str)) else f"$\\{k}={v}$"
                for k, v in mixed_param.items()
            )
            self._construct_xi_graph_for(
                n_obs, n_params, new_copula, plot_var, label, log_scale
            )
            plt.ylabel(r"$\xi$")
            legend_suffix = ""
        # legend with n_obs and n_params
        plt.legend()
        if params is None:
            x_param = self.params[0]
        else:
            x_param = [param for param in self.params if str(param) not in [*params]][0]
        # x_label = (
        #     f"$\\{x_param}$ ({format(n_params, ',')} data points with $n_"
        #     + "{obs}"
        #     + f"={format(n_obs, ',')}$ each{legend_suffix})"
        # )
        x_label = f"$\\{x_param}${legend_suffix}"
        plt.xlabel(x_label)
        plt.ylim(0, 1) if mixed_params else plt.ylim(*ylim)
        plt.title(f"{self.__class__.__name__} Copula")
        plt.grid(True)
        pathlib.Path("images").mkdir(exist_ok=True)
        fig1 = plt.gcf()
        plt.show()
        plt.draw()
        fig1.savefig(f"images/{self.__class__.__name__}{filename_suffix}.png")
        pathlib.Path("images/functions").mkdir(exist_ok=True)

    def _construct_xi_graph_for(
        self, n_obs, n_params, new_copula, plot_var, label=r"$\xi$", log_scale=False
    ):
        params = new_copula.get_params(n_params, log_scale=log_scale)
        data_points = []
        for param in params:
            data = new_copula(**{str(new_copula.params[0]): param}).rvs(n_obs)
            xi = chatterjee.xi_ncalculate(data[:, 0], data[:, 1])
            if plot_var:
                xivar = chatterjee.xi_nvarcalculate(data[:, 0], data[:, 1])
                y_err = 3.291 * np.sqrt(xivar / n_obs)
            else:
                y_err = 0
            data_points.append((param, xi, y_err))
        data_points = np.array(data_points)
        x = data_points[:, 0]
        y = data_points[:, 1]
        y_errs = data_points[:, 2]
        cs = CubicSpline(x, y) if len(x) > 1 else lambda x_: x_
        # Create a dense set of x-values for plotting
        if log_scale:
            left_boundary = float(self.intervals[str(self.params[0])].inf)
            if isinstance(self.log_cut_off, tuple):
                x_dense = np.logspace(*self.log_cut_off, 500) + left_boundary
            else:
                x_dense = (
                    np.logspace(-self.log_cut_off, self.log_cut_off, 500)
                    + left_boundary
                )
        else:
            x_dense = np.linspace(params[0], params[-1], 500)
        # Compute the corresponding y-values
        y_dense = cs(x_dense)
        # Plot the results
        plt.scatter(x, y, label=label)
        cs_label = "Cubic Spline" if label == r"$\xi$" else None
        plt.plot(x_dense, y_dense, label=cs_label)
        if log_scale:
            plt.xscale("log")
        plt.fill_between(x, y - y_errs, y + y_errs, alpha=0.2)
        pathlib.Path("images/functions").mkdir(exist_ok=True, parents=True)
        if isinstance(cs, CubicSpline):
            with open(f"images/functions/{self.__class__.__name__}.pkl", "wb") as f:
                pickle.dump(cs, f)
        with open(f"images/functions/{self.__class__.__name__}Data.pkl", "wb") as f:
            pickle.dump(data_points, f)

    def _plot_correlation_for(
        self, n_obs, n_params, new_copula, plot_var, log_scale=False
    ):
        params = new_copula.get_params(n_params, log_scale=log_scale)
        data_points = []
        for param in params:
            specific_copula = new_copula(**{str(new_copula.params[0]): param})
            data = specific_copula.rvs(n_obs)
            xi = chatterjee.xi_ncalculate(data[:, 0], data[:, 1])
            rho = scipy.stats.spearmanr(data[:, 0], data[:, 1])
            tau = scipy.stats.kendalltau(data[:, 0], data[:, 1])
            if plot_var:
                xivar = chatterjee.xi_nvarcalculate(data[:, 0], data[:, 1])
                y_err = 3.291 * np.sqrt(xivar / n_obs)
            else:
                y_err = 0
            data_points.append((param, xi, y_err, rho[0], tau[0]))
        data_points = np.array(data_points)
        x = data_points[:, 0]
        y = data_points[:, 1]
        y_errs = data_points[:, 2]
        y_rho = data_points[:, 3]
        y_tau = data_points[:, 4]
        cs = CubicSpline(x, y) if len(x) > 1 else lambda x_: x_
        cs_rho = CubicSpline(x, y_rho) if len(x) > 1 else lambda x_: x_
        cs_tau = CubicSpline(x, y_tau) if len(x) > 1 else lambda x_: x_
        # Create a dense set of x-values for plotting
        if log_scale:
            inf = float(self.intervals[str(self.params[0])].inf)
            if isinstance(self.log_cut_off, tuple):
                x_dense = np.logspace(*self.log_cut_off, 500) + inf
            else:
                x_dense = np.logspace(-self.log_cut_off, self.log_cut_off, 500) + inf
        else:
            x_dense = np.linspace(params[0], params[-1], 500)
            inf = 0
        # Compute the corresponding y-values
        y_dense = cs(x_dense)
        y_rho_dense = cs_rho(x_dense)
        y_tau_dense = cs_tau(x_dense)
        # Plot the results
        plt.scatter(x - inf, y, label="Chatterjee's xi", marker="o")
        plt.scatter(x - inf, y_rho, label="Spearman's rho", marker="^")
        plt.scatter(x - inf, y_tau, label="Kendall's tau", marker="s")
        plt.plot(x_dense - inf, y_dense)
        plt.plot(x_dense - inf, y_rho_dense)
        plt.plot(x_dense - inf, y_tau_dense)
        if log_scale:
            plt.xscale("log")
        if log_scale and inf != 0.0:
            ticks = plt.xticks()[0]
            infimum = int(inf) if inf.is_integer() else inf
            new_ticklabels = [f"${infimum} + 10^{{{int(np.log10(t))}}}$" for t in ticks]
            plt.xticks(ticks, new_ticklabels)
            plt.xlim(x[0] - inf, x[-1] - inf)
        # plt.fill_between(x - inf, y - y_errs, y + y_errs, alpha=0.2)

        pathlib.Path("images/functions").mkdir(exist_ok=True, parents=True)
        if isinstance(cs, CubicSpline):
            with open(f"images/functions/{self.__class__.__name__}.pkl", "wb") as f:
                pickle.dump(cs, f)
        with open(f"images/functions/{self.__class__.__name__}Data.pkl", "wb") as f:
            pickle.dump(data_points, f)

    @staticmethod
    def _mix_params(params):
        cross_prod_keys = [
            key
            for key, value in params.items()
            if isinstance(value, (str, list, property))
        ]
        values_to_cross_product = [
            val if isinstance(val, list) else [val] for val in params.values()
        ]
        cross_prod = list(itertools.product(*values_to_cross_product))
        return [
            dict(zip(cross_prod_keys, cross_prod[i])) for i in range(len(cross_prod))
        ]

    def get_params(self, n_params, log_scale=False):
        interval = self.intervals[str(self.params[0])]
        if isinstance(interval, sympy.FiniteSet):
            return np.array([float(val) for val in interval])
        cut_off = self.log_cut_off if log_scale else 20
        if log_scale:
            inf = float(interval.inf)
            if isinstance(cut_off, tuple):
                param_array = np.logspace(*cut_off, n_params) + inf
            else:
                param_array = np.logspace(-cut_off, cut_off, n_params) + inf
        else:
            if isinstance(cut_off, tuple):
                left_border = float(max(interval.inf, cut_off[0]))
                right_border = float(min(cut_off[1], interval.sup))
            else:
                left_border = float(max(-cut_off, interval.inf))
                right_border = float(min(cut_off, interval.sup))
            if interval.left_open:
                left_border += 0.01
            if interval.right_open:
                right_border -= 0.01
            param_array = np.linspace(left_border, right_border, n_params)
        return param_array

    def lambda_L(self):
        return sympy.limit(self.cdf(v=self.u).func / self.u, self.u, 0, dir="+")

    def lambda_U(self):
        expr = (1 - self.cdf(v=self.u).func) / (1 - self.u)
        return sympy.simplify(2 - sympy.limit(expr, self.u, 1, dir="-"))

    def _check_extreme_mixed_term(self, my_log_pdf, u, v, x1, x2, y1, y2):
        min_term = my_log_pdf.subs(u, x1).subs(v, y1)
        max_term = my_log_pdf.subs(u, x2).subs(v, y2)
        mix_term_1 = my_log_pdf.subs(u, x1).subs(v, y2)
        mix_term_2 = my_log_pdf.subs(u, x2).subs(v, y1)
        extreme_term = min_term + max_term
        mixed_term = mix_term_1 + mix_term_2
        try:
            comparison = extreme_term * 0.9999999999999 < mixed_term
        except TypeError:
            comparison = (
                extreme_term.as_real_imag()[0] * 0.9999999999999
                < mixed_term.as_real_imag()[0]
            )
        if not isinstance(comparison, (bool, BooleanFalse, BooleanTrue)):
            comparison = comparison.evalf()
        if not isinstance(comparison, (bool, BooleanFalse, BooleanTrue)):
            u = self.u
            v = self.v
            return self._check_extreme_mixed_term(my_log_pdf, u, v, x1, x2, y1, y2)
        if comparison:
            # print("my_log_pdf: ", my_log_pdf)
            print("x1: ", x1, "x2: ", x2, "y1: ", y1, "y2: ", y2)
            # print("min_term: ", min_term)
            # print("max_term: ", max_term)
            # print("mix_term_1: ", mix_term_1)
            # print("mix_term_2: ", mix_term_2)
            # print("extreme_term: ", extreme_term)
            # print("mixed_term: ", mixed_term)
        return comparison

    def is_tp2(self, range_min=None, range_max=None):
        log.info(f"Checking if {type(self).__name__} copula is TP2")
        if (
            isinstance(self.is_absolutely_continuous, bool)
            and not self.is_absolutely_continuous
        ):
            return False
        range_min = -10 if range_min is None else range_min
        ranges = {}
        if len(self.params) == 1:
            n_interpolate = 20
        elif len(self.params) == 2:
            n_interpolate = 10
        else:
            n_interpolate = 6
        for param in self.params:
            interval = self.intervals[str(param)]
            range_min = float(max(interval.inf, range_min))
            if interval.left_open:
                range_min += 0.01
            param_range_max = 10 if range_max is None else range_max
            param_range_max = float(min(interval.end, param_range_max))
            if interval.right_open:
                param_range_max -= 0.01
            ranges[param] = np.linspace(range_min, param_range_max, n_interpolate)
        u = self.u
        v = self.v
        points = np.linspace(0.0001, 0.9999, 20)
        for param_values in itertools.product(*ranges.values()):
            param_dict = dict(zip(ranges.keys(), param_values))
            keys = [str(key) for key in ranges.keys()]
            param_dict_str = dict(zip(keys, param_values))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=SymPyDeprecationWarning)
                my_copul = self(**param_dict_str)
                if not my_copul.is_absolutely_continuous:
                    print("No density, False for params: ", param_dict)
                    continue
                my_log_pdf = sympy.log(my_copul.pdf)
            is_tp2 = True
            if not my_copul.is_absolutely_continuous:
                print("False for params: ", param_dict)
                continue
                # return False
            for i in range(len(points) - 1):
                for j in range(len(points) - 1):
                    if my_copul._check_extreme_mixed_term(
                        my_log_pdf,
                        str(u),
                        str(v),
                        points[i],
                        points[i + 1],
                        points[j],
                        points[j + 1],
                    ):
                        # return False
                        is_tp2 = False
                        break
                if not is_tp2:
                    break
            if is_tp2:
                print("True for params: ", param_dict)
            else:
                print("False for params: ", param_dict)
        return True

    def is_cis(self, range_min=None, range_max=None, cond_distr=1):
        log.info(f"Checking if {type(self).__name__} copula is CI")
        range_min = -10 if range_min is None else range_min
        n_interpolate = 20
        linspace = np.linspace(0.001, 0.999, 20)
        try:
            param = str(self.params[0])
        except IndexError:
            is_ci, is_cd = self._is_copula_cis(self, linspace, cond_distr=cond_distr)
            if is_ci:
                print("CI True for param: None")
            elif is_cd:
                print("CD True for param: None")
            else:
                print("False for param: None")
            return is_ci, is_cd
        interval = self.intervals[param]
        range_min = float(max(interval.inf, range_min))
        if interval.left_open:
            range_min += 0.01
        param_range_max = 10 if range_max is None else range_max
        param_range_max = float(min(interval.end, param_range_max))
        if interval.right_open:
            param_range_max -= 0.01
        param_range = np.linspace(range_min, param_range_max, n_interpolate)
        points = linspace
        for param_value in param_range:
            param_dict = {param: param_value}
            my_copul = self(**param_dict)
            is_cd, is_ci = self._is_copula_cis(my_copul, points)
            if is_ci:
                print(f"CI True for param: {param_value}")
            elif is_cd:
                print(f"CD True for param: {param_value}")
            else:
                print(f"False for param: {param_value}")
            if not is_ci or not is_cd:
                continue
        return is_ci, is_cd

    def _is_copula_cis(self, my_copul, points, cond_distr=1):
        is_ci = True
        is_cd = True
        if cond_distr == 1:
            cond_method = my_copul.cond_distr_1
        elif cond_distr == 2:
            cond_method = my_copul.cond_distr_2
        else:
            raise ValueError("cond_distr must be 1 or 2")
        try:
            cond_method = cond_method().func
        except TypeError:
            for v in points:
                for u, next_u in zip(points[:-1], points[1:]):
                    if cond_distr == 1:
                        val1 = cond_method(next_u, v) * 0.9999999
                        val2 = cond_method(u, v)
                    else:
                        val1 = cond_method(v, next_u) * 0.9999999
                        val2 = cond_method(v, u)
                    if val1 > val2:
                        is_ci = False
                    if val2 < val1:
                        is_cd = False
                    if not is_ci and not is_cd:
                        break
        else:
            for v in points:
                cond_distr_eval_u = cond_distr.subs(my_copul.v, v)
                for u, next_u in zip(points[:-1], points[1:]):
                    eval_u = cond_distr_eval_u.subs(my_copul.u, u)
                    eval_next_u = cond_distr_eval_u.subs(my_copul.u, next_u)
                    if eval_next_u * 0.9999999 > eval_u:
                        is_ci = False
                    if eval_next_u < eval_u * 0.9999999:
                        is_cd = False
                    if not is_ci and not is_cd:
                        break
                if not is_ci and not is_cd:
                    break
        return is_cd, is_ci
