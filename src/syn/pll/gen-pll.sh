#!/bin/bash

cd $(dirname "$0")

# define frequencies in MHz
f_in=25
f_out=(
    48
    192
)

# always clean last generation
rm ./*.v

if [ "$1" == "clean" ]; then
    # if we're only meant to clean, then exit now
    exit
elif [ "$1" == "generate" ]; then
    # generate ecopll calls for all frequencies
    for i in "${!f_out[@]}"
    do
        name="pll${i}"
        echo "$i: ${f_out[$i]}MHz -> ${name}"

        ecppll --highres -i ${f_in} -o ${f_out[$i]} \
            -n ${name} \
            -f ./${name}.v
    done
fi;
