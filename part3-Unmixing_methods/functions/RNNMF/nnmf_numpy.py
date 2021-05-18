import numpy as np
from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF
from sklearn.decomposition.nmf import _initialize_nmf

def test_py(a, b):
    print(a+b)
    return a+b

def robust_NMF(data, basis_input, rank, beta, init, reg_val, sum_to_one, tol, max_iter=1000,print_every=10, user_prov=None):

    eps = 2.3e-16
    basis, coeff, outlier = initialize_rnmf(data, rank, init, beta,sum_to_one, user_prov)

    basis = basis_input
    data_approx = basis@coeff + outlier + eps
    fit = np.zeros(max_iter+1)
    obj = np.zeros(max_iter+1)

    fit[0] = beta_divergence(data, data_approx, beta)
    obj[0] = fit[0] + reg_val*np.sum(np.sqrt(np.sum(outlier**2, axis=0)))

    print('Iter = 0; Obj = {}'.format(obj[0]))

    for iter in range(max_iter):
        outlier = update_outlier(data, data_approx, outlier, beta, reg_val)
        data_approx = basis@coeff + outlier + eps

        coeff = update_coeff(data, data_approx, beta, basis, coeff, sum_to_one)
        data_approx = basis@coeff + outlier + eps

        basis = update_basis(data, data_approx, beta, basis, coeff)
        data_approx = basis@coeff + outlier + eps

        fit[iter+1] = beta_divergence(data, data_approx, beta)
        obj[iter+1] = fit[iter+1] +reg_val*np.sum(np.sqrt(np.sum(outlier**2, axis=0)))

        if iter % print_every == 0:
            print('Iter = {}; Obj = {}; Err = {}'.format(iter+1, obj[iter+1],
                  np.abs((obj[iter]-obj[iter+1])/obj[iter])))

        if np.abs((obj[iter]-obj[iter+1])/obj[iter]) <= tol:
            print('Algorithm converged as per defined tolerance')
            break

        if iter == (max_iter - 1):
            print('Maximum number of iterations achieved')

    obj = obj[:iter]
    fit = fit[:iter]

    return basis, coeff, outlier, obj


def initialize_rnmf(data, rank, alg, beta=2, sum_to_one=0, user_prov=None):

    eps = 2.3e-16

    outlier = np.random.rand(data.shape[0], data.shape[1])

    if alg == 'random':
        print('Initializing rNMF uniformly at random.')
        basis = np.random.rand(data.shape[0], rank)
        coeff = np.random.rand(rank, data.shape[1])

        # Rescale coefficients if they will have a simplex constraint later:
        if sum_to_one == 1:
            coeff = normalize(coeff, norm='l1', axis=0)

        return basis+eps, coeff+eps, outlier+eps

    elif alg == 'bNMF':

        print('Initializing rNMF with beta-NMF.')
        model = NMF(n_components=rank, init='nndsvdar', beta_loss=beta,
                    solver='mu', verbose=True)
        basis = model.fit_transform(data)
        coeff = model.components_

        # Rescale coefficients if they will have a simplex constraint later:
        if sum_to_one == 1:
            coeff = normalize(coeff, norm='l1', axis=0)

        return basis+eps, coeff+eps, outlier+eps

    elif alg == 'NMF':
        print('Initializing rNMF with NMF.')
        model = NMF(n_components=rank, init='nndsvdar', verbose=False)
        basis = model.fit_transform(data)
        coeff = model.components_

        if sum_to_one == 1:
            coeff = normalize(coeff, norm='l1', axis=0)

        return basis+eps, coeff+eps, outlier+eps

    elif alg == 'nndsvdar':
        print('Initializing rNMF with nndsvdar.')
        basis, coeff = _initialize_nmf(data,n_components=rank,init='nndsvdar')

        if sum_to_one == 1:
            coeff = normalize(coeff, norm='l1', axis=0)

        return basis+eps, coeff+eps, outlier+eps

    elif alg == 'user':
        print('Initializing rNMF with user provided values.')

        if user_prov is None:
            raise ValueError('You forgot the dictionary with the data')

        elif type(user_prov) is not dict:
            raise ValueError('Initializations must be in a dictionary')

        elif ('basis' not in user_prov or 'coeff' not in user_prov or
              'outlier' not in user_prov):
            raise ValueError('Wrong format for initialization dictionary')

        return user_prov['basis'], user_prov['coeff'], user_prov['outlier']

    else:
        raise ValueError('Invalid algorithm (typo?): got %r instead of one of %r' %
            (alg, ('random', 'NMF', 'bNMF', 'nndsvdar', 'user')))


def beta_divergence(mat1, mat2, beta):

    eps = 2.3e-16

    vec = lambda X: X.flatten()

    if beta == 2:
        beta_div = 0.5*(np.linalg.norm(mat1 - mat2, ord='fro')**2)

    elif beta == 1:
        idx_zeros = np.flatnonzero(mat1 <= eps)
        idx_interest = np.ones(mat1.size, dtype=bool)
        idx_interest[idx_zeros] = False

        nonzero = lambda X: X.flatten()[idx_interest]
        zero = lambda X: X.flatten()[idx_zeros]

        beta_div = np.sum((nonzero(mat1) * np.log(nonzero(mat1)/nonzero(mat2)))- nonzero(mat1) + nonzero(mat2)) + np.sum(zero(mat2))

    elif beta == 0:
        beta_div = np.sum(vec(mat1)/vec(mat2) - np.log(vec(mat1)/vec(mat2))) -len(vec(mat1))

    else:
        beta_div = np.sum(vec(mat1)**beta + (beta-1)*vec(mat2)**beta
                          - beta*vec(mat1)*(vec(mat2))**(beta-1))/(beta*(beta-1))

    return beta_div


def update_basis(data, data_approx, beta, basis, coeff):

    return basis * ((data*(data_approx**(beta-2))@coeff.T) /
                    ((data_approx**(beta-1))@coeff.T))


def update_coeff(data, data_approx, beta, basis, coeff, sum_to_one):
    bet1 = lambda X: X**(beta-1)
    bet2 = lambda X: X**(beta-2)

    if sum_to_one == 1:

        Gn = ((basis.T)@(data*bet2(data_approx)) +
              np.sum((basis@coeff)*bet1(data_approx), axis=0))
        Gp = ((basis.T)@bet1(data_approx) +
              np.sum((basis@coeff)*data*bet2(data_approx), axis=0))
        coeff = coeff*(Gn/Gp)

        return normalize(coeff, norm='l1', axis=0)

    elif sum_to_one == 0:
        return coeff * (((basis.T)@(data*bet2(data_approx))) /
                        ((basis.T)@bet1(data_approx)))


def update_outlier(data, data_approx, outlier, beta, reg_val):

    eps = 2.3e-16

    bet1 = lambda X: X**(beta-1)
    bet2 = lambda X: X**(beta-2)

    l2n = lambda X: (X /
                     (np.sum(np.abs(X)**2, axis=0)**(0.5)
                      + eps).T[np.newaxis, :])

    return outlier * ((data*bet2(data_approx)) / (bet1(data_approx) +
                                                  reg_val*l2n(outlier)))

