'Base classes for kinetic backgrounds.'


from abc import ABCMeta, abstractmethod
import numpy as np


class Maxwellian(metaclass=ABCMeta):
    r""" Base class for a Maxwellian distribution function. 
    It is defined on :math:`[0, 1]^3 \times \mathbb R^n, n \geq 1,` 
    with logical position coordinates :math:`\boldsymbol{\eta} \in [0, 1]^3`:

    .. math::

        f(\boldsymbol{\eta}, v_1,\ldots,v_n) = n(\boldsymbol{\eta}) \prod_{i=1}^n \frac{1}{\sqrt{2\pi}\,v_{\mathrm{th},i}(\boldsymbol{\eta})}
        \exp\left[-\frac{(v_i-u_i(\boldsymbol{\eta}))^2}{2\,v_{\mathrm{th},i}(\boldsymbol{\eta})^2}\right],

    defined by its velocity moments: the density :math:`n(\boldsymbol{\eta})`,
    the mean-velocities :math:`u_i(\boldsymbol{\eta})`,
    and the thermal velocities :math:`v_{\mathrm{th},i}(\boldsymbol{\eta})`.
    """

    @property
    @abstractmethod
    def vdim(self):
        """ Dimension of the velocity space (vdim = n).
        """
        pass

    @property
    @abstractmethod
    def is_polar(self):
        """ List of booleans. True if the velocity coordinates are polar coordinates.
        """
        pass

    @abstractmethod
    def n(self, *etas):
        """ Number density (0-form). 

        Parameters
        ----------
        etas : numpy.arrays
            Evaluation points. All arrays must be of same shape (can be 1d for flat evaluation).

        Returns
        -------
        A numpy.array with the density evaluated at evaluation points (same shape as etas).
        """
        pass

    @abstractmethod
    def u(self, *etas):
        """ Mean velocities (Cartesian components evaluated at x = F(eta)).

        Parameters
        ----------
        etas : numpy.arrays
            Evaluation points. All arrays must be of same shape (can be 1d for flat evaluation).

        Returns
        -------
        A numpy.array with the mean velocity evaluated at evaluation points (one dimension more than etas).
        The additional dimension is in the first index.
        """
        pass

    @abstractmethod
    def vth(self, *etas):
        """ Thermal velocities (0-forms).

        Parameters
        ----------
        etas : numpy.arrays
            Evaluation points. All arrays must be of same shape (can be 1d for flat evaluation).

        Returns
        -------
        A numpy.array with the thermal velocity evaluated at evaluation points (one dimension more than etas).
        The additional dimension is in the first index.
        """
        pass

    def gaussian(self, v, u=0., vth=1., is_polar=False):
        """1-dim. normal distribution, to which array-valued mean- and thermal velocities can be passed.

        Parameters
        ----------
        v : float | array-like
            Velocity coordinate(s).

        u : float | array-like
            Mean velocity evaluated at position array.

        vth : float | array-like
            Thermal velocity evaluated at position array, same shape as u.

        is_polar : boolean
            True if the velocity coordinate is the radial of polar coordinates.

        Returns
        -------
        An array of size(u).
        """

        if isinstance(v, np.ndarray) and isinstance(u, np.ndarray):
            assert v.shape == u.shape, f'{v.shape = } but {u.shape = }'

        if not is_polar:
            return 1./(np.sqrt(2.*np.pi) * vth) * np.exp(-(v - u)**2/(2.*vth**2))
        else:
            return 1./vth**2 * v * np.exp(-(v - u)**2/(2.*vth**2))

    def __call__(self, *args):
        """ Evaluates the Maxwellian distribution function M(etas, v1, ..., vn).

        There are two use-cases for this function in the code:

        1. Evaluating for particles ("flat evaluation", inputs are all 1D of length N_p)
        2. Evaluating the function on a meshgrid (in phase space).

        Hence all arguments must always have 

        1. the same shape
        2. either ndim = 1 or ndim = 3 + vdim.

        Parameters
        ----------
        *args : array_like
            Position-velocity arguments in the order eta1, eta2, eta3, v1, ..., vn.

        Returns
        -------
        f : np.ndarray
            The evaluated Maxwellian.
        """

        # Check that all args have the same shape
        shape0 = np.shape(args[0])
        for i, arg in enumerate(args):
            assert np.shape(
                arg) == shape0, f'Argument {i} has {np.shape(arg) = }, but must be {shape0 = }.'
            assert np.ndim(arg) == 1 or np.ndim(
                arg) == 3 + self.vdim, f'{np.ndim(arg) = } not allowed for Maxwellian evaluation.'  # flat or meshgrid evaluation

        # Get result evaluated at eta's
        res = self.n(*args[:-self.vdim])
        us = self.u(*args[:-self.vdim])
        vths = self.vth(*args[:-self.vdim])

        # take care of correct broadcasting, assuming args come from phase space meshgrid
        if np.ndim(args[0]) > 3:
            # move eta axes to the back
            arg_t = np.moveaxis(args[0], 0, -1)
            arg_t = np.moveaxis(arg_t, 0, -1)
            arg_t = np.moveaxis(arg_t, 0, -1)

            # broadcast
            res_broad = res + 0.*arg_t

            # move eta axes to the front
            res = np.moveaxis(res_broad, -1, 0)
            res = np.moveaxis(res, -1, 0)
            res = np.moveaxis(res, -1, 0)

        # Multiply result with gaussian in v's
        for i, v in enumerate(args[-self.vdim:]):
            # correct broadcasting
            if np.ndim(args[0]) > 3:
                u_broad = us[i] + 0.*arg_t
                u = np.moveaxis(u_broad, -1, 0)
                u = np.moveaxis(u, -1, 0)
                u = np.moveaxis(u, -1, 0)

                vth_broad = vths[i] + 0.*arg_t
                vth = np.moveaxis(vth_broad, -1, 0)
                vth = np.moveaxis(vth, -1, 0)
                vth = np.moveaxis(vth, -1, 0)
            else:
                u = us[i]
                vth = vths[i]

            res *= self.gaussian(v, u=u, vth=vth,
                                 is_polar=self.is_polar[i])

        return res
