.. title: auto
.. subtitle: Macros to implement automatic filter and exposure time control
.. date: jan 31 2012
.. version: $Revision: 25 $
.. manual_section: macros
.. manual_group: counting

#################
AUTO.MAC
#################

===================
General Information
===================

Summary
=======
This macro provides a set of definitions which allow for automatic filter
transmission and exposure time adjustments during experiments.

Description
===========
After each count command, the obtained counts are evaluated and checked for
over-/under-exposure. In case of unsatisfactory count levels, filter
transmissions and optionally exposure times are adjusted and exposures are
repeated until a valid exposure is obtained.

Exposure optimization modes
---------------------------
Two different modes of operation are available to optimize the count levels
for each exposure:

- Post-exposure adjustments: Each new exposures is taken with settings that
  are based on the feedback obtained from the previous one. This mode is
  based on the assumption that the measured intensity profiles are only
  gradually changing, and that a satisfactory prediction of the change in
  the count levels can be obtained in most cases to yield a good exposure.
  In those cases where the predictions fail and the new exposure falls
  outside the acceptable limits, the settings are adjusted and the exposure
  is retaken immediately.
- Pilot exposure: Each exposure is preceeded by a short pilot exposure,
  which is used to establish the count levels at the current positions.

Both modes have their relative merits and drawbacks. Post-exposure
adjustments are riskier in terms of overexposing a detector, since the
feedback is obtained only after potentially very long exposures. On the
other hand, they are more efficient in terms of dead-time, especially when
scanning signals that change only gradually. In this case, it is very
seldomly necessary to repeat exposures. The pilot exposure mode, in
contrast, is safer, since it detects potentially harmfully strong signals
much faster. This comes at the cost of significantly increased dead-times,
particularly for detectors with longer arming or readout times.

Exposure optimization scheme
----------------------------
The filter and exposure time adjustments principles are based on the
following criteria to formulate an adjustment strategy.  Firstly, it is
important to note that there are two separate effects which may cause an
over-exposure of the detector:

#. Paralizing the counter as a result of a count RATE which exceeds the
   ability of the detector to separate individual photons in time (only for
   single-photon-counting devices, does not apply to charge-integrating).
#. Saturating the counter as a result of exceeding the maximum NUMBER OF
   COUNTS that can be stored in the counter.

The incident photon RATE (case 1) can only be adjusted through the use of
filters (attenuators), while the integrated NUMBER OF COUNTS is affected
both by the filter transmission and the integration duration (count time).
In this implementation, ensuring a valid photon RATE always takes
precedence over any other adjustment. Once the rate has been optimized
(keeping it within a given band below the saturation threshold), the
exposure times may be adjusted. See the next sections below for details.

Filter tramsmission adjustments (RATE)
----------------------------------------
The filter adjustment assures a high incident photon rate within a band
just below the rate limit of the detector. The width of the band is
defined by the step size in transmission, defined in AUTO_FILTER_FACTOR,
which is used for each correction. If the count rate is higher than
AUTO_RATE_LIMIT, the transmission is immediately reduced by
AUTO_FILTER_FACTOR and the exposure is retaken. If the count rate is
lower than AUTO_RATE_LIMIT/(2*AUTO_FILTER_FACTOR), the change in
transmission required to reach a count rate of 0.75*AUTO_RATE_LIMIT is
calculated, the transmission increased by that factor and the exposure is
retaken immediately. If the measured count rate falls between these limits,
no change is applied to the filters. The following scheme illustrates
this behavior::

  Threshold levels           Actions
  ----------------           -------

                             - decrease trasmission by AUTO_FILTER_FACTOR
                             - retake exposure immediately
  AUTO_RATE_LIMIT---------------------------------------------------------
   /\
   || 2*AUTO_FILTER_FACTOR   - leave filters as they are
   \/
  ------------------------------------------------------------------------
                             - calculate change in transmission required to
                               reach 0.75*AUTO_RATE_LIMIT
                             - increase trasmission by this factor
                             - retake exposure immediately

Exposure time adjustments (integrated NUMBER OF COUNTS)
---------------------------------------------------------
Exposure time adjustments are designed with maximum efficiency in mind.
The general idea is to attempt to maintain the integrated count level as
close as possible to the user-defined AUTO_COUNT_TARGET, but to minimize
the number of re-exposures by accepting exposures which fall into an
"acceptable" count range, which is defined as any count level between
the detectors saturation count AUTO_COUNT_HIGH and a user-defined
lower count level AUTO_COUNT_LOW. If the exposure is within this
acceptable band, a new count time to reach the target level is
calculated based on the current exposure, but only applied to the next
exposure in an attempt to predict a change in the right direction. If the
current exposure falls outside the acceptable count range, the expsoure
time is adjusted and the exposure is retaken immediately. Note that
chosing a small acceptable range will thus result in retaking many
exposures, hence increasing scan times.
Count times will be adjusted between user-defined limits AUTO_EXP_LOW and
AUTO_EXP_HIGH and rounded to a user-defined precision AUTO_COUNT_PREC.

The diagram below outlines the measures taken when the registered maximum
NUMBER OF COUNTS falls into the various defined ranges::

  Threshold levels           Actions
  ----------------           -------

                             - reduce exposure time (if > minimum time)
                             - retake exposure immediately
  AUTO_COUNT_HIGH---------------------------------------------------------
                             - reduce exposure time (if > minimum time)
                             - apply only to next exposure
  AUTO_COUNT_TARGET-------------------------------------------------------
                             - increase exposure time (if < maximum time)
                             - apply only to next exposure
  AUTO_COUNT_LOW----------------------------------------------------------
                             - increase exposure time (if < maximum time)
                             - retake exposure immediately


Configuration
=============

No special configuration is needed to run these macros. Simply load the macro
file and run ''auto_setup''::

> qdo auto.mac
> auto_setup

Dependencies
------------

Dependencies on other macros:

* filter.mac (used to control the attenuators):

  - filter_trans
  - filter_get_trans()
  - filter_get_trans_up()
  - filter_get_mask()
  - filter_max()

* recount (modified count command used to retake an exposure)

Impact
------
The following chained macro definitions are affected by this macro:

* user_prescan_head
* user_chk_counts (provided in our modified ``count`` command)
* user_precount

File information
================

Authors
-------
* C.M. Schlepuetz (CS, cschlep),
  Argonne National Laboratory, cschlep@aps.anl.gov
* Y. Yang (YY, ysyang),
  University of Michigan, ysyang@umich.edu

Creation date
-------------
2011/02/25

Copyright
---------
Copyright 2010 by the above authors (see AUTHOR/AUTHORS)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

Version
-------
::

  $Date: 2011-04-11 13:17:13 -0400 (Mon, 11 Apr 2011) $
  $Author: cschlep $
  $URL: file:///data/svn/software/spec/trunk/common/auto.mac $
  $Revision: 25 $
  
  
Change log
----------
2011/02/25 (CS, YY):

- completely reworked previous versions of ``auto.mac`` to produce this new
  version:

  * improved efficiency
  * simplified code
  * new method of scaling the count times (see description above)

2011/04/04 (CS):

- cleaned up code further
- added and updated documentation
- added ``auto_setup`` macro
- added AUTO_AREADETECTOR_VERSION global to track which version of
  areaDetector is used in ``auto_init_analysis``.
- added ``auto_on`` and ``auto_off``
- changed all macro names to lower case and underscore naming convention
- changed all calls to macros from ``filter.mac`` to lower case and underscore
  naming conventions.

2011/04/11 (CS):

- changed ``auto_prescan_header``: if AUTO_LEVEL > 1, set the exposure times to
  the minimum exposure time to start with.

2012/03/29 (CS):

- modified code documentation to be compatible with the ROBODoc
  documentation generation software.
- monitor a configurable SPEC counter rather than an EPICS channel for the
  adjustments. This allows for the monitoring of any arbitrary counter in
  SPEC, but requires that whatever signal is to be monitored is captured in
  a SPEC counter during the count process.
- reworked the setup routines for easier use.
- removed unnecessary ``auto_init_analysis``
- removed unnecessary AUTO_AREADETECTOR_VERSION global variable
- renamed many variables for improved consistency

2012/04/23 (CS):

- fixed a bug where long exposures with valid rate but saturating the
  counter would result in an infinite loop.
  
2012/07/06 (CS):

- changed code documentation to be compatible with the new SPEC domain for the
  SPHINX code documentation suite.
  
TO DO
-----

- Extensive testing of the pilot exposure mode
- complete documentation
- insert hyperlinks into documentation

================
Available Macros
================

auto_help
===============================================================================
Summary
-------
Displays the auto help text.

Usage
-----
::

   > auto_help

.. note:: The help text is generated by simply displaying the text file
   ``auto_mac.txt``, which should reside in the same directory as
   ``auto.mac``. If the file does not exist, a generic help text defined in
   ``auto_help`` is shown.


auto_setup
===============================================================================

Summary
-------
  Set up the control parameters for the automatic filter and exposure
  adjustments.

Description
-----------
  The following parameters can be adjusted to fit the particular needs of an
  experiment or detector type (global variables holding these parameters and
  default values are given in brackets):
  
  * Auto level: the level of automatic adjustments to be performed. Three
    levels are currently available [AUTO_LEVEL = 0]:
    
      ===== ===================================================================
      Level Description
      ===== ===================================================================
      0     No automatic adjustments are made
      1     Only filters are adjusted, no exposure time adjustments
      2     Both filters and exposure times are automatically adjusted
      ===== ===================================================================

  * Auto mode: the mode used to calculate/apply the adjustments. Two modes
    are available [AUTO_MODE = 0]:

      ==== ===================================================================
      Mode Description
      ==== ===================================================================
      0    Post-exposure analysis: exposures are taken at normal settings and
           analyzed in retrospect. The exposure is only retaken if it is
           deemed unacceptable. Otherwise, the calculated adjustments are
           applied only to the next exposure. This mode is faster, but riskier
           in terms of over-exposing the detector for potentially much longer
           times.
      1    Pilot exposure mode: A short pilot exposure is taken before each
           exposure to determine the correct filter and exposure time
           settings. This is safer in terms of identifying over-exposures
           quickly and provides optimized settings for each exposure, but
           comes at a considerable cost in additional dead time. The pilot
           exposure time is specified in AUTO_PILOT_EXPTIME.
      ==== ===================================================================

  * Counter to monitor: the SPEC counter mnemonic or number of the counter
    used to assess the validity of the exposure. Note that when using area
    detectors, it is necessary to monitor the count levels per pixel, as this
    the saturation conditions. In this case, there needs to be a counter
    configured that is monitoring the maximum count rate of all pixels within
    the relevant region of interest. [AUTO_COUNTER = det]

  * Count RATE high limit: the maximum count rate (counts per second) on
    the detector that is acceptable for the experiment. If the measured count
    rate is higher than this limit, filters will be inserted to lower the
    rate. [AUTO_RATE_LIMIT = 2.0e5]

  * Target count level: the desired count level for a "perfect" exposure.
    All adjustments applied to filter and/or count times aim to achieve this
    level. [AUTO_COUNT_TARGET = 1.0e4]

  * Count level low limit: The lower count limit for an acceptable exposure.
    If the measured level is below this, filters and exposure times will be
    adjusted (if possible) and the exposure retaken.
    [AUTO_COUNT_LOW = 5000]

  * Counter saturation limit: The upper count limit for an acceptable
    exposure. This should be chosen below the actual saturation level of the
    detector. If the measured level exceeds the saturation limit, filters and
    exposure times will be adjusted (if possible) and the exposure is
    repeated.
    [AUTO_COUNT_HIGH = 5.0e5]

  * Transmission step: The step in filter transmission to be taken when
    adjusting the filters. The specified step must be larger than the
    largest available incremet in transmission values of the experimental
    setup to ensure that the adjustments can be successful. Ideally, this
    number is chosen anywhere between 2 and 10, but may need to be higher
    depending on the available filters. [AUTO_FILTER_FACTOR = 5]

  * Minimum exposure time: Minimum allowable exposure time to be used whith
    automatic exposure time adjustments. [AUTO_EXP_LOW = 1]

  * Maximum exposure time: Maximum allowable exposure time to be used whith
    automatic exposure time adjustments. [AUTO_EXP_HIGH = 10]

  * Pilot exposure time: Exposure time for the pilot exposure used in pilot
    mode. [AUTO_PILOT_EXPTIME = 0.05]

  * Count time precision: Automatically calculated count times will be
    rounded to this precision. Typically, a value of 0.01 or 0.001 seconds is
    recommended. [AUTO_COUNT_PREC = 0.01]

  * Maximum number of retries: The maximum number of retries to adjust
    exposure and filter settings before giving up. This avoids infinite loops
    due to inconsistent choices of control parameters. [AUTO_RETRY_MAX = 20]

Usage
-----
::

  > auto_setup
      then answer the questions



auto_off
=============

Summary
-------
Turn off any automatic filter and exposure adjustments.

Usage
-----
::

  > auto_off

.. note:: This command is equivalent to ``auto_set_level 0``

See also
--------
auto_set_level, auto_on



auto_set_level, auto_on
=========================

Summary
-------
Set the level of automatic filter and exposure adjustments.

Usage
-----
::

  > auto_set_level [<level>]
  > auto_on [<level>]
      where <level> can be one of the following:
        0 - automatic filter and exposure OFF
        1 - automatic filter ON, automatic exposure OFF
        2 - automatic filter and exposure ON
      if <level> is ommitted, the users is asked for input

Example
-------
::

  > auto_set_level
      then answer the questions in the dialogue

  > auto_on 1
      turns on automatic filter adjustments (level 1)

.. note::
   ``auto_set_level`` and ``auto_on`` are equivalent to each other

See also
--------
auto_off


auto_set_mode
==================

Summary
-------
Set the acquisition mode to be used for the automatic filter and
exposure time adjustments.

Description
-----------
Need some more details here...


Usage
-----
::

  > auto_set_mode [<mode>]
      where <mode> must be one of the following:
        0 - post-exposure analysis
        1 - pilot exposure mode
      when called with no arguments, the user is prompted

Example
-------
::

  > auto_set_mode 1
      use the pilot exposure mode for automatic adjustments.

See also
--------
auto, auto_setup


auto_set_exposure
======================

Summary
-------
Set the maximum and minimum exposure times used for automatic exposure
adjustments.

Usage
-----
::

  > auto_set_exposure [<min> <max>]
      where <min> is the minimum and <max> the maximum exposure time [s]
      when called with no arguments, the user is prompted

Example
-------
::

  > auto_set_exposure 1 10
      sets the minimum exposure time to 1 sec and the maximum to 10 sec.

auto_show
==============

Summary
-------
Display the current auto settings.

Usage
-----
::

  > auto_show

auto_show_exposure
=======================

Summary
-------
Display the current auto-level exposure settings.

Usage
-----
::

  > auto_show_exposure


================
Internal Macros
================

_auto_print_setup
======================

Summary
-------
Prints the configuration options and current values to screen

.. note::
   The option numbers must be kept in sync between ``_auto_set_option`` and
   ``_auto_print_setup``.


_auto_set_option
=====================

Summary
-------
Sets a new value for a given option

Description
-----------
Sets a new value for a given option from the options menu that was created
with the _auto_print_setup command.

.. note::
   The option numbers must be kept in sync between ``_auto_set_option`` and
   ``_auto_print_setup``.


_auto_analyze_exposure
===========================

Summary
-------
Analyze the previous exposure

Description
-----------
This macro retrieves the necessary information to analyze the last exposure
and to initiate adjustments, if necessary. Usually, this step consists only
of retrieving the count value from the monitored SPEC counter, but for more
sophisticated experimental setups, this definition could be overwritten to
include non-standard procedures, such as retrieving counts from EPICS PVs,
etc.

Usage
-----
::

  > _auto_analyze_exposure



_auto_adjust()
===================

Summary
-------
Calculate and apply necessary exposure time and filter adjustments.

Description
-----------
The function returns 1 if transmission or exposure time are changed, 0
otherwise.


_auto_check_exposure
=========================

Summary
-------
Make sure the user-entered exposure times are consistent

Usage
-----
::

  > _auto_check_exposure


_auto_check_levels
=======================

Summary
-------
Make sure the user-entered count levels are consistent

Usage
-----
::

  > _auto_check_levels


_auto_calc_exposure
========================

Summary
-------
Make sure the requested exposure time is between the min and max values and
round it to the given count time precision.

Usage
-----
::

  > adjusted_time = _auto_calc_exposure(requested_time)



_auto_adjust_redo()
========================

Summary
-------
Determines whether the auto-adjusting has been successful.

Description
-----------
If the current exposure does not meet the required criteria, counting
is repeated until the best possible filter and exposure settings have been
obtained, or a maximum number of retry counts has been reached.
The function returns 1 in case of success, 0 otherwise.

Usage
-----
::

  > success = _auto_adjust_redo()

.. note::
   This macro makes use of the ``recount`` macro, which has to be added to SPEC
   during the startup procedure.

_clear_screen
==================

Summary
-------
Clears the terminal screen

Description
-----------
Clears the screen without losing the screen history or messing up the
scrolling capabilities (this has been a problem for certain terminals)
by blanking out the entire height of the screen and returning the cursor to
the top left corner.
