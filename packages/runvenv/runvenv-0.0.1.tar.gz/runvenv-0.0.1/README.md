# 1. One line description

A tool to run a python script inside a virtual environment with a list of
preinstalled modules, creating it first in case it already does not exist.

For more details, once installed, run this:

    $ python -m runvenv --help


# 2. Information for users

# 2.1. Short version

If you want to run script "my_script.py" which needs all the modules listed in
file "requirements.txt", just do this:

    $ python -m runvenv --reqs requirements.txt my_script.py

# 2.2. Long version

When you download a python script it typically comes with a file called
"requirements.txt" that contains a list of modules (and their versions) that
need to be installed in order for the script to work.

    NOTE: Other versions of those same packages might also work, but the
    versions included in "requirements.txt" is what the developer tested with.

What you would need to do next is to create a new empty virtual environment,
install those packages specific versions inside of it and finally run the
script, like this:

    $ python -m venv .venv
    $ source .venv/bin/activate
    $ python -m pip install -r requirements.txt
    $ python my_script.py

This works but has two inconvenients:

    1. You need to remember where the virtual environment was installed and to
       run "source .venv/bin/activate" in the future if you want to run the
       script again after having deactivated the virtual environment.

    2. If you download a new version of the script you need to remember to
       check whether the contents of "requirements.txt" have changed and, if so,
       delete the old virtual environment and create and activate the new one.

Both issues can be overcome by using "runvenv". Just run this every time you
want to run the script:

    $ python -m runvenv --reqs requirements.txt my_script.py

This will automatically...

    1. Obtain a hash of the contents of "requirements.txt"

    2. If a previously generated virtual environment associated to that hash
       exists in the current PC, use it. Otherwise use "pip" to install and save
       it for the future.

    3. Enable the virtual environment.

    4. Run the script.

    5. Deactivate the virtual environment.

Thanks to the "hash" trick, even if "requirements.txt" changes you don't need to
do anything special... just run the same command every single time and it will
take care of everything under the hood.


# 3. Information for developers

Let's say you are working on a script that depends on modules "toml" and
"bzip3", so you do this:

    $ python -m venv .venv
    $ source .venv/bin/activate
    $ python -m pip install toml bzip3

...and then keep developing your script inside the just created virtual
environment.

You know that the particular version of the toml and bzip3 modules that have
been installed (ie. the ones you have been using while you were working on the
script) work fine, so you decide to take note of the specific versions by
running this script:

    $ python -m pip freeze > requirements.txt

...which generates a file such as this one:

    $ cat requirements.txt
    bzip3==0.1.5
    cffi==1.16.0
    pycparser==2.22
    toml==0.10.2

Notice that this list includes other packages in adition to "toml" and "bzip3".
This is because in order to install those two other dependencies had to be
pulled in too.

Anyway... you could have run these commands instead to obtain the same result:

   $ echo toml   > non-frozen.txt
   $ echo bzip3 >> non-frozen.txt
   $ python -m runvenv --freeze non-frozen.txt

...which is not much shorter than the standard way, but I had to include this
functionality in the script for completeness :)


# 4. Information for hackers

In order to crontribute to this project, please run this command and make sure
there are not errors before sending your patch:

    $ ruff check .


# 5. Information for packagers (that's me so that I don't forget :P)

The source code in this repository is meant to be distributed as a python
package that can be "pip install"ed.

Once you are ready to make a release:

  1. Increase the "version" number in file "pyproject.toml"
  2. Run the next command:

       $ python -m pip install --upgrade build
       $ python -m build

  3. Publish the contents of the "dist" folder to a remote package repository
     such as PyPi (see
     [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/))

  4. Tell your users that a new version is available and that they can install
     it by running this command:

       $ python -m pip install runvenv

NOTE: If "python -m build" returns an error, you probably have to install the
"python-build" package first, either using your package manager (preferred) or
inside a virtual environment. If you choose the latter, make sure you use the
"--copies" flag when creating the virtual environment or else you will later get
errors about symbolic links when creating the package:

    $ python -m venv --copies .my_venv 


