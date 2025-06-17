#!/bin/sh

for file in *.xlsx; do
	if [[ -f "$file" ]]; then
		basename=$(basename $file .xlsx)
		echo $basename
		python ../tomato.py --population ../24ssjin.xlsx --consumption ../a401.xlsx --production "$file" --distance ../prefecture_capital_distances.csv --transportation ../transportation_cost.csv --prefix "$basename" --profit --profit-detailed --transportation-distance
	fi
done
