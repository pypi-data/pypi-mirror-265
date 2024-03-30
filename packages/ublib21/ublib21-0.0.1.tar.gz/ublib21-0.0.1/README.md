# UBLib21

## Usage

~~~ python
# ToDo: Implement usage
~~~

## Extra (for developers)
### Development

1. Clone this repo
~~~ shell
git clone https://github.com/EverGrowRN/ublib21.git
~~~
2. Create a virtual environment with Python 3.10 or above.
~~~ shell
virtualenv venv --python=3.10
~~~ 
3. Activate environment
~~~ shell
# Linux
source ./venv/bin/activate

# Windows (i.e. using PowerShell)
./venv/Scripts/activate.ps1
~~~
4. Install requirements
~~~ shell
pip install -r requirements
~~~


### Testing
1. Install the package as development. Run on the project root directory the following
~~~ shell
pip install .[dev]
~~~
2. Install pytest
~~~ shell
pip install pytest
~~~
3. Run tests. Run on the project root directory the following
~~~ shell
pytest
~~~

### Deploy python package

https://packaging.python.org/en/latest/tutorials/packaging-projects/

#### To build:
~~~ shell
py -m build
~~~

#### To push package (test):
Replace **username** with yours. Replace **token_filename** with path to your file that contains the pypi project test server token.
~~~ shell
py -m twine upload --repository testpypi dist/* -u <username> -p $(cat <token_filename>)
~~~