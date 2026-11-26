data {
  int<lower=1> T;
  array[T] int<lower=0> captures;
  vector<lower=1>[T] traps_effort;
}
transformed data {
  real min_N = 1e-6;      // Minimum allowed population size
  real min_effort = 2000; // Minimum allowed effort
}
parameters {
  real<lower=70> N0;                    // Initial population size
  real<lower=5e-2, upper=1> r;          // Natural growth rate
  real<lower=1e-7, upper=1e-4> traps_q; // Catchability
}
transformed parameters {
  vector<lower=1e-6>[T] N;
  vector<lower=1e-8>[T] lambda;

  N[1] = N0;
  for (t in 1 : (T - 1)) {

    N[t + 1] = N[t] * exp(r) - captures[t];

    // If two consecutive periods have no captures and the next population
    // falls below one, with effort above the minimum, treat the population
    // as extinct.
    if (t > 1
        && captures[t - 1] < 1
        && captures[t]     < 1
        && traps_effort[t - 1] > min_effort
        && traps_effort[t]     > min_effort
        && N[t + 1] < 1) {
      N[t + 1] = min_N;
    }
    // With too little effort, zero captures do not prove absence: keep at
    // least one individual alive.
    if (traps_effort[t] <= min_effort) {
      N[t + 1] = fmax(N[t + 1] + 1, min_N + 1);
    }
    // Never let the population fall below the numerical floor.
    if (N[t + 1] < min_N) {
      N[t + 1] = min_N;
    }
  }

  for (t in 1 : T) {
    lambda[t] = traps_q * traps_effort[t] * N[t];
  }
}
model {
  // Priors
  N0 ~ lognormal(log(1e4), 1); // Tamaño inicial de la población
  r ~ normal(0.08, 0.03);      // Tasa de crecimiento natural
  traps_q ~ lognormal(log(1e-5),1);  // Capturabilidad

  for (t in 1:T) {
    if (N[t] < captures[t])
      target += negative_infinity();
  }

  // Likelihood
  captures ~ poisson(lambda);
}
generated quantities {
  int is_extinct;
  real E_critical;
  array[T] int is_progress;
  array[T] int is_progress_from_births;
  vector[T] n_birth;

  is_extinct = N[T] < 1;

  E_critical = r / traps_q;

  for (t in 1 : T) {
    is_progress[t] = traps_effort[t] > E_critical;
    n_birth[t] = N[t] * (exp(r) - 1);
    is_progress_from_births[t] = captures[t] > n_birth[t];
  }

}
