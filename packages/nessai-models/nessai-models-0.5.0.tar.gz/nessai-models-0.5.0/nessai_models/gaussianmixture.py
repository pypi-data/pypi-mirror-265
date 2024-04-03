# -*- coding: utf-8 -*-
"""
Gaussian mixture models.
"""
from typing import Dict, List, Optional, Sequence, Union

import numpy as np
from scipy.stats import multivariate_normal, norm
from scipy.special import logsumexp

from .base import BaseModel, NDimensionalModel, UniformPriorMixin


class GaussianMixture(UniformPriorMixin, NDimensionalModel):
    """A Gaussian mixture model with n Gaussians defined on [-10, 10]^n.

    Parameters
    ----------
    dims : int
        Number of dimensions
    n_gaussians : int
        Number of Gaussians.
    weights : Optional[Union[Sequence[float], np.ndarray]]
        Weights for each of the Gaussian. Must sum to one.
    config : Optional[Union[List[Dict[str, numpy.ndarray]]]]
        List of configurations for each Gaussian. Each dictionary should have
        a mean and cov key.
    random_state : Optional[numpy.random.RandomState]
        Random state to use for generation configuration if `config` is not
        specified. If not specified `seed` is used instead.
    seed : int
        Random seed for seeding random number generation.
    bounds : Union[Sequence[float], numpy.ndarray]
        Prior bounds.
    """

    def __init__(
        self,
        dims: int = 4,
        n_gaussians: int = 2,
        weights: Optional[Union[Sequence[float], np.ndarray]] = None,
        config: Optional[List[Dict[str, np.ndarray]]] = None,
        random_state: Optional[np.random.RandomState] = None,
        seed: int = 1234,
        bounds: Union[Sequence[float], np.ndarray] = [-10.0, 10.0],
    ) -> None:
        super().__init__(dims, bounds)

        if random_state is None:
            random_state = np.random.RandomState(seed=seed)

        self.n_gaussians = n_gaussians
        if weights is None:
            self.weights = np.ones(n_gaussians) / n_gaussians
        else:
            if len(weights) != n_gaussians:
                ValueError("Length of weights must match number of Gaussians")
            self.weights = np.array(weights)
        self.gaussians = n_gaussians * [None]
        if config is None:
            config = n_gaussians * [None]
        elif len(config) != n_gaussians:
            raise RuntimeError("Config does not match number of Gaussians")

        for n in range(n_gaussians):
            if config[n] is None:
                config[n] = dict(
                    mean=random_state.uniform(bounds[0], bounds[1], dims),
                    cov=3 * random_state.rand() * np.eye(dims),
                )
            self.gaussians[n] = multivariate_normal(**config[n])

    def log_likelihood(self, x: np.ndarray) -> np.ndarray:
        """Log-likelihood for the mixture of Gaussians."""
        _x = self.unstructured_view(x)
        b = np.broadcast_to(self.weights, (x.size, self.n_gaussians)).T
        arg = np.array([g.logpdf(_x) for g in self.gaussians])
        if arg.ndim == 1:
            arg = arg[:, np.newaxis]
        log_l = logsumexp(arg, b=b, axis=0)
        return log_l


class GaussianMixtureWithData(UniformPriorMixin, BaseModel):
    """
    A Gaussian mixture model with two peaks that uses samples and fits the
    the means standard deviations and weight.

    Based on the example from cpnest: \
        https://github.com/johnveitch/cpnest/blob/master/examples/gaussianmixture.py

    The parameters to estimate are the means, standard deviations and the
    weight.

    Parameters
    ----------
    n : int
        Number of data points to use.
    """

    def __init__(self, n: int = 1000) -> None:
        self.names = ["mu1", "sigma1", "mu2", "sigma2", "weight"]
        self.bounds = {
            "mu1": [-3, 3],
            "sigma1": [0.01, 1],
            "mu2": [-3, 3],
            "sigma2": [0.01, 1.0],
            "weight": [0.0, 1.0],
        }

        self.truth = {
            "mu1": 0.5,
            "sigma1": 0.5,
            "mu2": -1.5,
            "sigma2": 0.03,
            "weight": 0.2,
        }
        self.gaussian1 = norm(self.truth["mu1"], scale=self.truth["sigma1"])
        self.gaussian2 = norm(self.truth["mu2"], scale=self.truth["sigma2"])

        n1 = int(self.truth["weight"] * n)
        n2 = n - n1

        self.data = np.concatenate(
            [self.gaussian1.rvs(size=n1), self.gaussian2.rvs(size=n2)]
        )

    def log_likelihood(self, x: np.ndarray) -> np.ndarray:
        """Returns log likelihood of given live point."""
        w = x["weight"][..., np.newaxis]
        mu1 = x["mu1"][..., np.newaxis]
        mu2 = x["mu2"][..., np.newaxis]
        sigma1 = x["sigma1"][..., np.newaxis]
        sigma2 = x["sigma2"][..., np.newaxis]
        log_l1 = np.sum(
            np.log(w)
            - np.log(sigma1)
            - 0.5 * ((self.data - mu1) / sigma1) ** 2,
            axis=-1,
        )
        log_l2 = np.sum(
            np.log(1.0 - w)
            - np.log(sigma2)
            - 0.5 * ((self.data - mu2) / sigma2) ** 2,
            axis=-1,
        )
        log_l = np.logaddexp(log_l1, log_l2)
        return log_l
