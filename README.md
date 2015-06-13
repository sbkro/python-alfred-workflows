# python-alfred-workflow
[![Build Status](https://travis-ci.org/sbkro/python-alfred-workflows.svg?branch=develop)](https://travis-ci.org/sbkro/python-alfred-workflows)

This application is an utility for making a *Alfred workflows* plugin. You can create a workflows using Python.

*Alfred* is a Macintosh application. In detail ,refer to follows Web site.

* [Alfred App - Productivity App for Mac OS X](http://www.alfredapp.com)

# Installation
Please bundle my source code in your project. Recommended step is as follow. After setup, import my classes directly from your project.

```sh
$ cd your_project/src_dir
$ git clone https://github.com/sbkro/python-alfred-workflows.git
$ git filter-branch -f --subdirectory-filter workflows HEAD
```

# Features

## workflows.script_filter.ScriptFilterManager
Manipulation of *Script Filter XML* is provided as Python API.

```Python
from workflows.script_filter import ScriptFilterManager

manager = ScriptFilterManager()
manager.append_item('alfread result1', 'icon.png')
print mamanger.tostring()  # Return stdout to Alfred.
# <items>
#   <item>
#     <title>alfred result1</title>
#     <icon>icon.png</icon>
#   </item>
# </items>
```

### tostring()
#### Summary
Return script filter xml as string.

#### Returns
* str: script filter xml. Please return this to Alfred using stdout.

### append_item(self, title, icon_path_or_name, subtitle=None, uid=None, arg=None, valid=None, autocomplete=None, icon_type=None, is_file=False)

#### Summary
Append item in Alfred's search result.

#### Args
* title (str, required): title text
* icon_path_or_name (str, required): icon path or name
* subtitle(str, option): sub title text
* uid (str, option): unique id.
* arg (str, option): arg
* valid (bool, option): If it is False, it won't be actioned.
* autocomplete (str, option): If you select the item, this string is complemented in Alfred.
* icon_type (str, option): Loading type of specified icon. Support type is follows.
  * fileicon: load file type direcotry from icon path.
  * filetype: load file type from icon name.
* is_file (bool, option default=False): If it is True, specified item treated as file.

### append_subtitle(index, subtitle, shift=None, fn=None, ctrl=None, alt=None, cmd=None)
#### Summary
Add the subtitle to an existing result item.

#### Args
* index (int, required): item index
* subtitle (str, required): subtitle text
* shift (str, option): subtitle text when shift is pressed.
* fn (str, option): subtitle text when fn is pressed.
* ctrl (str, option): subtitle text when ctrl is pressed.
* alt (str, option): subtitle text when alt is pressed.
* cmd (str, option): subtitle text when cmd is pressed.

#### Raises
* ValueError: If subtitle is added in specified item, already.

### append_text(inde, copy=None, largetype=None)
#### Summary
Add the text information to an exsiting result item.

#### Args
* index (int, required): item index
* copy (str, option): define text when copying from Alfred's result. (2.3 later)
* largetype (str, option): define text for large type. (2.3 later)

#### Raises
* ValueError:  text is added in specified item, already.

# Example
Refer to *examples* folder.

# Operating Environments
* OSX 10.9.5
* Python 2.7.9
* Alfred v2 later and Powerpack license

# License
* The MIT License

# Change Log
## v.0.1.0: 2015/06/13
* First release. Implement a Python wrapper of *Script Filter XML*.
