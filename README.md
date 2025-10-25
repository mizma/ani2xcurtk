ani2xcurtk
========================================================================

THIS IS CURRENTLY A WORK IN PROGRESS.

*Installation and usage will not currently work.*

`.ani` to `xcursor` conversion toolkit.  This toolkit helps convert a
typical Windows cursor themes using `.cur` or `.ani` files with specific
file naming convention to map to a typical `Xcursor` theme and create
the cursor theme package.

This tool provides subcommands to split certain stages of the conversion
process for users to be able to intervene in key steps like making
alternate images of a cursor to be used in cursor types not typically
available in a Windows cursor theme pack.

Installation
------------------------------------------------------------------------

~~~shell
> pip install ani2xcurtk
~~~

Usage
------------------------------------------------------------------------

### getpng

extract `.cur` or `.ani` files to `.png` files.

Requires `win2xcur` and `xcur2png` to be installed and accessible in PATH

~~~shell
> a2xc getpng [OPTIONS] TARGET
~~~

* TARGET
  * directory containing a standard windows cursor theme pack
* -o, --output PATH
  * output directory path to place all converted files
* -c, --config CFG
  * CFG: Path to Configuration File (default: ani2xcurtk.yml)
* -v, --verbose
  * verbosity

### pack

Package the `.png` files into `xcursor` theme.

`pack` will create different sizes of the image files using `ImageMagic` and
map the typical Windows cursor package files to relevant Xcursor themes.

Requires `xcursorgen` and `ImageMagic` to be installed and accessible in PATH

~~~shell
> a2xc getpng [OPTIONS] TARGET
~~~

* TARGET
  * directory containg directories with xcursor input png and config files
* -o, --output PATH
  * output directory path to place the xcursor theme
* -c, --config CFG
  * CFG: Path to Configuration File (default: ani2xcurtk.yml)
* -v, --verbose
  * verbosity

### conv

Chains getpng and pack in one command

~~~shell
> a2xc conv [OPTIONS] TARGET
~~~

* TARGET
  * directory containg a standard windows cursor theme pack
* -o, --output PATH
  * output directory path to place the xcursor theme
* -c, --config CFG
  * CFG: Path to Configuration File (default: ani2xcurtk.yml)
* -v, --verbose
  * verbosity

### Configuration file

YAML based configuration file (default file name: ani2xcurtk.yaml)
is used to store default settings for the tool.
The command line options will take precedence over the configuration parameters.

following shows the default settings of the configuration

~~~yaml
option1: option1param
option2: option2param
optionArray:
  - item1
  - item2
optionDict:
  key1: item1
  key2: item2
  key3: item3
~~~

Known Issues
------------------------------------------------------------------------

Need to be implemented.

Development
------------------------------------------------------------------------

### Versioning

The project will follow the [semver2.0](http://semver.org/) versioning scheme.
With initial development phase starting at 0.1.0 and increasing
minor/patch versions until we deploy the tool to production
(and reach 1.0.0).
The interface relevant to versioning is whatever defined in this
document's "Usage" section (includes all (sub)commands, their cli arguments,
and the format of the configuration file "ani2xcurtk.yaml").

