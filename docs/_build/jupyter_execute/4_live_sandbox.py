#!/usr/bin/env python
# coding: utf-8

# # Live Sandbox

# In[1]:


import pandas as pd
import math
from scipy import interpolate


# In[2]:


# Definition of constants and variables

# Some common physical constants, mainly used to calculate `maxFlux`
## (the upper bound of energy flux received by a planet that allows it
## to be habitable according to Pierrehumbert (2015))

BIGG       = 6.67428e-11       # Gravitational constant
PI         = 3.1415926535
A          = 0.7344            # Pierrehumbert's Constant
SB         = 5.670373e-8       # Stefan-Boltzmann Constant
LH2O       = 2.425e6           # Latent Heat Capacity of Water
RGAS       = 461.5             # Universal Gas Constant
PLINE      = 1e4               
PREF       = 610.616           # Reference Pressure
TREF       = 273.13            # Reference Temperature
K0         = 0.055             # A constant in Runaway Greenhouse calculation


# Boundaries for albedo values:
ALBMINELSE = 0.05              # General lower bound
ALBMAXELSE = 0.8               # General upper bound
ALBMING    = 0.25              # Lower bound for planets orbiting G-type stars
ALBMAXM    = 0.35              # Upper bound for planets orbiting M-type stars


# The counterpart to maxFlux
## (unlike maxFlux, MINFLUX is a constant that does not depend on a planet's properties)
MINFLUX    = 67

# Definitions of units of measurement,
## mainly used to convert [exoplanet.org](exoplanet.org) data into SI units:
MEARTH     = 5.972186e24       # Earth mass in kilograms
REARTH     = 6378100           # Earth's radius in meters
S0         = 1362              # Solar constant in watts per square meter
MSUN       = 1.988416e30       # Solar mass in kilograms
RSUN       = 6.957e8           # Solar radius in meters
LSUN       = 3.828e26          # Solar luminosity in watts
RJUP       = 7.1492e7          # Jovian radius in meters
MJUP       = 1.8982e27         # Jovian mass in kilograms
AU         = 1.496e11          # The astronomical unit in meters


# In[3]:


# Definition of functions

# 1) A function to calculate the probability distribution of orbital eccentricity
def pofe(ecc,mu,sigma):
    return ((sigma*math.sqrt(2*math.pi))**(-1))*math.exp(-(((ecc-mu)**2)/(2*sigma**2)))/1000

# 2) A function to calculate the probability of a planet's terrestriality
def fp_ter(mPlanet,rPlanet,exoName):
    # Convert the unit to Earth's masses and radii
    mPlanet = mPlanet/MEARTH 
    rPlanet = rPlanet/REARTH
    
    # Calculate mu1
    ## Initialize mu1 value to 0
    mu1 = 0.0       
    
    # Initialize temporary variables to hold a mass/radius value
    ## from the (i-1)th row of the ZS table
    mZSimin1 = 0
    rZSimin1 = 0

    # This block iterates through the the 'M-Pure-MgSiO3' column
    #to find the bracket that contains mPlanet value
    for i in rowNum:
        # Initialize temporary variables to hold a mass/radius value
        #from the i-th row of the ZS table
        mZSi = zs.loc[i, "M-PureMgSiO3"]
        rZSi = zs.loc[i, "R-PureMgSiO3"]
        
        # Comparing mPlanet to the current value of mZSi
        if mPlanet == mZSi:
            mu1 = rZSi
            break                          
        elif mPlanet > mZSi:               
            mZSimin1 = mZSi                
            rZSimin1 = rZSi                  
        else: # if mPlanet < mZSi --> we have found the correct bracket
            f = interpolate.interp1d(zs.loc[(i-1):(i), "M-PureMgSiO3"], zs.loc[(i-1):(i), "R-PureMgSiO3"], kind='linear', assume_sorted=True)
            mu1 = f(mPlanet)
            break

    # Calculate mu2
    mu2 = 0.0
    mZSimin1 = 0
    rZSimin1 = 0
    for i in rowNum:
        mZSi = zs.loc[i, "M-MgSiO3-H2O-5050"]
        rZSi = zs.loc[i, "R-MgSiO3-H2O-5050"]
        if mPlanet == mZSi:
            mu2 = rZSi
            break
        elif mPlanet > mZSi:
            mZSimin1 = mZSi
            rZSimin1 = rZSi
        else: 
            f = interpolate.interp1d(zs.loc[(i-1):(i), "M-MgSiO3-H2O-5050"], zs.loc[(i-1):(i), "R-MgSiO3-H2O-5050"], kind='linear', assume_sorted=True)
            mu2 = f(mPlanet)
            break

    # Calculate sigma1
    sigma1 = (mu2-mu1)/3
    
    # Calculate the terrestrial probability
    p_ter = 0
    if rPlanet <= mu1:
        p_ter = 1
    elif rPlanet >= mu2:
        p_ter = 0
    else: # uses a pseudo-gaussian function
        p_ter = math.exp(-(0.5)*((rPlanet-mu1)/sigma1)**2)
    return p_ter


# In[4]:


# Data input
## Import exoplanet data from a CSV file into a pandas dataframe
exo = pd.read_csv (r'exoplanets_noKOI.csv', low_memory=False)

# Set the column with the header NAME to be used as an index to identify row 
exo = exo.set_index("NAME", drop = False)

# Extract names of planets as a list (to be used as a calling list)
exoList = pd.DataFrame(exo, columns=['NAME'])
exoList = exoList['NAME'].values.tolist()


# In[5]:


# Zeng-Sasselov boundaries input

## Import CSV of Zeng & Sasselov boundaries
zs = pd.read_csv (r'zsboundaries.csv')

## Set index using the RowNum column
zs = zs.set_index("RowNum", drop = False)

## Extract the column "RowNum" as a list (to be used as a calling list)
rowNum = pd.DataFrame(zs, columns=['RowNum'])
rowNum = rowNum['RowNum'].values.tolist()


# In[6]:


# Main subroutine to determine the habitability index value

habIndex = []
habIndexWithName = []
habIndexNotZero = []

for exoName in exoList:
    # Extract data of individual planets
    
    # HOST STAR PROPERTIES
    # Stellar radius (in solar radii)
    rStar = exo.loc[exoName, "RSTAR"]
    ## Convert to SI
    rStar = rStar*RSUN
    
    # Stellar temperature (in Kelvin)
    teffStar = exo.loc[exoName, "TEFF"]
    
    # Stellar luminosity
    luminosity = 4*math.pi*rStar*rStar*SB*teffStar**4
    
    # PLANET PROPERTIES   
    # Planetary radius (in Jovian radii)
    rPlanet = exo.loc[exoName, "R"]
    ## If R is not available, calculate it from  transit depth
    if math.isnan(rPlanet) == 1:
        depth = exo.loc[exoName, "DEPTH"]
        rPlanet = math.sqrt(depth)*rStar
    ## Convert to SI
    rPlanet = rPlanet*RJUP
    
    # Planetary mass (in Jovian masses)
    mPlanet = exo.loc[exoName, "MASS"] 
    ## If MASS is not available, calculate it from a common scaling law
    ### from the original HITE
    if math.isnan(mPlanet) == 1:
        if rPlanet/REARTH <= 1:
            mPlanet = ((rPlanet/REARTH)**3.268)*MEARTH
        elif rPlanet/REARTH > 1:
            mPlanet = ((rPlanet/REARTH)**3.65)*MEARTH
    ## Convert to SI
    mPlanet = mPlanet*MJUP
    
    # Surface planet gravity (in SI)
    surfGrav = BIGG*mPlanet/(rPlanet**2)    
    
    # ORBITAL PROPERTIES
    
    # Orbital eccentricity
    ecc = exo.loc[exoName, "ECC"]

    # Measurement uncertainty of orbital eccentricity    
    ## Upper bound (relative from E)
    eccUpRel = exo.loc[exoName, "ECCUPPER"]
    ### If measurement uncertainty is not available, assign it as 0.01
    if math.isnan(eccUpRel) == 1:
        eccUpRel = 0.01
    ### Upper bound (absolute)
    eccUpper = ecc + eccUpRel
    
    ## Lower bound (relative from E)
    eccLowRel = exo.loc[exoName, "ECCLOWER"]
    ### If measurement uncertainty is not available, assign it as 0.01
    if math.isnan(eccLowRel) == 1:
        eccLowRel = 0.01
    ###Lower bound (absolute)
    eccLower = ecc - eccLowRel
    
    # Orbital semi-major axis (in AU)
    semiAxis = exo.loc[exoName, "A"]      
    ## Convert to SI
    semiAxis = semiAxis*AU
    
    
    # Calculate the upper and lower bounds of F_OLR [...]
    ## that would allow for surface liquid water to exist
    pStar = PREF*math.exp(LH2O/(RGAS*TREF))
    # Upper bound: maximum F_OLR
    maxFlux = A*SB*(LH2O/(RGAS*math.log(pStar*math.sqrt(K0/(2*PLINE*surfGrav)))))**4
    # Lower bound: minimum F_OLR is the constant MINFLUX
    minFlux = MINFLUX
    
    # Probability of the planet being terrestrial
    p_ter = fp_ter(mPlanet,rPlanet,exoName)
        
    
    # Albedo (new)
    ## Boundaries
    albMin = ALBMINELSE
    albMax = ALBMAXELSE
    ## Special conditions
    ### For planets with M-type host star
    if teffStar >= 2300 and teffStar <=3800:
        albMax = ALBMAXM
    ### For planets with G-type host star
    elif teffStar >= 5370 and teffStar <=5980:
        albMin = ALBMING
        
        
    
    # Calculate F_OLR
    ## Albedo increments
    da = 0.01
    ## Eccentricity increments
    de = 0.01
    ## Sum of pofe (probability of eccentricity);
    ### (is used to normalize the index value, later)
    ### Initialized to 0
    pofeSum = 0
    ### Sum of how many instances of F_OLR meets the requirements for
    #### the planet to have surface liquid water. Each instances will then be
    #### multiplied by the probability of its eccentricity (pofe)
    ### Initialized to 0
    habFact = 0
    ### Incoming stellar radiation (instellation)
    flux0 = luminosity/(16*math.pi*semiAxis*semiAxis)

    # Calculate the habitability index
    ## Iterate through the albedo & eccentricity 2D matrix
    a = albMin
    while a < albMax:
        e = eccLower
        while e < eccUpper:
            flux = flux0*(1-a)/math.sqrt(1-e*e)
            pofeSum = pofeSum + pofe(e, ecc, eccUpRel)
            if flux < maxFlux and flux > MINFLUX:
                habFact = habFact + pofe(e, ecc, eccUpRel)
            e = e + de
        a = a + da   
    
    if ecc > 0.8:
        H = 0.0
    elif pofeSum != 0:
        H = (habFact/pofeSum)*p_ter
    else: # in the case of error; might be better to replace this with a throw exception statement
        H = 0.0
    
    habIndex.append(H)
    habIndexWithName.extend([exoName, ",", H])
    
    if H > 0:
        habIndexNotZero.extend([exoName+ ": "+str(H)])


# In[7]:


for i in habIndexNotZero:
    print(i)


# In[8]:


# Append the result (planet's name and index value) to a .txt file in the same folder 
#with open('out.txt','w') as f:
#    i = 1
#    for a in habIndexWithName:
#        if i == 3:
#            print(a, file=f)
#            i = 1
#        else:
#            print(a, file=f, end="")
#            i += 1

