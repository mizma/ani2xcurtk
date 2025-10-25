ani2xcurtk
========================================================================

THIS IS CURRENTLY A WORK IN PROGRESS.

*Installation and usage will not currently work.*

`.ani` to `Xcursor` conversion toolkit.  This toolkit helps convert a
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

### External Prerequisites

Following cli tools will need to be accessible in the environment.

* `win2xcur`
  * Used to convert `.cur` and `.ani` to `Xcursor` cursor file
* `xcur2png`
  * Used to extract `.png` image files from `Xcursor` cursor files
* `ImageMagick`
  * Used to create different cursor sizes
* `xcursorgen`
  * Used to re-package the extracted and up-converted `.png` files
    back to `Xcursor` cursor files

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

Package the `.png` files into `Xcursor` theme.

`pack` will create different sizes of the image files using `ImageMagick` and
map the typical Windows cursor package files to relevant `Xcursor` themes.

Requires `Xcursorgen` and `ImageMagick` to be installed and accessible in PATH

~~~shell
> a2xc getpng [OPTIONS] TARGET
~~~

* TARGET
  * directory containg directories with `Xcursor` input png and config files
* -o, --output PATH
  * output directory path to place the `Xcursor` theme
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
  * output directory path to place the `Xcursor` theme
* -c, --config CFG
  * CFG: Path to Configuration File (default: ani2xcurtk.yml)
* -v, --verbose
  * verbosity

### Configuration file

YAML based configuration file (default file name: ani2xcurtk.yaml)
is used to store default settings for the tool.
The command line options will take precedence over the configuration parameters.

#### Parameters

* `sizes` key
  * Extra cursor sizes (in pixels) to generate as an array.
* `mappings` key
  * Array of keys with the Windows cursor filename.
  * Each Windows cursor filename key has an array of `Xcursor` cursor
    file name associated to the Windows version.
    * The cursor generated from this `.cur/.ani` will be copied
      to the first element in the array, and the rest will become
      symbolic links to the first element.
    * If no mappings are available, keys can be omitted or use `null`
      to clarify that there is no current mapping.
  * Mappings are processed in the order it is defined.
    Any mapping appearing later will overwrite previous mappings.
    * This is to allow manually edited images to overwrite existing
      non-ideal mappings.
    * Make sure you do not override the top mapping for each file,
      Since the top file is the file copied over and all other mappings
      link to this

#### Example config

Following shows the default settings of the configuration

~~~yaml
sizes:
  - 40
  - 48
  - 56
  - 64
mapping:
  - "01-normal":
    - "arrow"
    - "default"
    - "left_ptr"
    - "top_left_arrow"
  - "02-link":
    - "alias"
    - "dnd-link"
    - "hand"
    - "hand1"
    - "hand2"
    - "link"
    - "openhand"
    - "pointer"
    - "pointing_hand"
    - "3085a0e285430894940527032f8b26df"
    - "640fb0e74195791501fd1ed57b41487f"
    - "9d800788f1b08800ae810202380a0822"
    - "a2a266d0498c3104214a47bd64ab0fc8"
    - "b66166c04f8c3109214a4fbd64a50fc8"
    - "e29285e634086352946a0e7090d73106"
  - "03-loading":
    - "half-busy"
    - "left_ptr_watch"
    - "progress"
    - "wait"
    - "watch"
    - "00000000000000020006000e7e9ffc3f"
    - "08e8e1c95fe2fc01f976f1e063a24ccd"
    - "3ecb610c1bf2410f44200f48c40d3599"
  - "04-help":
    - "dnd-ask"
    - "help"
    - "left_ptr_help"
    - "question_arrow"
    - "whats_this"
    - "5c6cd98b3f3ebcb1f9c7f1c204630408"
    - "d9ce0ab605698f320427677b458ad60b"
  - "05-text select":
    - "ibeam"
    - "text"
    - "xterm"
    - "vertical-text"
  - "06-handwriting":
    - "draft"
    - "pencil"
  - "07-precision":
    - "cell"
    - "color-picker"
    - "cross_reverse"
    - "cross"
    - "crosshair"
    - "diamond_cross"
    - "plus"
    - "size_all"
    - "tcross"
  - "08-unavailable":
    - "circle"
    - "crossed_circle"
    - "dnd-no-drop"
    - "forbidden"
    - "not-allowed"
    - "no-drop"
    - "pirate"
    - "03b6e0fcb3499374a867c041f52298f0"
  - "09-Location Select": null
  - "10-Person Select": null
  - "11-Vertical Resize":
    - "v_double_arrow"
    - "bottom_side"
    - "top_side"
    - "up-arrow"
    - "down-arrow"
    - "n-resize"
    - "ns-resize"
    - "row-resize"
    - "s-resize"
    - "sb_v_double_arrow"
    - "size_ver"
    - "split_v"
    - "sb_down_arrow"
    - "sb_up_arrow"
    - "00008160000006810000408080010102"
    - "2870a09082c103050810ffdffffe0204"
  - "12-Horizontal Resize":
    - "col-resize"
    - "e-resize"
    - "ew-resize"
    - "h_double_arrow"
    - "left_side"
    - "left-arrow"
    - "right_side"
    - "right-arrow"
    - "sb_right_arrow"
    - "sb_left_arrow"
    - "sb_h_double_arrow"
    - "size_hor"
    - "split_h"
    - "w-resize"
    - "14fef782d02440884392942c11205230"
    - "028006030e0e7ebffc7f7070c0600140"
  - "13-Diagonal Resize 1":
    - "bd_double_arrow"
    - "bottom_right_corner"
    - "lr_angle"
    - "nw-resize"
    - "nwse-resize"
    - "se-resize"
    - "size_fdiag"
    - "top_left_corner"
    - "ul_angle"
    - "c7088f0f3e6c8088236ef8e1e3e70000"
  - "14-Diagonal Resize 2":
    - "fd_double_arrow"
    - "bottom_left_corner"
    - "ll_angle"
    - "ne-resize"
    - "nesw-resize"
    - "size_bdiag"
    - "sw-resize"
    - "top_right_corner"
    - "ur_angle"
    - "fcf1c3c7cd4491d801f1e1c78f100000"
  - "15-Move":
    - "all-scroll"
    - "closedhand"
    - "dnd-move"
    - "dnd-none"
    - "fleur"
    - "grab"
    - "grabbing"
    - "move"
    - "4498f0e0c1937ffe01fd06f973665830"
    - "9081237383d90e509aa00f00170e968f"
  - "16-Alternate Select":
    - "center_ptr"
    - "right_ptr"
    - "draft_large"
    - "draft_small"
  # Following are for manual edit of existing images.
  # These will overwrite existing ones above.
  - "01-normal-mirrored":
    - "right_ptr"
    - "draft_large"
    - "draft_small"
  - "11-Vertical Resize-top":
    - "top_side"
    - "up-arrow"
    - "n-resize"
    - "sb_up_arrow"
  - "11-Vertical Resize-bottom":
    - "bottom_side"
    - "down-arrow"
    - "s-resize"
    - "sb_down_arrow"
  - "12-Horizontal Resize-left":
    - "left_side"
    - "left-arrow"
    - "sb_left_arrow"
    - "w-resize"
  - "12-Horizontal Resize-right":
    - "right_side"
    - "right-arrow"
    - "sb_right_arrow"
    - "e-resize"
  - "13-Diagonal Resize 1-top":
    - "top_left_corner"
    - "nw-resize"
    - "ul_angle"
  - "13-Diagonal Resize 1-bottom":
    - "bottom_right_corner"
    - "se-resize"
    - "lr_angle"
  - "14-Diagonal Resize 2-top":
    - "top_right_corner"
    - "ne-resize"
    - "ur_angle"
  - "14-Diagonal Resize 2-bottom":
    - "bottom_left_corner"
    - "sw-resize"
    - "ll_angle"
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

Acknowledgement
------------------------------------------------------------------------

* [win2xcur-batch](https://github.com/khayalhus/win2xcur-batch)
  * Base inspiration for the tool.  Initial mapping are based on their [map.json](https://github.com/khayalhus/win2xcur-batch/blob/main/map.json)
