import subprocess


def build_model(stan_file):
    stan_basename = stan_file.split(".")[0]
    try:
        result = subprocess.run(
            ["make", stan_basename],
            cwd="/opt/cmdstan",
        )
        return result.returncode
    except result.CalledProcessError as e:
        return e.returncode
