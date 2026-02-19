import subprocess


def build_model(stan_file):
    stan_basename = stan_file.split(".")[0]
    try:
        result = subprocess.run(
            ["make", f"/workdir/{stan_basename}"],
            cwd="/opt/cmdstan",
        )
        return result.returncode
    except result.CalledProcessError:
        return "Not compiled"
