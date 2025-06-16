#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 10:25:04 2024

@author: moli
"""


import os
import time
import glob
import scipy
import matplotlib
import numpy as np
from tqdm import tqdm
from scipy import fftpack
import matplotlib.cm as cm
import matplotlib.pyplot as plt



plt.rcParams['text.usetex'] = True
plt.rcParams['savefig.dpi'] = 300
plt.rc('xtick', labelsize=18)
plt.rc('ytick', labelsize=18)
plt.style.use('classic')


plt.close('all')



# =============================================================================
# 
# =============================================================================



results_dir = "/Users/moli/Document/Projet_CFD/NACA12/nacaAlphaRANS/results/V2"
pattern = os.path.join(
    results_dir,
    "alpha_*_postProcessing/forceCoeffs/0/coefficient.dat"
)
files = glob.glob(pattern)

alphas = []
CL_means = []
CD_means = []
LD_means = []

for coef_path in files:
    # Remonte 3 fois pour atterrir sur "alpha_m2_postProcessing"
    case_dir = os.path.basename(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(coef_path)
            )
        )
    )
    alpha_str = case_dir.replace("alpha_", "").replace("_postProcessing", "")
    # Conversion en nombre
    if alpha_str.startswith("m"):
        alpha = -int(alpha_str[1:])
    else:
        alpha = int(alpha_str.lstrip("p"))
    alphas.append(alpha)

    data = np.loadtxt(coef_path, comments="#")
    Cd = data[:, 1]
    Cl = data[:, 4]
    CD_means.append(Cd[-5:].mean())
    CL_means.append(Cl[-5:].mean())
    LD_means.append(Cl[-5:].mean() / Cd[-5:].mean())

# Tri par alpha
idx = np.argsort(alphas)
alphas = np.array(alphas)[idx]
CL_means = np.array(CL_means)[idx]
CD_means = np.array(CD_means)[idx]
LD_means = np.array(LD_means)[idx]


# Tracés
plt.figure(figsize=(7, 7))
plt.plot(alphas, CL_means, 'o-')
plt.xticks(fontsize=20); plt.yticks(fontsize=20);
plt.xlabel(r'$\alpha$', fontsize=26); plt.ylabel(r'$C_L$', fontsize=26); plt.grid()
# plt.title(r'$C_L~vs~\alpha$', fontsize=24)
plt.savefig('Figures/CL_vs_alpha.png', dpi=300, bbox_inches='tight')
plt.savefig('Figures/CL_vs_alpha.pdf', bbox_inches='tight')

plt.figure(figsize=(7, 7))
plt.plot(alphas, CD_means, 'o-')
plt.xticks(fontsize=20); plt.yticks(fontsize=20);
plt.xlabel(r'$\alpha$', fontsize=26); plt.ylabel(r'$C_D$', fontsize=26); plt.grid()
# plt.title(r'$C_D~vs~\alpha$', fontsize=24)
plt.savefig('Figures/CD_vs_alpha.png', dpi=300, bbox_inches='tight')
plt.savefig('Figures/CD_vs_alpha.pdf', bbox_inches='tight')

plt.figure(figsize=(7, 7))
plt.plot(alphas, LD_means, 'o-')
plt.xticks(fontsize=20); plt.yticks(fontsize=20);
plt.xlabel(r'$\alpha$', fontsize=26); plt.ylabel(r'$C_L/C_D$', fontsize=26); plt.grid()
# plt.title(r'$Efficience~C_L/C_D~vs~\alpha$', fontsize=24)
plt.savefig('Figures/CL_CD_vs_alpha.png', dpi=300, bbox_inches='tight')
plt.savefig('Figures/CL_CD_vs_alpha.pdf', bbox_inches='tight')





































