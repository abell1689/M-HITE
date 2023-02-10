# Lampiran B: Program HITE Orisinal

## 1. Pendahuluan
Program HITE orisinal ditulis dalam bahasa pemrograman C.
HITE diperuntukkan bagi planet yang ditemukan menggunakan dengan metode transit, yaitu pengamatan atas meredupnya cahaya bintang secara periodik, yang disebabkan oleh adanya eksoplanet yang melintas di depan bintang dan menghalangi sebagian cahaya untuk sampai di teleskop. 
https://www.youtube.com/watch?v=8v4SRfmoTuU
## 2. Data masukan
Data masukan yang diperlukan adalah berupa *transit observables*, yaitu data fisis yang dapat diketahui mengenai benda langit jika benda tersebut diamati saat sedang transit (melintas di depan sumber cahaya). Dalam hal ini, benda langitnya adalah planet, dan sumber cahayanya adalah bintang inang yang diorbit oleh planet tersebut.
Data masukan ini disimpan dalam berkas *plain text* dengan ekstensi  `.in`.
### Contoh
Berkas `earth.in` yang berisikan *transit observables* planet Bumi jika (disimulasikan) diamati saat sedang transit di depan Matahari 
```
NumPlanets	3

StellarLogG 	4.43812
StellarRadius	1.0
StellarTemp	5771.8

BodyPos		1
TransitDepth	82.9
Period		365.25
Duration	13.09
ImpactParam	0

BodyPos		2
TransitDepth	74.8
Period		225
Duration	11.14
ImpactParam	0

BodyPos		3
TransitDepth	23.5
Period		686.971
Duration	16.182
ImpactParam	0
```
#### Penjelasan:
`NumPlanets` adalah jumlah planet yang dideskripsikan dalam berkas ini, bisa bernilai `1` atau `3 `. Nilai `1` berarti berkas masukan hanya berisi data transit planet yang indeks kelayakhuniannya sedang dicari (dalam contoh ini, Bumi). Jika nilainya `3`, berarti berkas ini memuat data transit planet yang indeks kelayakhuniannya sedang dicari *serta* dua planet yang orbitnya mengapit orbit planet itu (dalam contoh ini, Bumi serta Mars dan Venus).
HITE orisinal tidak mewajibkan ada 3 data planet, tapi menganjurkannya untuk tata bintang dengan lebih dari satu planet demi penghitungan nilai indeks yang lebih akurat (lihat [Barnes *et al*. 2013 bagian 2.2 & 2.3] untuk penjelasan lebih lanjut).

`StellarLogG` adalah percepatan gravitasi di permukaan bintang inang (misal, dinotasikan sebagai *G*) dalam satuan *cgs* (*cm/s^2*), yang kemudian diubah ke dalam bentuk logaritmanya, log *G* (basis 10).

`StellarRadius` adalah jari-jari bintang inang dalam satuan kelipatan jari-jari Matahari (*Solar radius* = 6,955 × 10^8 meter).

`StellarTemp` adalah temperatur bintang inang dalam satuan kelvin.

`BodyPos` digunakan untuk menandakan planet mana yang sedang dihitung indeks kelayakhuniannya, dan planet mana yang 'mengapitnya'.
`BodyPos` bernilai `1` untuk planet yang sedang dihitung indeks kelayakhuniannya, bernilai `2` untuk planet yang orbitnya berada sebelum orbit planet `1` (lebih dekat ke bintangnya), dan bernilai 3 untuk planet yang orbitnya berada setelah orbit planet `1` (lebih jauh dari bintangnya). Jadi pada contoh ini, data yang berada di bawah `BodyPos 1` adalah data Bumi, yang di bawah `BodyPos 2`adalah Venus, yang dibawah dan `BodyPos 3` adalah Mars.
Jika `NumPlanets` bernilai `1`,  yang diperlukan hanya `BodyPos 1` . 

`TransitDepth` adalah besaran fraksional yang mengukur besar peredupan fluks bintang saat fenomena transit, relatif terhadap fluks normal bintang. 

![](transit_depth.jpg)
![](andrew_vandenburg_transit_depth.png)
Hak Cipta: NASA Ames, lisensi [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

`Period` adalah *transit period*, atau waktu yang dibutuhkan eksoplanet untuk melakukan satu revolusi pada orbitnya, diminta dalam satuan hari. 

`ImpactParam` menyatakan seberapa dekat planet dengan pusat bintang saat transit (berkaitan dengan kemiringan bidang orbit eksoplanet terhadap posisi Bumi), dinyatakan dalam satuan SI (meter).

## 3. Anotasi kode program
Kode program HITE orisinal bisa diperoleh dari [laman proyek HITE di Github](https://github.com/RoryBarnes/HITE).  Bagian ini akan memberikan anotasi singkat tentang bagian-bagian program dengan harapan bisa mempermudah pemahaman kode di awal, bersama dengan komentar dari penyusun yang sudah cukup mendetail.
### Header
```C
/**********************************************************
 * hite.c -- Habitability Index for Transiting Exoplanets *
 *                                                        *
 * Rory Barnes                                            *
 *                                                        *
 * Wed May 20 14:59:41 PDT 2015                           *
 * Updated Fri Sep  4 15:42:30 PDT 2015 to include log(g) *
 *                                                        *
 * This code calculate the habitability index for         *
 * transiting potentially habitable planets as described  *
 * in Barnes et al. (2015).                               *
 *                                                        *
 **********************************************************/
```

### Deklarasi library C yang dibutuhkan
```C
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
```

### Definisi konstanta
```C
#define BIGG       6.67428e-11       // Gravitation Constant
#define PI         3.1415926535
#define A          0.7344            // Pierrehumbert's Constant
#define SB         5.670373e-8       // Stefan-Boltzmann Constant
#define LH2O       2.425e6           // Latent Heat Capacity of Water
#define RGAS       461.5             // Universal Gas Constant
#define PLINE      1e4               // Pressure at which line are evaluated
#define PREF       610.616           // Reference Pressure
#define TREF       273.13            // Reference Temperature
#define K0         0.055             // Constant in Runaway Greenhouse calculation
#define MEARTH     5.972186e24
#define REARTH     6378100
#define S0         1362              // Solar Constant
#define MSUN       1.988416e30
#define RSUN       6.957e8
#define LSUN       3.828e26
#define AUM        1.49598e11
#define HRSEC      3600
#define DAYSEC     86400
#define PPM        1e-6              // Parts per million

#define EMIN       0
#define EMAX       0.8
#define ALBMIN     0.05
#define ALBMAX     0.8
#define MINFLUX    67

#define LINE       128
#define OPTLEN     24
#define MAXLINES   128
```

### Deklarasi struktur data untuk menampung data planet (BODY)
```C
typedef struct {
  int iPos;            // Position. 0 = star, 1 = PH, 2 = inner, 3 = outer 
  int iConstraint;     // Which HZ constrains? 0=both,-1=inner,1=outer 

  double dDepth;       // Transit depth
  double dImpact;      // Impact parameter
  double dDuration;    // Transit duration
  double dPeriod;      // Orbital period

  double dMass;        // Stellar mass
  double dRadius;      // Stellar radius
  double dGrav;        // Planet's gravitational acceleration
  double dEmin;        // Minimum eccentricity from transit data
  double dEmax;        // Maximum eccentricity from Hill stability
  double dSemi;        // Semi-major axis
  double dTDA;         // Transit Duration Anomoly
  double dCircDur;     // Transit duration if circular orbit
  double dFmax;        // Maximum allowable absorbed stellar energy
  double dProcky;      // Probability the planet is rocky
  double dSeff;        // Incident stellar energy, Earth units
  double dHabFact;     // HITE prime value (no ecc. constraints)
  double dHabFactEcc;  // HITE value (with eccentricity constraints)

  double dTemp;        // Stellar effective temperature
  double dLuminosity;  // Stellar luminosity
  double dLog_g;       // Stellar log(g)
}
BODY;
```

### Deklarasi struktur data untuk menampung data jumlah planet (OPTIONS)
```C
typedef struct {
  int iNumPl;
}
OPTIONS;
```

### Algoritma untuk membaca berkas masukan `.in`
#### a. Fungsi-fungsi untuk memvalidasi berkas masukan
Berkas masukan bisa memuat komentar yang diawali dengan `#`. Komentar akan diabaikan oleh program dengan memanfaatkan fungsi di bawah ini yang akan mengecek apakah ada tanda `#` dalam berkas.
```C
/************* Options functions **********************/

/* Is the first non-white space a #? If so, return 1 */
int CheckComment(char cLine[]) {
  int iPos;

  for (iPos=0;iPos<LINE;iPos++) {
    if (!isspace(cLine[iPos])) {
      if (cLine[iPos] == 35)
        return 1;
      else
	return 0;
    }
  }

  // Shouldn't get here, but line didn't start with a #
  return 0;
}
```

Fungsi untuk mengecek keberadaan whitespace dalam berkas masukan
```C
int CheckSpace(char cLine[]) {
  int iPos,bBlank=0;

  for (iPos=0;iPos<LINE;iPos++) {
    if (!isspace(cLine[iPos]) && cLine[iPos] != '\0') {
      return 0;     
    }
  } 

  return 1;
}
```
Kedua fungsi di atas akan dipanggil dalam subrutin di bawah.

#### b. Membaca berkas...
```C
/* Recursively call to get the next line that does not begin with 
   comment or white space. */
void GetLine(char cFile[MAXLINES][LINE],int *iLine) {
  int iLen;

  if (CheckComment(cFile[*iLine]) || CheckSpace(cFile[*iLine])) {
    (*iLine)++;
    GetLine(cFile,iLine);
  }
}

void NegativeExit(char cOption[],int iLine) {
  fprintf(stderr,"ERROR: Option %s cannot be negative.\n",cOption);
  fprintf(stderr,"\tLine: %d\n",iLine+1);
  exit(1);
}

void CheckOption(char cInput[],char cOption[],int iLine) {

  if (memcmp(cInput,cOption,strlen(cOption)+1)) {
    fprintf(stderr,"ERROR: Expected option %s, found option %s.\n",cOption,cInput);
    fprintf(stderr,"\tLine: %d\n",iLine+1);
    exit(1);
  }
}

double ReadOptionDouble(char cFile[MAXLINES][LINE],char cOption[],double dUnit,int *iLine) {
  double dOption;
  char cInput[OPTLEN],cArg[OPTLEN];

  /* Get the next line non-space, non-comment line. iLine keeps track of the 
     line number. */
  GetLine(cFile,iLine);

  // Get the first two arguments
  sscanf(cFile[*iLine],"%s %s",cInput,cArg);

  // Make sure the first argument is an exact match to expected option
  CheckOption(cInput,cOption,*iLine);

  // Convert second option into double and assign to proper place
  dOption = atof(cArg);

  // Make sure option is not negative.
  if (dOption < 0)
    NegativeExit(cOption,*iLine);

  // Convert to system units (SI)
  dOption *= dUnit;

  // Increment the line number
  (*iLine)++;
  
  return dOption;
}

int ReadOptionInt(char cFile[MAXLINES][LINE],char cOption[],int *iLine) {
  int iOption;
  char cInput[OPTLEN],cArg[OPTLEN];

  GetLine(cFile,iLine);
  sscanf(cFile[*iLine],"%s %s",cInput,cArg);
  CheckOption(cInput,cOption,*iLine);
  iOption = atoi(cArg);
  if (iOption <= 0)
    NegativeExit(cOption,*iLine);
  (*iLine)++;

  return iOption;
}


void ReadOptions(BODY *body,OPTIONS *options, char infile[]) {
  
  /* HITE demands a specific order of inputs, but white space
     and all characters after a # are ignored. */
  char *cTmp,cFile[MAXLINES][LINE];
  FILE *fp;
  int iLine=0;
  size_t iLen;

  fp = fopen(infile,"r");
```
Membaca berkas ....
```C
  /* Fill cFile with all the lines from the input file. */
  //getline(&cTmp,&iLen,fp);
  while (getline(&cTmp,&iLen,fp) != -1) {
    strcpy(cFile[iLine++],cTmp);
    //iLine++;
  }

  iLine=0;
  options->iNumPl = ReadOptionInt(cFile,"NumPlanets",&iLine);

  body[0].dLog_g = ReadOptionDouble(cFile,"StellarLogG",1,&iLine);
  body[0].dRadius = ReadOptionDouble(cFile,"StellarRadius",RSUN,&iLine);
  body[0].dTemp = ReadOptionDouble(cFile,"StellarTemp",1,&iLine);

  body[1].iPos = ReadOptionInt(cFile,"BodyPos",&iLine);
  body[1].dDepth = ReadOptionDouble(cFile,"TransitDepth",PPM,&iLine);
  body[1].dPeriod = ReadOptionDouble(cFile,"Period",DAYSEC,&iLine);
  body[1].dDuration = ReadOptionDouble(cFile,"Duration",HRSEC,&iLine);
  body[1].dImpact = ReadOptionDouble(cFile,"ImpactParam",1,&iLine);

  if (options->iNumPl > 1) {
    body[2].iPos = ReadOptionInt(cFile,"BodyPos",&iLine);
    body[2].dDepth = ReadOptionDouble(cFile,"TransitDepth",PPM,&iLine);
    body[2].dPeriod = ReadOptionDouble(cFile,"Period",DAYSEC,&iLine);
    body[2].dDuration = ReadOptionDouble(cFile,"Duration",HRSEC,&iLine);
    body[2].dImpact = ReadOptionDouble(cFile,"ImpactParam",1,&iLine);
    
    if (options->iNumPl > 2) {
      body[3].iPos = ReadOptionInt(cFile,"BodyPos",&iLine);
      body[3].dDepth = ReadOptionDouble(cFile,"TransitDepth",PPM,&iLine);
      body[3].dPeriod = ReadOptionDouble(cFile,"Period",DAYSEC,&iLine);
      body[3].dDuration = ReadOptionDouble(cFile,"Duration",HRSEC,&iLine);
      body[3].dImpact = ReadOptionDouble(cFile,"ImpactParam",1,&iLine);
    }
  }

  fclose(fp);

}
```
Subrutin berisi algoritma untuk menghitung nilai indeks planet
```
/**************** Habitability Factor Subroutines **********/

void GetRadius(BODY *body,int iNumPl) {
  int iBody;

  for (iBody=1;iBody<=iNumPl;iBody++) 
    body[iBody].dRadius=sqrt(body[iBody].dDepth)*body[0].dRadius;
}

void GetMass(BODY *body,int iNumPl) {
  int iBody;

  // Stellar Mass
  body[0].dMass = pow(10,body[0].dLog_g)*body[0].dRadius*body[0].dRadius/BIGG/100;

  for (iBody=1;iBody<=iNumPl;iBody++) {
    if (body[iBody].dRadius/REARTH < 1)
      body[iBody].dMass = pow(body[iBody].dRadius/REARTH,3.268)*MEARTH;
    else if (body[iBody].dRadius/REARTH >= 1 && body[iBody].dRadius/REARTH < 2.5)
      body[iBody].dMass =  pow(body[iBody].dRadius/REARTH,3.65)*MEARTH;
    else 
      body[iBody].dMass = (4*PI/3)*1000*pow(body[iBody].dRadius,3);
  }
}

void GetGrav(BODY *body) {
  body->dGrav = BIGG*body->dMass/pow(body->dRadius,2);
}

void GetSemis(BODY *body,int iNumPl) {
  int iBody;

  for (iBody=1;iBody<=iNumPl;iBody++)
    body[iBody].dSemi = pow(BIGG*(body[0].dMass+body[iBody].dMass)/(4*PI*PI)*body[iBody].dPeriod*body[iBody].dPeriod,(1.0/3));
}

void GetTDAs(BODY *body,int iNumPl) {
 int iBody;
 double dCircDur;

 for (iBody=1;iBody<=iNumPl;iBody++) {
   body[iBody].dCircDur =   sqrt((1 - body[iBody].dImpact*body[iBody].dImpact)*pow((body[0].dRadius+body[iBody].dRadius),2))*body[iBody].dPeriod/(PI*body[iBody].dSemi);
   body[iBody].dTDA = body[iBody].dDuration/body[iBody].dCircDur;
 }
}

void GetEmins(BODY *body,int iNumPl) {
  int iBody;

  for (iBody=1;iBody<=iNumPl;iBody++)
    body[iBody].dEmin = fabs( (body[iBody].dTDA*body[iBody].dTDA - 1)/(body[iBody].dTDA*body[iBody].dTDA + 1) );
}

double dHillEmax(double gamma[2],double lambda,double mu[2],double zeta) {
  double dArg1,dArg2,dArg3;

  dArg1 = 1 + pow(3,(4./3))*(mu[0]*mu[1]/pow(zeta,(4./3)));

  dArg2 = pow(zeta,3)/(mu[0] + (mu[1]/(lambda*lambda)));

  dArg3 = mu[1]*gamma[1]*lambda;

  gamma[0] = (1/mu[0])*(sqrt(dArg1*dArg2) - dArg3);

  if (fabs(gamma[0]) > 1) // System is Hill unstable 
    return -1;
  else 
    return sqrt(1 - gamma[0]*gamma[0]);
}

void GetEmax(BODY *body,int iNumPl) {
  double mu[2],zeta,gamma[2],lambda,dTotMass;
  double emax;

  if (iNumPl > 1) {
    dTotMass = body[0].dMass + body[1].dMass + body[2].dMass;
    mu[0] = body[1].dMass/body[0].dMass;
    mu[1] = body[2].dMass/body[0].dMass;
    zeta = mu[0]+mu[1];
    gamma[1] = sqrt(1-body[2].dEmin*body[2].dEmin);
    if (body[2].iPos == 2) // inner planet
      lambda = sqrt(body[1].dSemi/body[2].dSemi);
    else
      lambda = sqrt(body[2].dSemi/body[1].dSemi);

    body[1].dEmax = dHillEmax(gamma,lambda,mu,zeta);
    
    if (iNumPl == 3) {
      mu[1] = body[3].dMass/body[0].dMass;
      zeta = mu[0] + mu[1];
      gamma[1] = sqrt(1-body[3].dEmin*body[3].dEmin);
      if (body[3].iPos == 2) // inner planet
	lambda = sqrt(body[1].dSemi/body[3].dSemi);
      else
	lambda = sqrt(body[3].dSemi/body[1].dSemi);
      
      emax = dHillEmax(gamma,lambda,mu,zeta);
      
      if (emax < body[1].dEmax)
	body[1].dEmax = emax;
    }
  } else
    body[1].dEmax = EMAX;
}

void GetLuminosity(BODY *body) {
  body->dLuminosity = 4*PI*body->dRadius*body->dRadius*SB*pow(body->dTemp,4);
}

void GetFmax(BODY *body) {
  double pstar;

  pstar = PREF*exp(LH2O/(RGAS*TREF));

  body->dFmax = A*SB*pow(LH2O/(RGAS*log(pstar*sqrt(K0/(2*PLINE*body->dGrav)))),4);
}

void GetInstellation(BODY *body) {
  body[1].dSeff = body[0].dLuminosity/(4*PI*body[1].dSemi*body[1].dSemi);
}

double pofe(double e) {
  return 0.1619 - 0.5352*e + 0.6358*e*e - 0.2557*pow(e,3);
}

double procky(double dRadius) {
  if (dRadius/REARTH > 2.5)
    return 0;
  if (dRadius/REARTH > 1.5) 
    return 2.5 - dRadius/REARTH;

  return 1;
}

double ScanEccAlb(BODY *body,double dEmin,double dEmax) {
  double a,e,da,de;
  double flux,flux0,dHabFact=0,dTot=0;
  int bIHZ=0,bOHZ=0;

  if (dEmax < 0 || dEmin > dEmax)
    return 0;
  
  da=0.01;
  de=0.01;

  flux0=body[0].dLuminosity/(16*PI*body[1].dSemi*body[1].dSemi);

  for (a=ALBMIN;a<=ALBMAX;a+=da) {
    for (e=dEmin;e<=dEmax;e+=de) {
      flux = flux0*(1-a)/sqrt(1-e*e);
      dTot += pofe(e);
      if (flux < body[1].dFmax && flux > MINFLUX) 
	dHabFact += pofe(e);
      if (flux > body[1].dFmax)
	bIHZ=1;
      if (flux < MINFLUX)
	bOHZ=1;
    }
  }
  if (!bIHZ && !bOHZ)
    body[1].iConstraint = 0;
  if (bIHZ)
    body[1].iConstraint = 1;
  if (bOHZ)
    body[1].iConstraint = 2;
  if (bIHZ && bOHZ)
    body[1].iConstraint = 3;

  return (dHabFact/dTot)*body[1].dProcky;
}

void HabFact(BODY *body,OPTIONS options) {
  int iBody;

  GetRadius(body,options.iNumPl);
  GetMass(body,options.iNumPl);
  GetGrav(&body[1]);
  GetSemis(body,options.iNumPl);
  GetTDAs(body,options.iNumPl);
  GetEmins(body,options.iNumPl);
  GetEmax(body,options.iNumPl);
  GetFmax(&body[1]);
  GetLuminosity(&body[0]);
  GetInstellation(body);
  body[1].dProcky = procky(body[1].dRadius);

  // HabFact without any constraints on e
  body[1].dHabFact = ScanEccAlb(body,EMIN,EMAX);

  /* Now apply eccentricity constraints. If the computed value of e_max
     is greater than the range to be scanned (set by EMAX), then use EMAX
     as the largest e to be tested. */
  if (body[1].dEmax < EMAX) 
    body[1].dHabFactEcc = ScanEccAlb(body,body[1].dEmin,body[1].dEmax);
  else
    body[1].dHabFactEcc = ScanEccAlb(body,body[1].dEmin,EMAX);
}

void WriteOutput (BODY *body,OPTIONS options) {
  int iBody;
  FILE *fp;

  fp = fopen("hite.out","w");

  // Habitability Factors
  fprintf(fp,"Habitability Index (w/o ecc): %f\n",body[1].dHabFact);
  fprintf(fp,"Habitability Index (w ecc): %f\n",body[1].dHabFactEcc);

  // Stellar properties
  fprintf(fp,"\nStellar log(g) [g/cm^2]: %f\n",body[0].dLog_g);
  fprintf(fp,"Stellar Radius [solar]: %f\n",body[0].dRadius/RSUN);
  fprintf(fp,"Stellar Effective Temp [K]: %f\n",body[0].dTemp);
  fprintf(fp,"Stellar Mass [solar]: %f\n",body[0].dMass/MSUN);
  fprintf(fp,"Stellar Luminosity [solar]: %f\n",body[0].dLuminosity/LSUN);
  fprintf(fp,"Number of Planets: %d\n",options.iNumPl);

  for (iBody=1;iBody<=options.iNumPl;iBody++) {
    fprintf(fp,"\nPosition: %d\n",body[iBody].iPos);
    fprintf(fp,"Depth [ppm]: %f\n",body[iBody].dDepth/PPM);
    fprintf(fp,"Transit Duration [hour]: %f\n",body[iBody].dDuration/HRSEC);
    fprintf(fp,"Impact Parameter: %f\n",body[iBody].dImpact);
    fprintf(fp,"Period [days]: %f\n",body[iBody].dPeriod/DAYSEC);

    fprintf(fp,"Radius [Earth]: %f\n",body[iBody].dRadius/REARTH);
    fprintf(fp,"Mass [Earth]: %f\n",body[iBody].dMass/MEARTH);
    fprintf(fp,"Semi-Major Axis [AU]: %f\n",body[iBody].dSemi/AUM);
    fprintf(fp,"Circular Duration [hour]: %f\n",body[iBody].dCircDur/HRSEC);
    fprintf(fp,"Transit Duration Anomoly: %f\n",body[iBody].dTDA);
    fprintf(fp,"Minimum Eccentricity: %f\n",body[iBody].dEmin);
    if (iBody == 1) {
      fprintf(fp,"Planet's Gravity [m/s^2]: %f\n",body[iBody].dGrav);
      fprintf(fp,"Maximum Eccentricity: %f\n",body[iBody].dEmax);
      fprintf(fp,"Maximum Flux [W/m^2]: %f\n",body[iBody].dFmax);
      fprintf(fp,"Circular Instellation [Earth]: %f\n",body[1].dSeff/S0);
      fprintf(fp,"Flux Constraint: ");
      if (body[1].iConstraint == 0)
	fprintf(fp,"None");
      if (body[1].iConstraint == 1)
	fprintf(fp,"Maximum");
      if (body[1].iConstraint == 2)
	fprintf(fp,"Minimum");
      if (body[1].iConstraint == 3)
	fprintf(fp,"Both");
      fprintf(fp,"\n");
    }
  }
  fclose(fp);
}  

int main(int argc, char **argv) {
  BODY *body;
  OPTIONS options;

  if (argc != 2) {
    fprintf(stderr,"Usage: %s inputfile\n",argv[0]);
    exit(1);
  }

  body=malloc(4*sizeof(BODY));
  ReadOptions(body,&options,argv[1]);

  HabFact(body,options);

  WriteOutput(body,options);

  exit(0);
}

```