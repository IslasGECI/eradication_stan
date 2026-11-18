data {
  int<lower=1> T;
  array[T] int<lower=0> captures;
  vector<lower=1>[T] traps_effort;
}
parameters {
  real<lower=70> N0;              // Tamaño inicial de la población
  real<lower=5e-2, upper=1> r;    // Tasa de crecimieno natural
  real<lower=1e-7, upper=1e-4> traps_q; // Capturabilidad
}
transformed parameters {
  vector<lower=1e-6>[T] N;
  vector<lower=1e-8>[T] lambda;

  N[1] = N0;
  for (t in 1 : (T - 1)) {
    N[t + 1] = fmax(1e-6, N[t] * exp(r) - captures[t]);
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
generated traps_quantities {
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
