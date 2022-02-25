# Simulated Annealing implementation

This stochastic optimization method is primarily used for solving combinatorial problems,
where the total search space can be enormous (grow factorially)

In the provided example I used it to solve the travelling salesman problem, widely known in this area.
The results are quite wierd as the increase in quality (i.e., the quality of suboptimal solution) seems to be small.
By looking at the images produced by the script and playing with the parameters, e.g. temperature cooling factor and bounds, one may observe that the Hamiltonian cycle produced is not closely optimal. It is fairly possible that my implementation is incorrect or inconsistent. I noticed that selecting smaller lower temperature bound resulted into longer runs but almost no improvements in quality (the optimal solution merely did not change through last iterations). Higher upper bound, however, could result into better results.
In the end, I do not consider this method to be really useful (at least in this particular setup). It only seems to brute-force the solution but with tiny optimizations. If the solution space is not that big (try placing 6-8 cities),suboptimal soultion is found after 10-20k iterations. In a bigger task (15-50 cities), the produced solution is not nearly optimal.
