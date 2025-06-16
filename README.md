# naca-rans-aoa-sweep

Mini-benchmark **OpenFOAM v2412** : profil **NACA 0012**  
- c = 1.0 m (corde)  
- m = 0.02 (cambrure max)  
- p = 0.4 (position cambrure)  
- t = 0.12 (épaisseur relative)  

Inlet velocity: **100 m/s (Ma ≈ 0,3)**, angles d’attaque **–5 ° → 20 °**, RANS k-ω.


`alpha-naca.geo` – géométrie NACA  
`batchMeshing.sh` – génération maillage  
`runSweep.sh` – boucle angles  
`plot_polar.py` – tracé polaire  
