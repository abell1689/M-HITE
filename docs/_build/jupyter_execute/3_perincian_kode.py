#!/usr/bin/env python
# coding: utf-8

# # Perincian Kode

# ## **Libraries import declarations**
# ```python
# import pandas as pd
# import math
# from scipy import interpolate
# ```

# ## **Definition of constants and variables**
# 
# Some common physical constants, mainly used to calculate maxFlux (the upper bound of energy flux received by a planet that allows it to be habitable according to Pierrehumbert (2015)):
# 
# ```python
# BIGG       = 6.67428e-11       # Gravitational constant
# PI         = 3.1415926535
# A          = 0.7344            # Pierrehumbert's Constant
# SB         = 5.670373e-8       # Stefan-Boltzmann Constant
# LH2O       = 2.425e6           # Latent Heat Capacity of Water
# RGAS       = 461.5             # Universal Gas Constant
# PLINE      = 1e4               
# PREF       = 610.616           # Reference Pressure
# TREF       = 273.13            # Reference Temperature
# K0         = 0.055             # A constant in Runaway Greenhouse calculation
# ```
# 
# Boundaries for albedo values:
# 
# ```python
# ALBMINELSE = 0.05              # General lower bound
# ALBMAXELSE = 0.8               # General upper bound
# ALBMING    = 0.25              # Lower bound for planets orbiting G-type stars
# ALBMAXM    = 0.35              # Upper bound for planets orbiting M-type stars
# ```
# 
# The counterpart to maxFlux (unlike maxFlux, MINFLUX is a constant that does not depend on a planet's properties)
# ```python
# MINFLUX    = 67                
# ```
# 
# Definitions of units of measurement, mainly used to convert [exoplanet.org](exoplanet.org) data into SI units:
# 
# ```python
# MEARTH     = 5.972186e24       # Earth mass in kilograms
# REARTH     = 6378100           # Earth's radius in meters
# S0         = 1362              # Solar constant in watts per square meter
# MSUN       = 1.988416e30       # Solar mass in kilograms
# RSUN       = 6.957e8           # Solar radius in meters
# LSUN       = 3.828e26          # Solar luminosity in watts
# RJUP       = 7.1492e7          # Jovian radius in meters
# MJUP       = 1.8982e27         # Jovian mass in kilograms
# AU         = 1.496e11          # The astronomical unit in meters
# ```

# ## **Definition of functions**
# 
# ### **1) A function to calculate the probability distribution of orbital eccentricity**
# 
# #### **Original probability distribution of eccentricity (from the original code, not used in M-HITE). Note how it differs from the new one**
# 
# ```python
# pofe = 'probability of e'
# def pofe(ecc):
#     return 0.1619 - 0.5352*ecc + 0.6358*ecc*ecc - 0.2557*ecc**3
# ```
# 
# #### **New probability distribution of eccentricity**
# Unlike the original, this function uses known eccentricity data from [exoplanet.org](exoplanet.org), but retains the form of a probability distribution so it would still work with the algorithm   
# 
# ```python
# def pofe(ecc,mu,sigma):
#     return ((sigma*math.sqrt(2*math.pi))**(-1))*math.exp(-(((ecc-mu)**2)/(2*sigma**2)))/1000
# ```
# 
# ### **2) A function to calculate the probability of a planet's rocky-ness/terrestriality**
# 
# In both HITE and M-HITE, a planet's chance of **terrestriality** is determined by its **composition**. More 'rocky' means more terrestrial.
# 
# To predict a planet's **composition**, M-HITE uses a model developed by Zeng-Sasselov (ZS) (2013). This model treats the composition of planets as a three-pronged circular spectrum. assesses the overall density of a planet and then tries to place it in a three-pronged spectrum based on the likelihood of its composition: between 100% MgSiO<sub>3</sub>, 100% H<sub>2</sub>O, and 100% Fe. Only a narrow **range** in this spectrum gives a terrestriality chance of not zero: between 100% MgSiO<sub>3</sub> This density can be expressed as the ratio between a planet's mass and radius. A result of the In other words, for any given planetary mass, there is a probability distribution that dictates its chance of being terrestrial and this distribution is a function of the planet's radius.
# 
# --BOOKMARK fix statements about ZS
# 
# ![Terrestrial range of radius for a planet with a mass 3 times of Earth's mass](zeng-sasselov_1.png)
# 
# The plot above shows such a probability function T<sub>m<sub>planet</sub></sub>.
# Note that this particular function is specific to a planet with a mass of 3 Earth's masses (M<sub>🜨</sub>). Planets with different masses have different distributions.
# 
# For any planet, only a narrow **range** of radius values gives a terrestriality chance of not zero.
# In the plot above, the upper bound of that 'terrestrial range' is around 1.7 Earth's radii (R<sub>🜨</sub>), while the lower bound is not shown. This means that for any theoretically existing planets with a mass of 3 M<sub>🜨</sub>, if its radius is _more_ than 1.7 R<sub>🜨</sub> (the upper bound), then it is considered as non-terrestrial, and vice versa for the lower bound. On the other hand, if the radius of the planet falls within the terrestrial range, then its terrestriality chance is not zero. The actual probability value is then determined by interpolating inside an existing dataset from Zeng-Sasselov (2013) with the help of a pseudo-gaussian equation (note the shape of the above plot).
# 
# The purpose of the code in this section is: 1) to determine the upper and lower bounds of that narrow 'terrestrial range' for a given planet, and then, 2) to assess whether the planet could be considered as terrestrial or not.
# 
# In this program, the variable _mu1_ and _mu2_ represents the lower and upper bounds, respectively.
# 
# #### Calculation of the lower bound (_mu1_)
# 
# For any given planet of mass _M_, the lower bound of the 'terrestrial range' is defined as the radius that the planet would have if it was composed of pure MgSiO<sub>3</sub>. The Zeng-Sasselov (ZS) dataset table contains a list of mass values, each one mapped to a radius value so that each pair would describe a planet with the aforementioned composition. The values are stored in columns labeled 'M-Pure-MgSiO3' and 'R-Pure-MgSiO3', respectively, in units of Earth's masses and radii.
# 
# ![Inside the ZS table](zeng-sasselov_2.png)
# 
# For example, in this model, a planet with a mass of 0.00623 times of Earth's mass and a radius of 0.2029 times of Earth's radius is considered to be composed of 100 percent MgSiO<sub>3</sub>. Any theoretically existing planets with that exact mass would have 0.2029 Earth's radii as the lower bound of its 'terrestrial range'.
# 
# Let's say that we wish to find out this 'terrestrial lower bound' for exoplanet WASP-96 b (mass: 152.6 Earth's masses; radius 13.45 Earth's radii). This requires us to find out the radius of WASP-96 b if it were a planet of pure MgSiO<sub>3</sub>. 
# 
# Unfortunately, although the dataset is graphically algorithmic, it's not advisable to set up a simple regression equation to interpolate 
# 
# ![Logarithmic interpolation](zeng-sasselov_4.png)
# 
# using the ZS database because of the very large 
# --------BOOKMARK
# 
# We do this by using the ZS dataset table. Take into consideration the mass value of WASP-96 b, and then compare it to the values in the 'M-Pure-MgSiO3' column. If by chance, a value in the list is exactly 152.6, then we only have to look up its corresponding value in the 'R-Pure-MgSiO3' column, and that would be the terrestrial lower bound for WASP-96 b. It is more likely, though, that the mass value of a planet would fall _between_ the values in the list, so what we would get is a bracket that contains the planet's mass.  
# 
# ![Iterating through the ZS table to place WASP-96 b' mass inside the list](zeng-sasselov_3.png)
# 
# The picture above illustrates some steps of this process. Suppose we have already iterated through the first 43 rows and found out that the mass of WASP-96 b was not contained in any of the brackets formed by the previous values. We are currently comparing it to the mass value in the 44th row (140.3). Because 152.6 is still larger than 140.3, it means that our bracket of interest is _not_ the bracket formed by the value in the 44th row and its predecessor. Next, we compare it to the value in the 45th row (158.2). This value is larger than 152.6, meaning that the mass of WASP-96 b is contained between this row and its predecessor, meaning that this _is_ our bracket of interest.
# 
# The next step is to obtain the corresponding 'pure MgSiO<sub>3</sub>' radius value. We do this by using linear interpolation (this is different from the interpolation that would be used to obtain the exact terrestriality probability later).
# 
# --------BOOKMARK
# 
# #### Calculation of the upper bound (_mu2_)
# 
# Similar to that of _mu1_ but uses these columns of the ZS table instead: 'R-MgSiO3-H2O-5050' and 'M-MgSiO3-H2O-5050'.
# 
# #### Calculation of terrestriality probability
# 
# This part is fairly straightforward. We already have the lower and upper boundaries, and the only thing left to do is to compare them to the actual radius of the planet. If the planet's radius value falls outside of the confines of the boundaries, then the probability of terrestriality is considered to be zero. If the radius is within the boundaries, the probability is not zero and the exact value is determined through a pseudo-gaussian equation that makes use of both _mu1_ and _mu2_.
# 
# The function concludes with a return statement for the terrestriality probability value.
# 
# #### The code
# ```python
# # Start of the function definition
# def pRocky (mPlanet,rPlanet,exoName):
#     # Convert the unit to Earth's masses and radii
#     # (the Zeng-Sasselov dataset table uses Earth's mass and radius as the units) 
#     mPlanet = mPlanet/MEARTH 
#     rPlanet = rPlanet/REARTH
# 
#     # Calculate mu1, the lower bound of the 'not-zero chance' range
#     mu1 = 0.0       # initialize mu1 value
#     mZSimin1 = 0    # a temporary variable to hold a mass value from the ZS table
#     rZSimin1 = 0    # a temporary variable to hold a radius value from the ZS table
#     
#     # This conditional block tries to find the appropriate position for mPlanet within the list of 'pure MgSiO3' masses
#     for row in rowNum:                     # iterate through all the values in the table (barring a break statement)
#         mZSi = zs.loc[row, "M-PureMgSiO3"] # load a mass value from a row in the ZS table
#         rZSi = zs.loc[row, "R-PureMgSiO3"] # load the corresponding 'pure MgSiO3' radius from the same row
#         # This block compares mPlanet to the currently loaded mass value from the ZS table
#         if mPlanet == mZSi:                # if the values happen to be the same, then the lower bound is simply
#             mu1 = rZSi                     # ...the 'pure MgSiO3' radius that is mapped to the currently loaded mass value
#             break                          # get out of the 'for' loop
#         elif mPlanet > mZSi:               # if mPlanet is larger than the currently loaded mass value, it means we may have been...
#             mZSimin1 = mZSi                # ... not in the correct bracket yet
#             rZSimin1 = rZSi                # move the mass-radius values to these two variables
#             # The process would then go back up to the top of the 'for' block, assigning mZSi and rZSi with the next pair in the ZS list  
#         else:
#             # when mPlanet is finally smaller than the currently loaded mass value, it means we have found the correct bracket
#             # Now, what we have to do is interpolate the 'R-Pure-MgSiO3' value
#             # (we do not use the closest existing value in the ZS table because the gap between existing data points can be quite large...
#             # ... especially for larger masses) 
#             # The bracket we are in is divided into ten steps of equal width
#             f = interpolate.interp1d(zs.loc[(row-1):(row), "M-PureMgSiO3"], zs.loc[(row-1):(row), "R-PureMgSiO3"], kind='linear', assume_sorted=True)
#             mu1 = f(mPlanet)
#             break
#     print("mu1: ", mu1)
# 
#     ### Calculate mu2, the upper bound of the 'not-zero chance' range
#     ## for a given planetary mass, the upper bound is defined as the radius that the planet would have if it was composed of exactly half MgSiO3 and half H2O 
#     ## the procedure is similar to that for calculating mu1, but uses the 'M-MgSiO3-H2O-5050' and'R-MgSiO3-H2O-5050' columns in the ZS table
#     mu2 = 0.0
#     mZSimin1 = 0
#     rZSimin1 = 0
#     for i in rowNum:
#         mZSi = zs.loc[i, "M-MgSiO3-H2O-5050"]
#         rZSi = zs.loc[i, "R-MgSiO3-H2O-5050"]
#         if mPlanet == mZSi:
#             mu2 = rZSi
#             break
#         elif mPlanet > mZSi:
#             mZSimin1 = mZSi
#             rZSimin1 = rZSi
#         else: 
#             f = interpolate.interp1d(zs.loc[(row-1):(row), "M-MgSiO3-H2O-5050"], zs.loc[(row-1):(row), "R-MgSiO3-H2O-5050"], kind='linear', assume_sorted=True)
#             mu2 = f(mPlanet)
#             break
# 
#     ### Calculate sigma1
#     sigma1 = (mu2-mu1)/3
#     
#     pRocky = 0
#     if rPlanet <= mu1:
#         pRocky = 1
#     elif rPlanet >= mu2:
#         pRocky = 0
#     else: # use the T_M_p function from SEPHI
#         pRocky = math.exp(-(0.5)*((rPlanet-mu1)/sigma1)**2)
#         
#     return pRocky
# ```

# In[4]:


### Import exoplanet data from a CSV into a pandas dataframe
exo = pd.read_csv (r'exoplanetsInUse_noKOI1.csv', low_memory=False)

### Set the column with the header NAME to be used as an index to identify row 
exo = exo.set_index("NAME", drop = False)

### Extract names of planets as a list (to be used as a calling list)
exoList = pd.DataFrame(exo, columns=['NAME'])
exoList = exoList['NAME'].values.tolist()


# In[11]:


### Import CSV of Zeng & Sasselov boundaries
zs = pd.read_csv (r'zeng-sasselov_boundaries.csv')

### Set index using the RowNum column
zs = zs.set_index("RowNum", drop = False)

### Extract the column "RowNum" as a list (to be used as a calling list)
rowNum = pd.DataFrame(zs, columns=['RowNum'])
rowNum = rowNum['RowNum'].values.tolist()


# In[6]:


## Subroutine to determine Habitability Index value

habIndex = []
habIndexWithName = []

for exoName in exoList:
    #Extract data of individual planets
    
    #### HOST STAR PROPERTIES
    ### Stellar radius (in solar radii)
    rStar = exo.loc[exoName, "RSTAR"]
    # Convert to SI
    rStar = rStar*RSUN
    ### Stellar temperature (in Kelvin)
    teffStar = exo.loc[exoName, "TEFF"]
    ### Stellar luminosity
    luminosity = 4*math.pi*rStar*rStar*SB*teffStar**4
    
    ###### PLANET PROPERTIES   
    ### Planetary radius (in Jovian radii)
    rPlanet = exo.loc[exoName, "R"]
    # If Rp is not available, calculate it from  transit depth
    if math.isnan(rPlanet) == 1:
        depth = exo.loc[exoName, "DEPTH"]
        rPlanet = math.sqrt(depth)*rStar
    # Convert to SI
    rPlanet = rPlanet*RJUP
    ### Planetary mass (in Jovian masses)
    mPlanet = exo.loc[exoName, "MASS"] 
    # If Mp is not available, calculate it from a common scaling law, [...]
    # using Rp
    if math.isnan(mPlanet) == 1:
        if rPlanet/REARTH <= 1:
            mPlanet = ((rPlanet/REARTH)**3.268)*MEARTH
        elif rPlanet/REARTH > 1:
            mPlanet = ((rPlanet/REARTH)**3.65)*MEARTH
    # Convert to SI
    mPlanet = mPlanet*MJUP
    ### Surface planet gravity (in SI)
    surfGrav = BIGG*mPlanet/(rPlanet**2)    
    
    
    
    ###### Orbital properties
    ### Orbital eccentricity
    ecc = exo.loc[exoName, "ECC"]
    ### Measurement uncertainty of orbital eccentricity    
    # Upper bound (relative from E)
    eccUpRel = exo.loc[exoName, "ECCUPPER"]
    # If measurement uncertainty is not available, assign it as 0.01
    if math.isnan(eccUpRel) == 1:
        eccUpRel = 0.01
    # Upper bound (relative from E)
    eccUpper = ecc + eccUpRel
    # Lower bound (relative from E)
    eccLowRel = exo.loc[exoName, "ECCLOWER"]
    # If measurement uncertainty is not available, assign it as 0.01
    if math.isnan(eccLowRel) == 1:
        eccLowRel = 0.01
    # Lower bound (absolute)
    eccLower = ecc - eccLowRel
    ### Orbital semi-major axis (in AU)
    semiAxis = exo.loc[exoName, "A"]      
    # Convert to SI
    semiAxis = semiAxis*AU
    
    
    ###### Calculate the upper and lower bounds of F_OLR [...]
    ###### that would allow for surface liquid water to exist
    ### lupa apa
    pStar = PREF*math.exp(LH2O/(RGAS*TREF))
    ### Upper bound: maximum F_OLR
    maxFlux = A*SB*(LH2O/(RGAS*math.log(pStar*math.sqrt(K0/(2*PLINE*surfGrav)))))**4
    ### Lower bound: minimum F_OLR is the constant MINFLUX

    
    ###### Probability of rocky-ness (new)
    pRocky = pRocky(mPlanet,rPlanet,exoName)
        
    
    ###### Albedo (new)
    ### Boundaries
    albMin = ALBMINELSE
    albMax = ALBMAXELSE
    
    # Special conditions
    # For planets with M-type host star
    if teffStar >= 2300 and teffStar <=3800:
        albMax = ALBMAXM
    # For planets with G-type host star
    elif teffStar >= 5370 and teffStar <=5980:
        albMin = ALBMING
        
        
    
    ###### Calculate F_OLR
    ### Albedo increments
    da = 0.01
    ### Eccentricity increments
    de = 0.01
    ### Sum of pofe (probability of eccentricity);
    ### is used to normalize the index value, later)
    pofeSum = 0
    ### How many instances of F_OLR meets the requirements for [...]
    ### the planet to have surface liquid water? Each instances would be [...]
    ### multiplied by the probability of that value of F_OLR from occuring
    habFact = 0
    ### Incoming stellar radiation (instellation)
    flux0 = luminosity/(16*math.pi*semiAxis*semiAxis)

    ### Calculate H
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
        H = (habFact/pofeSum)*pRocky
    else: # for error case
        H = 0.0
    
    habIndex.append(H)
    habIndexWithName.extend([exoName, ",", H])
    
        
    print(exoName, H)
    
    


# In[7]:


# print(sum(habIndexList)/len(habIndexList)) #0.002815606263929704
# print(habIndexList)
print(sum(habIndex)/len(habIndex))


# In[8]:


with open('out.txt','w') as f:
    i = 1
    for a in habIndexWithName:
        if i == 3:
            print(a, file=f)
            i = 1
        else:
            print(a, file=f, end="")
            i += 1


# In[6]:


print(0.48 * MJUP/MEARTH, ",", 1.2 * RJUP/REARTH)


# In[14]:


print(pRocky (152.56323229048795,13.450776877126417,"WASP-96 b"))


# In[ ]:




