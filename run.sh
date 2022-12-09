#./run.sh
#!/bin/bash
#set -x
float_scale=2

function float_eval()
{
    local stat=0
    local result=0.0
    if [[ $# -gt 0 ]]; then
        result=$(echo "scale=$float_scale; $*" | bc -q 2>/dev/null)
        stat=$?
        if [[ $stat -eq 0  &&  -z "$result" ]]; then stat=1; fi
    fi
    echo $result
    return $stat
}

# User section
# Define parameters here
offsetx=$(float_eval "0")
echo "offsetx" is $offsetx
offsety=$(float_eval "0")
echo "offsety" is $offsety
npointsx=1;
echo "npointsx" is $npointsx
npointsy=1;
echo "npointsy" is $npointsy
sizex=$(float_eval "3.0")
echo "sizex" is $sizex #half
sizey=$(float_eval "3.0")
echo "sizey" is $sizey #half
nsimproc=3;
echo "Number of parallel process: $nsimproc"

# End of user section
# initialize x to 0
dx=$(float_eval "($sizex / $npointsx)")
echo "dx" is $dx
dy=$(float_eval "($sizey / $npointsy)")
echo "dy" is $dy

y=0;
i=0;
k=0;
while [ "$i" -lt $npointsy ] 
do
 echo "Current value of y: $y"
 j=0;
 x=0;
 while [ "$j" -lt $npointsx ]
 do
  echo "Current value of x: $x"
  if [ "$k" -lt $nsimproc ]; then
   Gate -a [WrappingMaterial,PTFE][CrystalMaterial,LYSO-Ce-Hilger][LateralSurface,BlackEpoxyPaint][TopSurface,PTFE_wrapped][X,$x][Y,$y][i,$i][j,$j] mac/mainMacroMono.mac > output/Mono511keV/term_output$i$j.txt&
   k=$(expr $k + 1)
  else
   Gate -a [WrappingMaterial,PTFE][CrystalMaterial,LYSO-Ce-Hilger][LateralSurface,BlackEpoxyPaint][TopSurface,PTFE_wrapped][X,$x][Y,$y][i,$i][j,$j] mac/mainMacroMono.mac > output/Mono511keV/term_output$i$j.txt
   k=0;
  fi
  # increment the value of x:
 x=$(float_eval "(($x + $dx + $offsetx))")
 j=$(expr $j + 1)
 done
 y=$(float_eval "(($y + $dy + $offsety))")
 i=$(expr $i + 1)
done 

