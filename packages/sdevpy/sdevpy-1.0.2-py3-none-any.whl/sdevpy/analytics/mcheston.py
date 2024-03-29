""" Monte-Carlo simulation for Heston model (vanillas). The model is defined as
    dS = sqrt(v) * S * dW
    dv = kappa * (theta - v) * dt + xi * sqrt(v) * dZ with <dW, dZ> = rho
    """
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp
# from analytics.sabr import calculate_alpha
from sdevpy.tools.timegrids import SimpleTimeGridBuilder
from sdevpy.tools import timer


def price(expiries, strikes, are_calls, fwd, parameters, num_mc=10000, points_per_year=10):
    """ Calculate vanilla prices under Heston model by Monte-Carlo simulation"""
    scale = fwd
    if scale < 0.0:
        raise ValueError("Negative forward")

    # Temporarily turn off the warnings for division by 0. This is because on certain paths,
    # the spot becomes so close to 0 that Python effectively handles it as 0. This results in
    # a warning when taking a negative power of it. However, this is not an issue as Python
    # correctly finds +infinity and since we use a floor, this case is correctly handled.
    np.seterr(divide='ignore')

    # Build time grid
    time_grid_builder = SimpleTimeGridBuilder(points_per_year=points_per_year)
    time_grid_builder.add_grid(expiries)
    time_grid = time_grid_builder.complete_grid()
    num_factors = 2

    # Find payoff times
    is_payoff = np.in1d(time_grid, expiries)

    # Retrieve parameters
    lnvol = parameters['LnVol']
    kappa = parameters['Kappa']
    theta = parameters['Theta']
    xi = parameters['Xi']
    rho = parameters['Rho']
    sqrtmrho2 = np.sqrt(1.0 - rho**2)
    v0 = calculate_v0(lnvol)

    # Draw all gaussians
    # gaussians = rand.gaussians(num_steps, num_mc, num_factors, rand_method)

    # Define dimensions
    mean = np.zeros(num_factors)
    corr = np.zeros((num_factors, num_factors))
    for c in range(num_factors):
        corr[c, c] = 1.0

    # Draw for each step
    seed = 42
    rng = np.random.RandomState(seed)

    # Initialize paths
    spot = np.ones((2 * num_mc, 1)) * fwd
    vol2 = np.ones((2 * num_mc, 1)) * v0

    # Loop over time grid
    ts = te = 0
    payoff_count = 0
    mc_prices = []
    for i, t in enumerate(time_grid):
        ts = te
        te = t
        dt = te - ts
        sqrt_dt = np.sqrt(dt)

        # Evolve
        dz = rng.multivariate_normal(mean, corr, size=num_mc) * sqrt_dt
        dz = np.concatenate((dz, -dz), axis=0) # Antithetic paths
        dz0 = dz[:, 0].reshape(-1, 1)
        dz1 = dz[:, 1].reshape(-1, 1)

        # Evolve vol
        vol2s = np.abs(vol2)
        sqrt_vol2s = np.sqrt(vol2s)
        vol2e = vol2s + kappa * (theta - vol2s) * dt + xi * sqrt_vol2s * dz1
        vol2e = np.abs(vol2e)
        vol2 = vol2e

        # Evolve spot
        intvol2 = 0.5 * (vol2s + vol2e) * dt
        ito = 0.5 * intvol2
        dw = rho * dz1 + sqrtmrho2 * dz0
        spot *= np.exp(-ito + sqrt_vol2s * dw)

        # Calculate payoff
        if is_payoff[i]:
            w = [1.0 if is_call else -1.0 for is_call in are_calls[payoff_count]]
            w = np.asarray(w).reshape(1, -1)
            k = np.asarray(strikes[payoff_count]).reshape(1, -1)
            payoff = np.maximum(w * (spot - k), 0.0)
            rpayoff = np.mean(payoff, axis=0)
            mc_prices.append(rpayoff)
            payoff_count += 1

    np.seterr(divide='warn')

    return np.asarray(mc_prices)

def calculate_v0(lnvol):
    """ Calculate approximated v0 parameter from lognormal vol (for order of magnitude
        only)"""
    return lnvol**2


if __name__ == "__main__":
    EXPIRIES = [0.5, 1.0, 5.0, 10.0]
    NSTRIKES = 50
    FWD = -0.005
    SHIFT = 0.03
    SFWD = FWD + SHIFT
    IS_CALL = False
    ARE_CALLS = [IS_CALL] * NSTRIKES
    ARE_CALLS = [ARE_CALLS] * len(EXPIRIES)
    LNVOL = 0.25
    # Spread method
    # SPREADS = np.linspace(-200, 200, NSTRIKES)
    # SPREADS = np.asarray([SPREADS] * len(EXPIRIES))
    # STRIKES = FWD + SPREADS / 10000.0
    # SSTRIKES = STRIKES + SHIFT
    # XAXIS = SPREADS
    # Distribution method
    np_expiries = np.asarray(EXPIRIES).reshape(-1, 1)
    PERCENT = np.linspace(0.01, 0.99, NSTRIKES)
    PERCENT = np.asarray([PERCENT] * len(EXPIRIES))
    ITO = -0.5 * LNVOL**2 * np_expiries
    DIFF = LNVOL * np.sqrt(np_expiries) * sp.norm.ppf(PERCENT)
    SSTRIKES = SFWD * np.exp(ITO + DIFF)
    STRIKES = SSTRIKES - SHIFT
    XAXIS = STRIKES

    THETA = LNVOL**2
    PARAMETERS = {'LnVol': LNVOL, 'Kappa': 1.0, 'Theta': THETA, 'Xi': 0.50, 'Rho': -0.25}
    NUM_MC = 100 * 1000
    POINTS_PER_YEAR = 25
    # SCHEME = 'LogAndersen'
    # SCHEME = 'LogEuler'

    # Calculate MC prices
    mc_timer = timer.Stopwatch("MC")
    mc_timer.trigger()
    MC_PRICES = price(EXPIRIES, SSTRIKES, ARE_CALLS, SFWD, PARAMETERS, NUM_MC, POINTS_PER_YEAR)
    mc_timer.stop()
    mc_timer.print()

    # Convert to IV and compare against approximate closed-form
    import black
    import bachelier
    mc_ivs = []
    n_ivs = []
    for a, expiry in enumerate(EXPIRIES):
        mc_iv = []
        cf_iv = []
        n_iv = []
        for j, sstrike in enumerate(SSTRIKES[a]):
            mc_iv.append(black.implied_vol(expiry, sstrike, IS_CALL, SFWD, MC_PRICES[a, j]))
            n_iv.append(bachelier.implied_vol_solve(expiry, STRIKES[a, j], IS_CALL, FWD,
                                                    MC_PRICES[a, j]))
        mc_ivs.append(mc_iv)
        n_ivs.append(n_iv)

    plt.figure(figsize=(10, 8))
    plt.subplots_adjust(hspace=0.40)
    plt.subplot(2, 2, 1)
    plt.plot(XAXIS[0], mc_ivs[0], label='MC')
    plt.legend(loc='best')
    plt.title(f"Expiry: {EXPIRIES[0]}")
    plt.subplot(2, 2, 2)
    plt.plot(XAXIS[1], mc_ivs[1], label='MC')
    plt.legend(loc='best')
    plt.title(f"Expiry: {EXPIRIES[1]}")
    plt.subplot(2, 2, 3)
    plt.plot(XAXIS[2], mc_ivs[2], label='MC')
    plt.legend(loc='best')
    plt.title(f"Expiry: {EXPIRIES[2]}")
    plt.subplot(2, 2, 4)
    plt.plot(XAXIS[3], mc_ivs[3], label='MC')
    plt.legend(loc='best')
    plt.title(f"Expiry: {EXPIRIES[3]}")

    plt.show()

    # plt.figure(figsize=(10, 8))
    # plt.subplots_adjust(hspace=0.40)
    # plt.subplot(2, 2, 1)
    # plt.plot(XAXIS[0], n_ivs[0], label='MC')
    # plt.legend(loc='best')
    # plt.title(f"NVOL Expiry: {EXPIRIES[0]}")
    # plt.subplot(2, 2, 2)
    # plt.plot(XAXIS[1], n_ivs[1], label='MC')
    # plt.legend(loc='best')
    # plt.title(f"NVOL Expiry: {EXPIRIES[1]}")
    # plt.subplot(2, 2, 3)
    # plt.plot(XAXIS[2], n_ivs[2], label='MC')
    # plt.legend(loc='best')
    # plt.title(f"NVOL Expiry: {EXPIRIES[2]}")
    # plt.subplot(2, 2, 4)
    # plt.plot(XAXIS[3], n_ivs[3], label='MC')
    # plt.legend(loc='best')
    # plt.title(f"NVOL Expiry: {EXPIRIES[3]}")

    # plt.show()
