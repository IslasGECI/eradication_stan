data {
  int<lower=1> T;
  array[T] int<lower=0> captures;
  array[T] int<lower=0> detections;
  vector<lower=1>[T] traps_effort;
  vector<lower=1>[T] cameras_effort;
}
parameters {
  real<lower=70> N0;              // Initial population size
  real<lower=5e-2, upper=1> r;    // Natural growth rate
  real<lower=1e-7, upper=1e-4> traps_q; // Traps capturability
  real<lower=1e-7, upper=1e-4> cameras_q; // Cameras detectability
}
transformed parameters {
  vector<lower=1e-6>[T] N;
  vector<lower=1e-8>[T] traps_lambda;
  vector<lower=1e-8>[T] cameras_lambda;

  N[1] = N0;
  for (t in 1 : (T - 1)) {
    N[t + 1] = fmax(1e-6, N[t] * exp(r) - captures[t]);
  }

  for (t in 1 : T) {
    traps_lambda[t] = traps_q * traps_effort[t] * N[t];
    cameras_lambda[t] = cameras_q * cameras_effort[t] * N[t];
  }
}
model {
  // Priors
  N0 ~ lognormal(log(1e4), 1); // Initial population size prior
  r ~ normal(0.08, 0.03);      // Natural growth rate prior
  traps_q ~ lognormal(log(1e-5),1);  // Traps capturability prior
  cameras_q ~ lognormal(log(1e-5),1);  // Cameras detectability prior

  for (t in 1:T) {
    if (N[t] < captures[t])
      target += negative_infinity();
  }

  // Likelihood
  captures ~ poisson(traps_lambda);
  detections ~ poisson(cameras_lambda);
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
