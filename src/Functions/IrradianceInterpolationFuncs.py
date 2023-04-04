import math
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline
import scipy.constants

def ParseDatafile(filename):
    try:
        with open(filename, "r") as openedfile:
            fileData = openedfile.readlines()
        # detect line that header starts on, if any
        headerIndex = 0
        for line in fileData:
            try:
                float(line.strip("\n").replace("\t", " ").split(" ")[0].split(",")[0])
            except ValueError as headerErr:
                if "could not convert string to float:" in str(headerErr):
                    headerIndex += 1
                else:
                    raise headerErr
        wavelengths = []
        irradiances = []
        for i in range(headerIndex, len(fileData)):
            wavelengths.append(float(fileData[i].strip("\n").replace("\t", " ").split(" ")[0].split(",")[0]))
            irradiances.append(float(fileData[i].strip("\n").replace("\t", " ").split(" ")[-1].split(",")[-1]))

        return wavelengths, irradiances
    except Exception as err:
        raise err

def GrayBody(wavelength, a, b, C):
    """
    Calculates irradiance based on a model of a gray body.
    Coefficient inputs are generally determined from curve-fitting.
    The a and b coefficients are determined first from curve-fitting, then used with the gray body model to determine C, also through curve-fitting

    Gray body model assumed:
        E_lambda = (C_0 + C_1 * lambda + C_2 * lambda**2 + ... + C_n * lambda**n) * lambda**-5 * e^(a + b / lambda)

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        "The 1973 NBS Scale of Spectral Irradiance"

    ----------------------------------------------------------------------------
    Inputs
        wavelength  - wavelength or array of wavelengths. Expected units: nm
        a           - coefficient in gray body model, related to gray body emissivity with e**a. Needs determined independently by fitting data (see ab_model function)
        b           - coefficient in gray body model, related to reciprocal of temperature distribution. Needs determined independently by fitting data (see ab_model function)
        C           - nx1 array containing gray body coefficients C_0, C_1, ... , C_n

    ----------------------------------------------------------------------------
    Returns
        Irradiance with units W/cm**-3
    """
    return __GrayBody__(a, b)(wavelength, *C)

def __GrayBody__(a, b):
    """
    Gray body model used in curve-fitting. Written to return another function to allow arbitrary number of coefficients in curve-fitting and while enabling substitution of a and b coefficients.
    Usage in this form to yield irradiance: GrayBody_model(a, b)(wavelength, C1, C2, C3, ...)
    **Intended use is curve-fitting to determine C coefficients. See and use the function 'GrayBody' to calculate irradiance from wavelength and coefficients**

    Gray body model assumed:
        E_lambda = (C_0 + C_1 * lambda + C_2 * lambda**2 + ... + C_n * lambda**n) * lambda**-5 * e^(a + b / lambda)

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        NIST TN 594-13 "The 1973 NBS Scale of Spectral Irradiance"

    ----------------------------------------------------------------------------
    Inputs
        a - coefficient in gray body model, related to gray body emissivity with e**a. Needs determined independently by fitting data (see ab_model function)
        b - coefficient in gray body model, related to reciprocal of temperature distribution. Needs determined independently by fitting data (see ab_model function)

    ----------------------------------------------------------------------------
    Returns
        GrayBody - function with independent variable (wavelength) and coefficients (C) as inputs
    """
    def GrayBody_model(wavelength, *C):
        """
        Gray body model used in curve-fitting. Written to return another function to allow arbitrary number of coefficients in curve-fitting and while enabling substitution of a and b coefficients.
        Usage in this form to yield irradiance: GrayBody_model(a, b)(wavelength, C1, C2, C3, ...)
        **Intended use is curve-fitting to determine C coefficients. See and use the function 'GrayBody' to calculate irradiance from wavelength and coefficients**

        Gray body model assumed:
            E_lambda = (C_0 + C_1 * lambda + C_2 * lambda**2 + ... + C_n * lambda**n) * lambda**-5 * e^(a + b / lambda)

        ----------------------------------------------------------------------------
        Notes
            Authored by: Michael Braine, Physicist, NIST Gaithersburg
            EMAIL: michael.braine@nist.gov
            October 2022

        ----------------------------------------------------------------------------
        References
            NIST TN 594-13 "The 1973 NBS Scale of Spectral Irradiance"

        ----------------------------------------------------------------------------
        Inputs
            wavelength  - wavelength or array of wavelengths. Expected units: nm
            C           - nx1 array containing gray body coefficients C_0, C_1, ... , C_n

        ----------------------------------------------------------------------------
        Returns
            Irradiance with units W/cm**-3
        """
        for i, coefficient in enumerate(C):
            if i == 0:
                summ = coefficient
            else:
                summ = summ + coefficient*np.array(wavelength)**i
        return summ*np.array(wavelength)**-5*math.e**(a + b/np.array(wavelength))
    return GrayBody_model

def ab_model(wavelength, a, b):
    """
    Model to determine coefficients in Gray Body model.
    These constants are fit and determined independently of others in gray body model by fitting data to:
        ln(E_lambda*lambda**5) = a + b/lambda

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        NIST TN 594-13 "The 1973 NBS Scale of Spectral Irradiance"

    ----------------------------------------------------------------------------
    Inputs
        wavelength  - wavelength or array of wavelengths. Expected units: nm
        a           - coefficient in gray body model, related to gray body emissivity with e**a. Needs determined independently by fitting data (see ab_model function)
        b           - coefficient in gray body model, related to reciprocal of temperature distribution. Needs determined independently by fitting data (see ab_model function)

    ----------------------------------------------------------------------------
    Returns
        GrayBody - function with independent variable (wavelength) and coefficients (C) as inputs
    """
    return math.e**(a + b/wavelength)/wavelength**5

def UncertaintyFromCovariance(covariance, k=1):
    """
    Calculates uncertainty in coefficients determined from curve-fitting using the fit's covariance matrix.

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        none

    ----------------------------------------------------------------------------
    Inputs
        covariance  - nxn covariance matrix
        k           - level of confidence in returned uncertainty value(s). defaults to k=1

    ----------------------------------------------------------------------------
    Returns
        Uncertainty - n uncertainties
    """
    return np.sqrt(np.diag(covariance))

def GrayBodyCoefficients(wavelength, irradiance, region, dof):
    """
    Performs curve-fitting on wavelength-irradiance data to generate coefficients and their uncertainties using the gray body model

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        none

    ----------------------------------------------------------------------------
    Inputs
        wavelength  - array of wavelengths. Expected units: nm
        irradiance  - array irradiances. Expected units: W cm^-3 sr^-1
        region      - 1x2 array or tuple of start/stop wavelengths for the interpolation. syntax is [start, stop]. Expected units: nm
        dof         - degrees of freedom for gray body coefficient fitting

    ----------------------------------------------------------------------------
    Returns
        coefficients_GrayBody   - C coefficients in the gray body model
        U                       - uncertainties in the C coefficients
        a                       - coefficient in gray body model, related to gray body emissivity with e**a
        b                       - coefficient in gray body model, related to reciprocal of temperature distribution
    """
    i_lowerBound, i_upperBound = WavelengthRegionIndex(wavelength, region)

    ab, ab_covariance = curve_fit(ab_model, wavelength[i_lowerBound:i_upperBound], irradiance[i_lowerBound:i_upperBound], p0=[50, -4800], sigma=irradiance[i_lowerBound:i_upperBound])
    a, b = ab[0], ab[1]
    U_ab = UncertaintyFromCovariance(ab_covariance)

    coefficients_GrayBody, coeff_covariance = curve_fit(__GrayBody__(a, b), wavelength[i_lowerBound:i_upperBound], irradiance[i_lowerBound:i_upperBound], p0=[0]*(dof+1), sigma=irradiance[i_lowerBound:i_upperBound])
    U_coeff = UncertaintyFromCovariance(coeff_covariance)
    return coefficients_GrayBody, U_coeff, a, b, U_ab

def GrayBodyInterpolation(region, coefficients, a, b, step):
    """
    Performs interpolation on wavelength-irradiance data to generate coefficients and their uncertainties using the gray body model

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        none

    ----------------------------------------------------------------------------
    Inputs
        region          - 1x2 array or tuple of start/stop wavelengths for the interpolation. syntax is [start, stop]. Expected units: nm
        coefficients    - C coefficients in the gray body model
        a               - coefficient in gray body model, related to gray body emissivity with e**a
        b               - coefficient in gray body model, related to reciprocal of temperature distribution
        step            - step size to perform interpolation

    ----------------------------------------------------------------------------
    Returns
        wavelengths     - array of wavelengths used in interpolation. Units: nm
        irradiances     - array of iraddiances from the interpolation. Units: W cm^-3 sr^-1
    """
    wavelengths = np.arange(region[0], region[1]+step, step).astype(float)
    return wavelengths, __GrayBody__(a, b)(wavelengths, *coefficients)

def WavelengthRegionIndex(wavelength, region):
    """
    Finds indices of bounding wavelengths based on given region

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        none

    ----------------------------------------------------------------------------
    Inputs
        wavelength  - array of wavelengths. Expected units: nm
        irradiance  - array irradiances. Expected units: W cm^-3 sr^-1

    ----------------------------------------------------------------------------
    Returns
        i_lowerBound    - index of lower bound wavelength
        i_upperBound    - index of upper bound wavelength
    """
    return np.where(np.array(wavelength)==region[0])[0][0], np.where(np.array(wavelength)==region[1])[0][0]+1

def CubicSplineInterpolation(wavelength, irradiance, region, step):
    """
    Performs cubic spline interpolation on wavelength-irradiance data

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        none

    ----------------------------------------------------------------------------
    Inputs
        wavelength  - array of wavelengths. Expected units: nm
        irradiance  - array irradiances. Expected units: W cm**-3 sr^-1
        region      - 1x2 array or tuple of start/stop wavelengths for the interpolation. syntax is [start, stop]. Expected units: nm
        step        - step size to perform interpolation

    ----------------------------------------------------------------------------
    Returns
        wavelengths     - array of wavelengths used in interpolation. Units: nm
        irradiances     - array of iraddiances from the interpolation. Units: W cm^-3 sr^-1
        f.c             - cubic spline coefficients used in interpolation
        f               - cubic spline fit (scipy object)
    """
    i_lowerBound, i_upperBound = WavelengthRegionIndex(wavelength, region)
    f = CubicSpline(wavelength[i_lowerBound:i_upperBound], irradiance[i_lowerBound:i_upperBound], bc_type="natural")
    wavelengths = np.arange(region[0], region[1]+step, step).astype(float)
    return wavelengths, f(wavelengths), f.c, f

def PeakWavelength(wavelengths, irradiances):
    return wavelengths[np.argmax(irradiances)]

def ApparentBBTemp(wavelengths, irradiances):
    """
    Calculates the gray body temperature (apparent black body temperature) using Wein's displacement law

    ----------------------------------------------------------------------------
    Notes
        Authored by: Michael Braine, Physicist, NIST Gaithersburg
        EMAIL: michael.braine@nist.gov
        October 2022

    ----------------------------------------------------------------------------
    References
        none

    ----------------------------------------------------------------------------
    Inputs
        wavelengths  - array of wavelengths. Expected units: nm
        irradiances  - array irradiances. Expected units: W cm^-3 sr^-1

    ----------------------------------------------------------------------------
    Returns
        temperature - apparent black body temperature. Units: K
    """
    return PeakWavelength(wavelengths, irradiances)/1e2/scipy.constants.physical_constants['Wien wavelength displacement law constant'][0]
