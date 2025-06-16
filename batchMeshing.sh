BASE_GEO="alpha-naca.geo"          # geo maitre
OUT_DIR="meshes"                   # dossier de sortie

mkdir -p "${OUT_DIR}"

for deg in $(seq -5 1 20); do 
    negdeg=$(( -deg ))
    alpha_expr="${negdeg}*Pi/180"

    #fname=$(printf "alpha_%+02d" "$deg" | tr '+-' 'p-')
    if [ "$deg" -lt 0 ]; then
        prefix="m${deg#-}"
    else
        prefix="p${deg}"
    fi
    fname="alpha_${prefix}"
    geo_tmp="${OUT_DIR}/${fname}.geo"
    msh_out="${OUT_DIR}/${fname}.msh"

    cp "${BASE_GEO}" "${geo_tmp}"
    #sed -i '' -E "s/^alpha *=.*;/alpha = ${alpha_expr};/" "${geo_tmp}"
    sed -i '' -E "s|^alpha *=.*;|alpha = ${alpha_expr};|" "${geo_tmp}"

    echo "↳ α = ${deg}°  →  ${msh_out}"
    gmsh -3 -format msh2 "${geo_tmp}" -o "${msh_out}"
done

