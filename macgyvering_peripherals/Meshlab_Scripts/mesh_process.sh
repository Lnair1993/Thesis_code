#!/bin/sh
# Script for reading a set of .dae, .stl or .obj files and converting them to processed ply files

inFolder="Input/*"
outFolder="output"
mlxScript="mesh_process.mlx"

for f in $inFolder
do
	if [ ! -d "$outFolder" ]; then
		mkdir $outFolder
	fi

	filename=$(basename -- "$f")
	filename="${filename%.*}"
	filename="$filename.ply"

	#Process through meshlab
	echo "meshlabserver -i $f -o $outFolder/out_$filename -s ./$mlxScript -om vc vn;"
	meshlabserver -i $f -o $outFolder/out_$filename -s ./$mlxScript -om vc vn;
done


