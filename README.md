# IrradInterPy: Irrad(iance) Inter(polation) Py(thon)
## Table of Contents
* [About](#about)
* [Python requirements](#requirements)
* [How to use](#howToUse)
    - [How to launch GUI with executable](#launchExe)
    - [How to launch GUI with Python script](#launchScript)
    - [How to import and use library (no GUI)](#useLibrary)
* [General guidance for irradiance interpolation](#guidance)

## About <a class="anchor" id=about></a>
IrradInterPy is an interpolation program for irradiance data from 250 nm to 2500 nm using a gray body model for nonlinear least squares fitting. It returns coefficients for that fit and the interpolated data in user-defined steps. Both fit coefficients and interpolation results are written to a CSV, along with the uncertainty in each coefficient.

The GUI, when data has been read and interpolated, appears in Figure 1.

<p align="center">
    <img src=images/Main-350to900.png>
    <figcaption><b>Figure 1:</b> IrradInterPy GUI with data loaded and interpolated from 350 nm to 900 nm</figcaption>
</p>

Data read into the program must be in CSV or TXT format, either comma- or tab-delimited. The first column must contain wavelengths, and the second column must contain irradiance. The program will strip out any header data, but there must not be any additional data below rows of wavelengths and irradiance.

The gray body model used to nonlinear least squares fit the measurement data is the product of a polynomial and Planckian function

 $$ E_\lambda = (A_0 + A_1 \lambda + A_2 \lambda^2 + ... + A_n \lambda^n) \lambda^{-5} exp^{a + \frac{b}{\lambda}} $$

where the coefficients $a$ and $b$ are determined by least-squares fitting to the Planckian function separately

$$\ln{E_\lambda \lambda^5 = a + \frac{b}{\lambda}}$$

Additionally, the coefficients A<sub>0</sub>, A<sub>1</sub>, ... , A<sub>n</sub> are determined with $\frac{1}{E_\lambda^2}$ weighting, using an assumption of constant relative measurement error (see NBS TN 594-13 in Documentation).

## Python requirements <a class="anchor" id=requirements></a>
IrradInterPy requires Python >= 3.9.16 and the following libraries with their dependencies:
* NumPy >= 1.23.3
* SciPy >= 1.9.1

To use the GUI, additional libraries and their dependencies are required:
* PyQT5 >= 5.15.7
* matplotlib >= 3.5.2

The virtual environment file, `IrradInterPy.yaml`, will specifiy all required libraries for use of the interpolation functions and GUI.

**Note:** older versions of these libraries and Python may work, but are untested.

## How to use<a class="anchor" id=howToUse></a>
There are three ways to use IrradInterPy: [with the GUI using the compiled executable](#launchExe), [with the GUI using the Python script](#launchScript), or [directly with the functions library](#useLibrary)

In the GUI, each time a selection is made, e.g. changing the interpolation step size, the coefficients, interpolation, and visualization update automatically.

First, select the lower and upper wavelength bounds to apply the fit over, and the degrees of freedom of the fit. The degrees of freedom selection dictates the number of A<sub>n</sub> coefficients.

Next, select the lower and upper wavelength bounds to apply the interpolation over, and enter the desired interpolation step. Because extrapolation can easily produce poor results from this fit, when selecting a wavelength bound of interpolation that is outside the region of the fit, the fit will automatically change to the interpolation bounds.

Last, use the `Write interpolation to file` button below the interpolation results table to generate a CSV containing the fit coefficients and interpolation results. A dialog will appear that allows naming and locating the output CSV file.

### How to launch GUI with executable <a class="anchor" id=launchExe></a>
The executable is available from the publicly available Github repository. On the Releases page, the latest executable can be downloaded for Windows 10 machines: https://github.com/usnistgov/IrradInterPy/releases. Simply download the .exe and run it.

### How to launch GUI with Python script <a class="anchor" id=launchScript></a>
With `src` as the root folder in a terminal and IrradInterPy as the active environment, use `python IrradInterPy.py` to launch the GUI. Read data into the program with `File > Open datafile ...` where a dialog opens to navigate and select the datafile.

### How to import and use library (no GUI) <a class="anchor" id=useLibrary></a>
With `src` as the root folder, use `import Functions.IrradianceInterpolationFuncs as IIF`.

Read measurement data into Python with `wavelengths, irradiances = IIF.ParseDatafile(filename)`

Fit coefficients are determined with `GBcoefficients, GBuncertainty, GBa, GBb, abUncertainty = IIF.GrayBodyCoefficients(wavelengths, irradiances, (lowerBound, upperBound), DegreesOfFreedom)`. This function will fit and provide both the polynomial coefficients ($A_0$, $A_1$, ..., $A_n$) and the Planckian coefficients ($a$ and $b$)

Inputs to the `GrayBodyCoefficients` function are:
* `wavelengths` - list/array of wavelengths, units of nanometers
* `irradiances` - list/array of irradiance measurements, units of W cm<sup>-3</sup> sr<sup>-1</sup>
* `(lowerBound, upperBound)` - tuple of lower and upper wavelength bounds to fit over
* `DegreesOfFreedom` - fit degrees of freedom, determines number of coefficients of A<sub>n</sub>

Returned from `GrayBodyCoefficients` are:
* `GBcoefficients` - list of coefficients of A<sub>n</sub>
* `GBuncertainty` - uncertainty in A<sub>n</sub> coefficients
* `GBa` - coefficient $a$
* `GBa` - coefficient $b$
* `abUncertainty` - uncertainty in coefficients $a$ and $b$

Perform the interpolation with `GBinterpWavelengths, GBinterpIrradiances = IIF.GrayBodyInterpolation((lowerBound, upperBound), GBcoefficients, GBa, GBb, step)`

Inputs to the `GrayBodyInterpolation` function are:
* `(lowerBound, upperBound)` - tuple of lower and upper wavelength bounds to interpolate over, units of nanometers
 * `GBcoefficients` - list of coefficients of A<sub>n</sub>
 * `GBa` - coefficient $a$
 * `GBb` - coefficient $b$
 * `step` - step size, units of nanometers

 Returned from `GrayBodyInterpolation` are:
 * `GBinterpWavelengths` - array of interpolated wavelengths
 * `GBinterpIrradiances` - array of interpolated irradiances

 ## General guidance for irradiance interpolation <a class="anchor" id=guidance></a>
 Most fits with this model are best performed in sections and used as piecewise functions while maintaining an overlap in the fit data. Applying a single fit to 200 nm to 2400 nm generally does not produce a better fit than breaking the data up into regions and applying a separate fit to each region. For example, a fit of 200 nm to 410 nm data gives a fit for 200 nm to 400 nm, 390 nm to 810 nm gives a fit for 400 to 800 nm, etc. The slight overlap gives better continuity of the piecewise functions.