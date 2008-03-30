#!/bin/bash

################################################################################
# copyright Bjarne D Mathiesen
#           KÀbenhavn ; Danmark ; Europa
#           macintosh .at. mathiesen .dot. info
# date      20/10-2005
#
# this script is released under the OSS GPL license
# the author welcomes feedback and improvements
# 

# purpose : to automate the whole 'port -acu upgrade' process
#           recursively uninstalling and re-installing ports 
#           that are dependent upon the ports that need upgrading

# update MacPorts itself
echo "Running port selfupdate..."
sudo port selfupdate
echo "Running port sync..."
sudo port sync

echo "get a list of the installed ports..."
portList=( $( port installed | sed 1,1d | cut -f 3 -d ' ' ) )

echo "get a list of the outdated ports..."
echo
port outdated
portOutdated=( $( port outdated | sed 1,1d | cut -f 1 -d ' ' ) )

declare -a portDeactivate           # a list of the ports dependent on a single port
declare -a portDeactivateCurrent    # accumulated list of port dependencies for a single iteration of the search
declare -a portDeactivateTotal      # the total list of the found dependencies
declare -a portTesting              # a list of the ports under scrutiny
declare -a portDependencies         # the total list of port dependencies

echo "build the total list of ports that have dependencies..."
(( index=0 ))
for listet in ${portList[@]}
do
    portDepends=( $( port deps ${listet} | sed "/${listet}/d" |tr -d '\t' ) )
    if [ ${#portDepends[@]} -ne 0 ]
    then
        portDependencies[${index}]=$( echo "${listet}: ${portDepends[@]}" )
        (( index++ ))
    fi
done

echo "intiate the first search for dependencies..."
portDeactivateCurrent=( $( echo ${portOutdated[@]} ) )

echo "keep on testing recursively..."
while [ ! ]
do
    echo -e "."
    portTesting=( $( echo ${portDeactivateCurrent[@]} ) )
    unset -v portDeactivateCurrent[@]

    # portTesting has now been initiated with the ports found in the last iteration
    # portDeactivateCurrent has been cleared and is ready to receive newly found dependencies

    for deactivate in ${portTesting[@]}
    do
        # search through all the installed ports for ports that has a 
        # dependency on one of the ports that's being tested
        portDeactivate=( \
            $( { for (( index=0 ; index < ${#portDependencies[@]} ; index++ ))
                 do
                     echo "${portDependencies[${index}]}"
                 done } \
              | grep ${deactivate} |  sed -E "/^${deactivate}:/d" | cut -f 1 -d ':' ) )

        # remove duplicates from the list of currently found dependencies
        for portName in ${portDeactivate[@]}
        do
            portDeactivateCurrent=( $( echo "${portDeactivateCurrent[@]}" \
                                  | sed "s/${portName}//" ) )
        done

        portDeactivateCurrent=( $( echo "${portDeactivate[@]} ${portDeactivateCurrent[@]}" ) )
    done

    # don't recurse down through the outdated ports
    # so remove them if they should turn up as dependencies
    for portName in ${portOutdated[@]}
    do
        portDeactivateCurrent=( $( echo "${portDeactivateCurrent[@]}" \
                              | sed "s/${portName}//" ) )
    done

    # test if new dependecies have been discovered
    if [ -n "$(echo -n ${portDeactivateCurrent[@]} | tr -d ' ')" ]
    then
        # remove instances of dependencies that already are present in the total list
        for portName in ${portDeactivateCurrent[@]}
        do
            portDeactivateTotal=( $( echo "${portDeactivateTotal[@]}" | sed "s/${portName}//" ) )
        done

        # concatenate the newly discovered dependencies with the old list
        portDeactivateTotal=( $( echo "${portDeactivateCurrent[@]} ${portDeactivateTotal[@]}" ) )
    else
        # stop the search
        break
    fi

done

echo -e "\n\rThe following installed ports seem to have dependencies on the outdated ports."
for deactivate in ${portDeactivateTotal[@]}
do
    echo $(port installed ${deactivate} | sed 1,1d)
        (sudo port uninstall ${deactivate}) ; wait
done

echo -e "\n\rupgrade the outdated ports"
echo "and uninstall and remove the outdated version(s)"
for outdated in ${portOutdated[@]}
do
    echo $(port installed ${outdated} | sed 1,1d)
        (sudo port -acu upgrade ${outdated}) ; wait
done

echo -e "\n\rre-install all the ports that in some way is dependent on the upgraded ports"
for activate in ${portDeactivateTotal[@]}
do
    (sudo port install ${activate}) ; wait
    done

    exit

