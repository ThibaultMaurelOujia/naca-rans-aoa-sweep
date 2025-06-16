#!/usr/bin/env bash
 
set -euo pipefail     

# 1) Parametres
MESH_DIR="meshes"      
RESULTS_DIR="results"  
NPROCS=4 
SOLVER="rhoPimpleFoam"

# 2) Generer tous les maillages
#./batchMeshing.sh

# 3) Preparation dossier resultats
mkdir -p "${RESULTS_DIR}"

# 4) Boucle sur chaque maillage
for msh in ${MESH_DIR}/alpha_*.msh; do
    caseName=$(basename "${msh}" .msh)     
    echo -e "\n=== ${caseName} ==="

    # --- Nettoyage du case courant ---
    rm -rf processor* postProcessing constant/polyMesh

    # --- Conversion maillage ---
    gmshToFoam "${msh}"


    # constant/polyMesh/boundary
    BND="constant/polyMesh/boundary"
    awk 'BEGIN{c=0}
        /type[[:space:]]*patch;/ {
        if(c==0)      sub(/type[[:space:]]*patch;/,"type            empty;")
        else if(c==1) sub(/type[[:space:]]*patch;/,"type            wall;")
        c++
        }
        { print }
        ' "$BND" > "${BND}.tmp" && mv "${BND}.tmp" "$BND"


    renumberMesh -overwrite > /dev/null        # optionnel

    # --- Decomposition (parallele) ---
    decomposePar -force > /dev/null

    # --- Execution parallelisee ---
    LOG_FILE="${RESULTS_DIR}/${caseName}.log"
    echo "  → Calcul ${SOLVER} (log : ${LOG_FILE})"
    mpirun -np ${NPROCS} ${SOLVER} -parallel > "${LOG_FILE}" 2>&1

    # --- Sauvegarde resultats ---
    mv postProcessing "${RESULTS_DIR}/${caseName}_postProcessing"
    echo "  ✓ Termine, resultats deplaces."
done

echo -e "\nSweep complet : tous les postProcessing et logs sont dans '${RESULTS_DIR}/'"
