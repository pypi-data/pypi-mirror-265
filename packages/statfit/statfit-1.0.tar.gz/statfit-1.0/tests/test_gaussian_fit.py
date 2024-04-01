from statfit import gaussian_fit 
import numpy as np
import math

testing_sigma = 0.3

data_1_noRandom_even = gaussian_fit.gaussian_fit(sigma=testing_sigma, numOfParameters=4, mean_width=0.1, rand=False)

data_2_Random_even = gaussian_fit.gaussian_fit(sigma=testing_sigma, numOfParameters=4, mean_width=0.1, rand=True)

data_3_noRandom_odd = gaussian_fit.gaussian_fit(sigma=testing_sigma, numOfParameters=5, mean_width=0.1, rand=False)

data_4_Random_odd = gaussian_fit.gaussian_fit(sigma=testing_sigma, numOfParameters=5, mean_width=0.1, rand=True)

# assert(np.std(data_1_noRandom_even) == testing_sigma)  # PASSED

print(np.std(data_1_noRandom_even))

print(np.mean(data_1_noRandom_even))

# assert(np.std(data_2_Random_even) == testing_sigma) # PASSED

print(np.std(data_2_Random_even))

print(np.mean(data_2_Random_even))

# assert(np.std(data_3_noRandom_odd) == testing_sigma) # PASSED

print(np.std(data_3_noRandom_odd))

print(np.mean(data_3_noRandom_odd))

# assert(np.std(data_4_Random_odd) == testing_sigma)

print(np.std(data_4_Random_odd))

print(np.mean(data_4_Random_odd))







