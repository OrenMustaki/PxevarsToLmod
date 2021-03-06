#!/usr/bin/env python3
#
# Project : IntelPsxevarsToLmod
#
import os
import sys
import subprocess as sp
from files import Files
import argparse

# exclude the following from the created lua files
exclude_names = ["PS1", "INTEL_PYTHONHOME", "CONDA_PYTHON_EXE", "CONDA_SHLVL", "CONDA_PROMPT_MODIFIER", "CONDA_EXE", "CONDA_PREFIX", "CONDA_DEFAULT_ENV"]
exclude_values = ["/usr/local/bin", "/usr/bin", "/usr/local/man", "/usr/local/share/man", "/usr/share/man", ""]
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=f"")
parser.add_argument(dest='path', action='store')
a = parser.parse_args()

arch = 'intel64'
lua_module = ''
intel_license_line = ''
f = Files()

gcc = f.files['gcc']
env = f.files['env']

if not os.path.isdir(a.path):
    print(f"\n{a.path} is not a directory.\n")
    exit()

vars_script = f.find("psxevars.sh", a.path)

if not vars_script:
    print("Could not find psxevars.sh")
    exit()

psxe_version = os.path.basename(os.path.dirname(vars_script))

if os.getenv('INTEL_LICENSE_FILE', False):
    intel_license_line = f"setenv(\"INTEL_LICENSE_FILE\",\"{os.getenv('INTEL_LICENSE_FILE')}\")"

env_cmd = f'{env} -i bash -f -c \'export PATH={os.path.dirname(gcc)}:$PATH;source {vars_script} {arch};{env}\''
show_env = sp.getoutput(env_cmd)
clean_env_cmd = f'env -i bash -f -c env'
clean_env = sp.getoutput(clean_env_cmd).splitlines()

vars = {}
for line in show_env.splitlines():
    if "=" not in line:
        #print(f"Skipping line : \"{line}\"")
        continue
    if line in clean_env:
        continue
    var = line.split("=")[0]
    values = "".join(line.split("=")[1:])

    vars[var] = [ v for v in values.split(":") ] 
for var, values in vars.items():
    for value in values:
        if var in exclude_names or value in exclude_values:
            continue
        if 
        lua_module += f"prepend_path(\"{var}\",\"{value}\")\n"

lua_module = f"""-- -*- lua module file for {psxe_version} --

help([[Ensures that you have the path to {psxe_version} in your path]])

family("intel_compiler")

whatis("{psxe_version}")
{lua_module}
{intel_license_line}
load("gcc")

setenv("CC","icc")
setenv("CXX","icpc")
setenv("FC","ifort")
setenv("F90","ifort")
setenv("F77","ifort")
setenv("libs","/home/odd/lib/x86_64/ifort")

"""
print(lua_module)
