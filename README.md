# IrradInterPy: Irrad(iance) Inter(polation) Py(thon)
## About
IrradInterPy is an interpolation program for irradiance data from 250 nm to 2500 nm using a gray body model for nonlinear least squares fitting, and returns coefficients for that fit and interpolated data in user-defined steps. Both fit coefficients and interpolation results are written to a CSV, along with uncertainty in each coefficient.

The GUI, when data has been read and interpolated, appears in Figure 1.

<p align="center">
    <img src=images/Main-350to900.png>
    <figcaption><b>Figure 1:</b> IrradInterPy GUI with data loaded and interpolated from 350 nm to 900 nm</figcaption>
</p>

Data read into the program must be in CSV or TXT format, either comma- or tab-delimited. The first column must contain wavelengths, and the second column must contain irradiance. The program will strip out any header data, but there must not be any additional data below rows of wavelengths and irradiance.

The gray body model used to nonlinear least squares fit the measurement data is 

 $$ E_\lambda = (A_0 + A_1 \lambda + A_2 \lambda^2 + ... + A_n \lambda^n) \lambda^{-5} exp^{a + \frac{b}{\lambda}} $$

where the coefficients $a$ and $b$ are determined separately by least squares fitting to

$$\ln{E_\lambda \lambda^5 = a + \frac{b}{\lambda}}$$

Additionally, the coefficients $A_0$, $A_1$, ... , $A_n$ are determined with $\frac{1}{E_\lambda^2}$ weighting, using an assumption of constant relative measurement error (see NBS TN 594-13 in Documentation).

## How to use
IrradInterPy requires Python >= 3.9.16 and the following libraries with their dependencies:
* NumPy >= 1.23.3
* SciPy >= 1.9.1

To use the GUI, additional libraries and their dependencies are required:
* PyQT5 >= 5.15.7
* matplotlib >= 3.5.2

The virtual environment file, `IrradInterPy.yaml` will specifiy all required libraries for use of the interpolation functions and GUI.

**Note:** older versions of these libraries and Python may work, but are untested.

There are two ways to use IrradInterPy: [with the GUI](#LaunchGUI), or [directly with functions library](#UseLibrary)

### How to launch GUI <a class="anchor" id=LaunchGUI></a>
With `src` as the root folder in a terminal that has the IrradInterPy python virtual environment in its path, use `python IrradInterPy.py` to launch the GUI. Read data into the program with `File > Open datafile ...` where a dialog opens to navigate and select the datafile.

In the GUI, each time a selection is made, e.g. changing the interpolation step size, the coefficients, interpolation, and visualization update automatically.

First, select the lower and upper wavelength bounds to apply the fit over, and the degrees of freedom of the fit. The degrees of freedom selection dictates the number of A$_n$ coefficients.

Next, select the lower and upper wavelength bounds to apply the interpolation over, and enter the desired interpolation step. Because extrapolation can easily produce poor results from this fit, when selecting a wavelength bound of interpolation that is outside the region of the fit, the fit will automatically change to the interpolation bounds.

Last, use the `Write gray body interpolation to file` button below the interpolation results table to generate a CSV containing the fit coefficients and interpolation results. A dialog will appear that allows naming and locating the output CSV file.

### How to import and use library <a class="anchor" id=UseLibrary></a>
With `src` as the root folder, use `import Functions.IrradianceInterpolationFuncs as IIF`. 

Read measurement data into Python with `wavelengths, irradiances = IIF.ParseDatafile(filename)`

Fit coefficients are determined with `GBcoefficients, GBuncertainty, GBa, GBb, abUncertainty = IIF.GrayBodyCoefficients(wavelengths, irradiances, (lowerBound, upperBound), DegreesOfFreedom)`. 

Inputs to the `GrayBodyCoefficients` function are:
* wavelengths - list/array of wavelengths, units of nanometers
* irradiances - list/array of irradiance measurements, units of W cm$^{-3}$ sr$^{-1}$
* (lowerBound, upperBound) - tuple of lower and upper wavelength bounds to fit over
* DegreesOfFreedom - fit degrees of freedom, determines number of coefficients of A$_n$

Returned from `GrayBodyCoefficients` are:
* list of coefficients of A$_n$
* uncertainty in A$_n$ coefficients
* coefficient $a$
* coefficient $b$
* uncertainty in coefficients $a$ and $b$

Perform the interpolation with `GBinterpWavelengths, GBinterpIrradiances = IIF.GrayBodyInterpolation((lowerBound, upperBound), GBcoefficients, GBa, GBb)`

Inputs to the `GrayBodyInterpolation` function are:
* (lowerBound, upperBound) - tuple of lower and upper wavelength bounds to interpolate over
 * list of coefficients of A$_n$
 * coefficient $a$
 * coefficient $b$

 ### General guidance for the interpolation