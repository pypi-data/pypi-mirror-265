from .gaussianmixture import GaussianMixture
import numpy as np


class SlabSpike(GaussianMixture):
    """Slab plus spike model.

    Both the slab and spike are Gaussian and centred at zero and have
    diagonal covariance matrices. The slab has a covariance of 1 and the
    covariance of the spike is :code:`spike_scale` times that.

    See also the GaussianMixture and Brewer models.

    Parameters
    ----------
    dims : int
        Number of dimensions
    spike_scale : float
        Scale used to set to the covariance of the spike.
    kwargs :
        Keyword arguments passed to :code:`GaussianMixture` class. Note, the
        :code:`config:` keyword argument will always be overwritten.
    """

    def __init__(self, dims: int = 3, spike_scale: float = 1e-3, **kwargs):
        if "config" not in kwargs.keys():
            mu = np.zeros(dims)
            cov_slab = np.diag(np.ones(dims))
            cov_spike = np.diag(np.ones(dims) * spike_scale)
            kwargs["config"] = [
                dict(mean=mu, cov=cov_slab),
                dict(mean=mu, cov=cov_spike),
            ]
        return super().__init__(dims=dims, **kwargs)
