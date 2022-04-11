#!/usr/bin/env python
# coding: utf-8

# # Tutorial

# In[1]:


### Import necessary libraries
import pandas as pd
import math


# In[2]:


### Define constants
BIGG       = 6.67428e-11       # konstanta gravitasi
PI         = 3.1415926535
A          = 0.7344            # Pierrehumbert's Constant
SB         = 5.670373e-8       # Stefan-Boltzmann Constant
LH2O       = 2.425e6           # kapasitas kalor laten air
RGAS       = 461.5             # konstanta gas universal
PLINE      = 1e4               # ???
PREF       = 610.616           # ??? Reference Pressure
TREF       = 273.13            # ??? Reference Temperature
K0         = 0.055             # ???Constant in Runaway Greenhouse calculation
MEARTH     = 5.972186e24
REARTH     = 6378100
S0         = 1362              # Solar constant (daya yang diterima Bumi dari Matahari, dalam watt)
MSUN       = 1.988416e30
RSUN       = 6.957e8
LSUN       = 3.828e26
AUM        = 1.49598e11
HRSEC      = 3600
DAYSEC     = 86400
PPM        = 1e-6              # Parts per million

EMIN       = 0
EMAX       = 0.8
ALBMINELSE = 0.05
ALBMAXELSE = 0.8
ALBMING    = 0.25
ALBMAXM    = 0.35
MINFLUX    = 67

LINE       = 128
OPTLEN     = 24
MAXLINES   = 128

RJUP       = 7.1492e7
MJUP       = 1.8982e27
AU         = 1.496e11


# In[3]:


#### Define functions

### Probability distribution of eccentricity (from the original code, not used in M-HITE)
### pofe = probability of e
### def pofe(ecc):
    #### return 0.1619 - 0.5352*ecc + 0.6358*ecc*ecc - 0.2557*ecc**3

### Probability distribution of eccentricity (uses data from the exoplanet data file)
def mpofe(ecc,mu,sigma):
    return ((sigma*math.sqrt(2*math.pi))**(-1))*math.exp(-(((ecc-mu)**2)/(2*sigma**2)))/1000

### Zeng-Sasselov boundaries (digunakan oleh fpRocky)
def mzsrank(mPlanet,mZSi,mZSimin1):
    w = (mZSi - mZSimin1)/10
    i = 1
    while i < 10:
        mTest = mZSimin1 + i*w
        if mPlanet < mTest:
            rank = i
            print("rank",rank,"mPlanet",mPlanet,"mTest",mTest)
            break
        else:
            rank = i
            i = i + 1
    return rank

### Calculate probability of planet's rocky-ness/terrestriality
def fpRocky (mPlanet,rPlanet,exoName):
    mPlanet = mPlanet/MEARTH # Convert the unit to Earth's masses
    rPlanet = rPlanet/REARTH # Convert the unit to Earth's radii
    
    # Calculate mu1
    mu1 = 0
    mZSimin1 = 0
    rZSimin1 = 0
    for i in zsList:
        mZSi = zs.loc[i, "M-PureMgSiO3"]
        rZSi = zs.loc[i, "R-PureMgSiO3"]
        if mPlanet == mZSi:
            mu1 = rZSi
            break
        elif mZSi > mPlanet:
            mu1 = rZSimin1 + mzsrank(mPlanet,mZSi,mZSimin1)*(rZSi-rZSimin1)/10
            break
        else:
            mZSimin1 = mZSi
            rZSimin1 = rZSi # the loop won't stop until either of the two conditions above are satisfied 

    ### Calculate mu2
    mu2 = 0
    mZSimin1 = 0
    rZSimin1 = 0
    for i in zsList:
        mZSi = zs.loc[i, "M-MgSiO3-H2O-5050"]
        rZSi = zs.loc[i, "R-MgSiO3-H2O-5050"]
        if mPlanet == mZSi:
            mu2 = rZSi
            break
        elif mPlanet < mZSi:
            mu2 = rZSimin1 + mzsrank(mPlanet,mZSi,mZSimin1)*(rZSi-rZSimin1)/10
            break
        else:
            mZSimin1 = mZSi
            rZSimin1 = rZSi

    ### Calculate sigma1
    sigma1 = (mu2-mu1)/3
    
    pRocky = 0
    if rPlanet <= mu1:
        pRocky = 1
    elif rPlanet >= mu2:
        pRocky = 0
    else: # use the T_M_p function from SEPHI
        pRocky = math.exp(-(0.5)*((rPlanet-mu1)/sigma1)**2)
        
    return pRocky


# In[4]:


### Import exoplanet data from CSV into a pandas dataframe
exo = pd.read_csv (r'C:\Users\Zulfa\Documents\SPITE\exoplanetsInUse_noKOI1.csv', dtype={"UBIGOM":"str", "BIGOMURL":"str", "KOI":"str", "SEURL":"str", "SEDEPTHJREF":"str", "SEDEPTHJURL":"str", "USET":"str", "SETREF":"str", "SETURL":"str"})

### Set the column with the header NAME to be used as an index to identify row 
exo = exo.set_index("NAME", drop = False)

### Extract names of planets as a list (to be used as a calling list)
exoList = pd.DataFrame(exo, columns=['NAME'])
exoList = exoList['NAME'].values.tolist()


# In[5]:


### Import CSV of Zeng & Sasselov boundaries
zs = pd.read_csv (r'C:\Users\Zulfa\Documents\SPITE\zsboundaries.csv')

### Set index using the SORT column
zs = zs.set_index("SORT", drop = False)

### Extract the column "SORT" as a list (to be used as a calling list)
zsList = pd.DataFrame(zs, columns=['SORT'])
zsList = zsList['SORT'].values.tolist()


# In[6]:


habIndexList = []

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
    ### Maximum F_OLR
    fMax = A*SB*(LH2O/(RGAS*math.log(pStar*math.sqrt(K0/(2*PLINE*surfGrav)))))**4
    
    ### Maximum F_OLR (Fmin) is the constant MINFLUX

    
    ###### Probability of rocky-ness (new)
    pRocky = fpRocky(mPlanet,rPlanet,exoName)
        
    
    ###### Albedo (new)
    ### Boundaries
    albMin = ALBMINELSE
    albMax = ALBMAXELSE
    
    # Special conditions
    # For planets with M-type host star
    if teffStar >= 2300 and teffStar <=3800:
        albMin = ALBMINELSE
        albMax = ALBMAXM
    # For planets with G-type host star
    elif teffStar >= 5370 and teffStar <=5980:
        albmin = ALBMING     
        
    
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
            pofeSum = pofeSum + mpofe(e, ecc, eccUpRel)
            if flux < fMax and flux > MINFLUX:
                habFact = habFact + mpofe(e, ecc, eccUpRel)
            e = e + de
        a = a + da   
    
    if pofeSum != 0:
        H = (habFact/pofeSum)*pRocky
        H = str(H)
        habIndexList.append(H)
    elif ecc > 0.8:
        H = 0
        habIndexList.append(0)
    else:
        H = 0
        habIndexList.append(0)
        
    print("exoName",exoName,"H", H)
    
    
    


# In[7]:


print(habIndexList)


# In[8]:


with open('out.txt','w') as f:
    for a in habIndexList:
        print(a, file=f)


# In[ ]:




