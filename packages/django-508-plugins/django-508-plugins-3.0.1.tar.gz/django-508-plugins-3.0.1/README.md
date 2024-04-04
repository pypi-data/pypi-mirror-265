# django-508-plugins
Installable Django app containing 508-compliant plugins.

## Requirements:

* jQuery 3.6.0+ or jQuery 3.4.1.

## Current 508 Compliant packages:

* select2 v3 [ [Docs](https://select2.github.io/select2/) ]
* selectcn (select2 V4.1.0-rc.0) [ [Docs](https://select2.org/) ]
* jQuery 1.11.4 Datepicker [ [Git](https://github.com/jquery/jquery-ui) | [Docs](https://api.jqueryui.com/datepicker/) ]

## Usage

```
pip install django-508-plugins
```

### select2

Add `plugins.select2` to your `INSTALLED_APPS` setting.  Then, add the following source files to your template::

    select2/select2.css
    select2/select2-bootstrap.css # Only needed if using Bootstrap 3
    select2/select2.js

**Note**:  It is **highly** recommnded you do not include both `plugins.select2` and `plugins.selectcn` stylesheets in the same template.  These stylesheets include rules that will conflict with each other and can cause unexpected results.

### selectcn


Add `plugins.selectcn` to your `INSTALLED_APPS` setting.  Then, add the following source files to your template::

    selectcn/css/selectcn.css
    selectcn/js/selectcn.js

**Note**:  It is **highly** recommended you do not include both `plugins.selectcn` and `plugins.select2` stylesheets in the same template.  These stylesheets include rules that will conflict with each other and can cause unexpected results.

When using selectcn, make sure the the `for` attribute of the related `<label>` tag matches the ID of the select box.

### datepicker

Add `plugins.datepicker` to your `INSTALLED_APPS` setting.  In order for the 508 Compliant datepicker to work, you must include jQuery UI in your template. Add the following source files to your template::

    jquery-ui/jquery-ui.css
    jquery-ui/jquery-ui.js
    datepicker/js/jqueryui_datepicker_508.js

**Note** This build of jquery-ui only includes the jQuery UI Datepicker.  Other jQuery UI components may not be 508 Compliant.

**Note** This build also contain a yet to be released bug fix on datepicker which caused issues with a datepicker's dropdown widget placement on screen if it was in a popover or modal or there was scrolling. This bugfix has yet to be released on the current stable version of jquery-ui and this build still uses the legacy 1.11.4 build which will likely never get this bugfix. The pull request for this issue is here: [https://github.com/jquery/jquery-ui/pull/1935](https://github.com/jquery/jquery-ui/pull/1935). These changes were built and minified the same way that jquery-ui builder built the source for the original jquery-ui in here, only instead built using a local instance of download.jqueryui.com against the one line change from the bug fix applied to the 1.11 stable branch jquery-ui.ui.datepicker.js file.

Minified versions of `datepicker` source files are also included in the install.
