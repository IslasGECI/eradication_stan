data {
  int<lower=1> T;
  array[T] int<lower=0> capturas;
  vector<lower=1>[T] esfuerzo;
}
parameters {
  real<lower=70> N0;              // Tamaño inicial de la población
  real<lower=5e-2, upper=1> r;    // Tasa de crecimieno natural
  real<lower=1e-7, upper=1e-4> q; // Capturabilidad
}
transformed parameters {
  vector<lower=1e-6>[T] N;
  vector<lower=1e-8>[T] lambda;

  N[1] = N0;
  for (t in 1 : (T - 1)) {
    N[t + 1] = fmax(1e-6, N[t] * exp(r) - capturas[t]);
  }

  for (t in 1 : T) {
    lambda[t] = q * esfuerzo[t] * N[t];
  }
}
model {
  // Priors
  N0 ~ lognormal(log(1e4), 1); // Tamaño inicial de la población
  r ~ normal(0.08, 0.03);      // Tasa de crecimiento natural
  q ~ lognormal(log(1e-5),1);  // Capturabilidad

  for (t in 1:T) {
    if (N[t] < capturas[t])
      target += negative_infinity();
  }

  // Likelihood
  capturas ~ poisson(lambda);
}
generated quantities {
  int is_extinct;
  real E_critical;
  vector[T] int is_progress;
  vector[T] int is_progress_from_births;
  vector[T] int n_birth;

  is_extinct = N[T] < 1;

  E_critical = r / q;

  for (t in 1 : T) {
    is_progress[t] = esfuerzo[t] > E_critical;
    n_birth[t] = N[t] * (exp(r) - 1);
    is_progress_from_births[t] = capturas[t] > n_birth[t];
  }

}
