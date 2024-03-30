"""
Generate samples of synthetic data sets.
"""

# ported from sklearn/datasets/_samples_generator.py
# Authors: B. Thirion, G. Varoquaux, A. Gramfort, V. Michel, O. Grisel,
#          G. Louppe, J. Nothman
# License: BSD 3 clause

import numbers, warnings
import numpy as np

def check_random_state(seed):
    """Turn seed into a np.random.RandomState instance.

    Parameters
    ----------
    seed : None, int or instance of RandomState
        If seed is None, return the RandomState singleton used by np.random.
        If seed is an int, return a new RandomState instance seeded with seed.
        If seed is already a RandomState instance, return it.
        Otherwise raise ValueError.

    Returns
    -------
    :class:`numpy:numpy.random.RandomState`
        The random state object based on `seed` parameter.

    Examples
    --------
    >>> from sklearn.utils.validation import check_random_state
    >>> check_random_state(42)
    RandomState(MT19937) at 0x...
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, numbers.Integral):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError(
        "%r cannot be used to seed a numpy.random.RandomState instance" % seed
    )


def make_friedman1(n_samples=100, n_features=10, *, noise=0.0, random_state=None):
    """Generate the "Friedman #1" regression problem.

    This dataset is described in Friedman [1] and Breiman [2].

    Inputs `X` are independent features uniformly distributed on the interval
    [0, 1]. The output `y` is created according to the formula::

        y(X) = 10 * sin(pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 \
+ 10 * X[:, 3] + 5 * X[:, 4] + noise * N(0, 1).

    Out of the `n_features` features, only 5 are actually used to compute
    `y`. The remaining features are independent of `y`.

    The number of features has to be >= 5.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    n_features : int, default=10
        The number of features. Should be at least 5.

    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] J. Friedman, "Multivariate adaptive regression splines", The Annals
           of Statistics 19 (1), pages 1-67, 1991.

    .. [2] L. Breiman, "Bagging predictors", Machine Learning 24,
           pages 123-140, 1996.

    Examples
    --------
    >>> from sklearn.datasets import make_friedman1
    >>> X, y = make_friedman1(random_state=42)
    >>> X.shape
    (100, 10)
    >>> y.shape
    (100,)
    >>> list(y[:3])
    [16.8..., 5.8..., 9.4...]
    """
    generator = check_random_state(random_state)

    X = generator.uniform(size=(n_samples, n_features))
    y = (
        10 * np.sin(np.pi * X[:, 0] * X[:, 1])
        + 20 * (X[:, 2] - 0.5) ** 2
        + 10 * X[:, 3]
        + 5 * X[:, 4]
        + noise * generator.standard_normal(size=(n_samples))
    )

    return X, y


def make_friedman2(n_samples=100, *, noise=0.0, random_state=None):
    """Generate the "Friedman #2" regression problem.

    This dataset is described in Friedman [1] and Breiman [2].

    Inputs `X` are 4 independent features uniformly distributed on the
    intervals::

        0 <= X[:, 0] <= 100,
        40 * pi <= X[:, 1] <= 560 * pi,
        0 <= X[:, 2] <= 1,
        1 <= X[:, 3] <= 11.

    The output `y` is created according to the formula::

        y(X) = (X[:, 0] ** 2 + (X[:, 1] * X[:, 2] \
 - 1 / (X[:, 1] * X[:, 3])) ** 2) ** 0.5 + noise * N(0, 1).

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 4)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] J. Friedman, "Multivariate adaptive regression splines", The Annals
           of Statistics 19 (1), pages 1-67, 1991.

    .. [2] L. Breiman, "Bagging predictors", Machine Learning 24,
           pages 123-140, 1996.

    Examples
    --------
    >>> from sklearn.datasets import make_friedman2
    >>> X, y = make_friedman2(random_state=42)
    >>> X.shape
    (100, 4)
    >>> y.shape
    (100,)
    >>> list(y[:3])
    [1229.4..., 27.0..., 65.6...]
    """
    generator = check_random_state(random_state)

    X = generator.uniform(size=(n_samples, 4))
    X[:, 0] *= 100
    X[:, 1] *= 520 * np.pi
    X[:, 1] += 40 * np.pi
    X[:, 3] *= 10
    X[:, 3] += 1

    y = (
        X[:, 0] ** 2 + (X[:, 1] * X[:, 2] - 1 / (X[:, 1] * X[:, 3])) ** 2
    ) ** 0.5 + noise * generator.standard_normal(size=(n_samples))

    return X, y


def make_friedman3(n_samples=100, *, noise=0.0, random_state=None):
    """Generate the "Friedman #3" regression problem.

    This dataset is described in Friedman [1] and Breiman [2].

    Inputs `X` are 4 independent features uniformly distributed on the
    intervals::

        0 <= X[:, 0] <= 100,
        40 * pi <= X[:, 1] <= 560 * pi,
        0 <= X[:, 2] <= 1,
        1 <= X[:, 3] <= 11.

    The output `y` is created according to the formula::

        y(X) = arctan((X[:, 1] * X[:, 2] - 1 / (X[:, 1] * X[:, 3])) \
/ X[:, 0]) + noise * N(0, 1).

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 4)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] J. Friedman, "Multivariate adaptive regression splines", The Annals
           of Statistics 19 (1), pages 1-67, 1991.

    .. [2] L. Breiman, "Bagging predictors", Machine Learning 24,
           pages 123-140, 1996.

    Examples
    --------
    >>> from sklearn.datasets import make_friedman3
    >>> X, y = make_friedman3(random_state=42)
    >>> X.shape
    (100, 4)
    >>> y.shape
    (100,)
    >>> list(y[:3])
    [1.5..., 0.9..., 0.4...]
    """
    generator = check_random_state(random_state)

    X = generator.uniform(size=(n_samples, 4))
    X[:, 0] *= 100
    X[:, 1] *= 520 * np.pi
    X[:, 1] += 40 * np.pi
    X[:, 3] *= 10
    X[:, 3] += 1

    y = np.arctan(
        (X[:, 1] * X[:, 2] - 1 / (X[:, 1] * X[:, 3])) / X[:, 0]
    ) + noise * generator.standard_normal(size=(n_samples))

    return X, y


def make_sparse_coded_signal(
    n_samples,
    *,
    n_components,
    n_features,
    n_nonzero_coefs,
    random_state=None,
    data_transposed="deprecated",
):
    """Generate a signal as a sparse combination of dictionary elements.

    Returns a matrix `Y = DX`, such that `D` is of shape `(n_features, n_components)`,
    `X` is of shape `(n_components, n_samples)` and each column of `X` has exactly
    `n_nonzero_coefs` non-zero elements.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int
        Number of samples to generate.

    n_components : int
        Number of components in the dictionary.

    n_features : int
        Number of features of the dataset to generate.

    n_nonzero_coefs : int
        Number of active (non-zero) coefficients in each sample.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    data_transposed : bool, default=False
        By default, Y, D and X are not transposed.

        .. versionadded:: 1.1

        .. versionchanged:: 1.3
            Default value changed from True to False.

        .. deprecated:: 1.3
            `data_transposed` is deprecated and will be removed in 1.5.

    Returns
    -------
    data : ndarray of shape (n_features, n_samples) or (n_samples, n_features)
        The encoded signal (Y). The shape is `(n_samples, n_features)` if
        `data_transposed` is False, otherwise it's `(n_features, n_samples)`.

    dictionary : ndarray of shape (n_features, n_components) or \
            (n_components, n_features)
        The dictionary with normalized components (D). The shape is
        `(n_components, n_features)` if `data_transposed` is False, otherwise it's
        `(n_features, n_components)`.

    code : ndarray of shape (n_components, n_samples) or (n_samples, n_components)
        The sparse code such that each column of this matrix has exactly
        n_nonzero_coefs non-zero items (X). The shape is `(n_samples, n_components)`
        if `data_transposed` is False, otherwise it's `(n_components, n_samples)`.

    Examples
    --------
    >>> from sklearn.datasets import make_sparse_coded_signal
    >>> data, dictionary, code = make_sparse_coded_signal(
    ...     n_samples=50,
    ...     n_components=100,
    ...     n_features=10,
    ...     n_nonzero_coefs=4,
    ...     random_state=0
    ... )
    >>> data.shape
    (50, 10)
    >>> dictionary.shape
    (100, 10)
    >>> code.shape
    (50, 100)
    """
    generator = check_random_state(random_state)

    # generate dictionary
    D = generator.standard_normal(size=(n_features, n_components))
    D /= np.sqrt(np.sum((D**2), axis=0))

    # generate code
    X = np.zeros((n_components, n_samples))
    for i in range(n_samples):
        idx = np.arange(n_components)
        generator.shuffle(idx)
        idx = idx[:n_nonzero_coefs]
        X[idx, i] = generator.standard_normal(size=n_nonzero_coefs)

    # encode signal
    Y = np.dot(D, X)

    # TODO(1.5) remove data_transposed
    # raise warning if data_transposed is not passed explicitly
    if data_transposed != "deprecated":
        warnings.warn(
            "data_transposed was deprecated in version 1.3 and will be removed in 1.5.",
            FutureWarning,
        )
    else:
        data_transposed = False

    # transpose if needed
    if not data_transposed:
        Y, D, X = Y.T, D.T, X.T

    return map(np.squeeze, (Y, D, X))


def make_sparse_uncorrelated(n_samples=100, n_features=10, *, random_state=None):
    """Generate a random regression problem with sparse uncorrelated design.

    This dataset is described in Celeux et al [1]. as::

        X ~ N(0, 1)
        y(X) = X[:, 0] + 2 * X[:, 1] - 2 * X[:, 2] - 1.5 * X[:, 3]

    Only the first 4 features are informative. The remaining features are
    useless.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    n_features : int, default=10
        The number of features.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] G. Celeux, M. El Anbari, J.-M. Marin, C. P. Robert,
           "Regularization in regression: comparing Bayesian and frequentist
           methods in a poorly informative situation", 2009.

    Examples
    --------
    >>> from sklearn.datasets import make_sparse_uncorrelated
    >>> X, y = make_sparse_uncorrelated(random_state=0)
    >>> X.shape
    (100, 10)
    >>> y.shape
    (100,)
    """
    generator = check_random_state(random_state)

    X = generator.normal(loc=0, scale=1, size=(n_samples, n_features))
    y = generator.normal(
        loc=(X[:, 0] + 2 * X[:, 1] - 2 * X[:, 2] - 1.5 * X[:, 3]),
        scale=np.ones(n_samples),
    )

    return X, y


def make_swiss_roll(n_samples=100, *, noise=0.0, random_state=None, hole=False):
    """Generate a swiss roll dataset.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of sample points on the Swiss Roll.

    noise : float, default=0.0
        The standard deviation of the gaussian noise.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    hole : bool, default=False
        If True generates the swiss roll with hole dataset.

    Returns
    -------
    X : ndarray of shape (n_samples, 3)
        The points.

    t : ndarray of shape (n_samples,)
        The univariate position of the sample according to the main dimension
        of the points in the manifold.

    Notes
    -----
    The algorithm is from Marsland [1].

    References
    ----------
    .. [1] S. Marsland, "Machine Learning: An Algorithmic Perspective", 2nd edition,
           Chapter 6, 2014.
           https://homepages.ecs.vuw.ac.nz/~marslast/Code/Ch6/lle.py

    Examples
    --------
    >>> from sklearn.datasets import make_swiss_roll
    >>> X, t = make_swiss_roll(noise=0.05, random_state=0)
    >>> X.shape
    (100, 3)
    >>> t.shape
    (100,)
    """
    generator = check_random_state(random_state)

    if not hole:
        t = 1.5 * np.pi * (1 + 2 * generator.uniform(size=n_samples))
        y = 21 * generator.uniform(size=n_samples)
    else:
        corners = np.array(
            [[np.pi * (1.5 + i), j * 7] for i in range(3) for j in range(3)]
        )
        corners = np.delete(corners, 4, axis=0)
        corner_index = generator.choice(8, n_samples)
        parameters = generator.uniform(size=(2, n_samples)) * np.array([[np.pi], [7]])
        t, y = corners[corner_index].T + parameters

    x = t * np.cos(t)
    z = t * np.sin(t)

    X = np.vstack((x, y, z))
    X += noise * generator.standard_normal(size=(3, n_samples))
    X = X.T
    t = np.squeeze(t)

    return X, t


def make_s_curve(n_samples=100, *, noise=0.0, random_state=None):
    """Generate an S curve dataset.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of sample points on the S curve.

    noise : float, default=0.0
        The standard deviation of the gaussian noise.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 3)
        The points.

    t : ndarray of shape (n_samples,)
        The univariate position of the sample according
        to the main dimension of the points in the manifold.

    Examples
    --------
    >>> from sklearn.datasets import make_s_curve
    >>> X, t = make_s_curve(noise=0.05, random_state=0)
    >>> X.shape
    (100, 3)
    >>> t.shape
    (100,)
    """
    generator = check_random_state(random_state)

    t = 3 * np.pi * (generator.uniform(size=(1, n_samples)) - 0.5)
    X = np.empty(shape=(n_samples, 3), dtype=np.float64)
    X[:, 0] = np.sin(t)
    X[:, 1] = 2.0 * generator.uniform(size=n_samples)
    X[:, 2] = np.sign(t) * (np.cos(t) - 1)
    X += noise * generator.standard_normal(size=(3, n_samples)).T
    t = np.squeeze(t)

    return X, t


def _shuffle(data, random_state=None):
    generator = check_random_state(random_state)
    n_rows, n_cols = data.shape
    row_idx = generator.permutation(n_rows)
    col_idx = generator.permutation(n_cols)
    result = data[row_idx][:, col_idx]
    return result, row_idx, col_idx


def make_biclusters(
    shape,
    n_clusters,
    *,
    noise=0.0,
    minval=10,
    maxval=100,
    shuffle=True,
    random_state=None,
):
    """Generate a constant block diagonal structure array for biclustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    shape : tuple of shape (n_rows, n_cols)
        The shape of the result.

    n_clusters : int
        The number of biclusters.

    noise : float, default=0.0
        The standard deviation of the gaussian noise.

    minval : float, default=10
        Minimum value of a bicluster.

    maxval : float, default=100
        Maximum value of a bicluster.

    shuffle : bool, default=True
        Shuffle the samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape `shape`
        The generated array.

    rows : ndarray of shape (n_clusters, X.shape[0])
        The indicators for cluster membership of each row.

    cols : ndarray of shape (n_clusters, X.shape[1])
        The indicators for cluster membership of each column.

    See Also
    --------
    make_checkerboard: Generate an array with block checkerboard structure for
        biclustering.

    References
    ----------

    .. [1] Dhillon, I. S. (2001, August). Co-clustering documents and
        words using bipartite spectral graph partitioning. In Proceedings
        of the seventh ACM SIGKDD international conference on Knowledge
        discovery and data mining (pp. 269-274). ACM.

    Examples
    --------
    >>> from sklearn.datasets import make_biclusters
    >>> data, rows, cols = make_biclusters(
    ...     shape=(10, 20), n_clusters=2, random_state=42
    ... )
    >>> data.shape
    (10, 20)
    >>> rows.shape
    (2, 10)
    >>> cols.shape
    (2, 20)
    """
    generator = check_random_state(random_state)
    n_rows, n_cols = shape
    consts = generator.uniform(minval, maxval, n_clusters)

    # row and column clusters of approximately equal sizes
    row_sizes = generator.multinomial(n_rows, np.repeat(1.0 / n_clusters, n_clusters))
    col_sizes = generator.multinomial(n_cols, np.repeat(1.0 / n_clusters, n_clusters))

    row_labels = np.hstack(
        [np.repeat(val, rep) for val, rep in zip(range(n_clusters), row_sizes)]
    )
    col_labels = np.hstack(
        [np.repeat(val, rep) for val, rep in zip(range(n_clusters), col_sizes)]
    )

    result = np.zeros(shape, dtype=np.float64)
    for i in range(n_clusters):
        selector = np.outer(row_labels == i, col_labels == i)
        result[selector] += consts[i]

    if noise > 0:
        result += generator.normal(scale=noise, size=result.shape)

    if shuffle:
        result, row_idx, col_idx = _shuffle(result, random_state)
        row_labels = row_labels[row_idx]
        col_labels = col_labels[col_idx]

    rows = np.vstack([row_labels == c for c in range(n_clusters)])
    cols = np.vstack([col_labels == c for c in range(n_clusters)])

    return result, rows, cols

def make_checkerboard(
    shape,
    n_clusters,
    *,
    noise=0.0,
    minval=10,
    maxval=100,
    shuffle=True,
    random_state=None,
):
    """Generate an array with block checkerboard structure for biclustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    shape : tuple of shape (n_rows, n_cols)
        The shape of the result.

    n_clusters : int or array-like or shape (n_row_clusters, n_column_clusters)
        The number of row and column clusters.

    noise : float, default=0.0
        The standard deviation of the gaussian noise.

    minval : float, default=10
        Minimum value of a bicluster.

    maxval : float, default=100
        Maximum value of a bicluster.

    shuffle : bool, default=True
        Shuffle the samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape `shape`
        The generated array.

    rows : ndarray of shape (n_clusters, X.shape[0])
        The indicators for cluster membership of each row.

    cols : ndarray of shape (n_clusters, X.shape[1])
        The indicators for cluster membership of each column.

    See Also
    --------
    make_biclusters : Generate an array with constant block diagonal structure
        for biclustering.

    References
    ----------
    .. [1] Kluger, Y., Basri, R., Chang, J. T., & Gerstein, M. (2003).
        Spectral biclustering of microarray data: coclustering genes
        and conditions. Genome research, 13(4), 703-716.

    Examples
    --------
    >>> from sklearn.datasets import make_checkerboard
    >>> data, rows, columns = make_checkerboard(shape=(300, 300), n_clusters=10,
    ...                                         random_state=42)
    >>> data.shape
    (300, 300)
    >>> rows.shape
    (100, 300)
    >>> columns.shape
    (100, 300)
    >>> print(rows[0][:5], columns[0][:5])
    [False False False  True False] [False False False False False]
    """
    generator = check_random_state(random_state)

    if hasattr(n_clusters, "__len__"):
        n_row_clusters, n_col_clusters = n_clusters
    else:
        n_row_clusters = n_col_clusters = n_clusters

    # row and column clusters of approximately equal sizes
    n_rows, n_cols = shape
    row_sizes = generator.multinomial(
        n_rows, np.repeat(1.0 / n_row_clusters, n_row_clusters)
    )
    col_sizes = generator.multinomial(
        n_cols, np.repeat(1.0 / n_col_clusters, n_col_clusters)
    )

    row_labels = np.hstack(
        [np.repeat(val, rep) for val, rep in zip(range(n_row_clusters), row_sizes)]
    )
    col_labels = np.hstack(
        [np.repeat(val, rep) for val, rep in zip(range(n_col_clusters), col_sizes)]
    )

    result = np.zeros(shape, dtype=np.float64)
    for i in range(n_row_clusters):
        for j in range(n_col_clusters):
            selector = np.outer(row_labels == i, col_labels == j)
            result[selector] += generator.uniform(minval, maxval)

    if noise > 0:
        result += generator.normal(scale=noise, size=result.shape)

    if shuffle:
        result, row_idx, col_idx = _shuffle(result, random_state)
        row_labels = row_labels[row_idx]
        col_labels = col_labels[col_idx]

    rows = np.vstack(
        [
            row_labels == label
            for label in range(n_row_clusters)
            for _ in range(n_col_clusters)
        ]
    )
    cols = np.vstack(
        [
            col_labels == label
            for _ in range(n_row_clusters)
            for label in range(n_col_clusters)
        ]
    )

    return result, rows, cols
