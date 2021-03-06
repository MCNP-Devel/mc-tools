#! /bin/sh
#
# This is an auxiliary script for fluka2root.
# It simplifies calling the FLUKA merge tools
# with GNU parallel
# The script assumes that the argv[1] extension
# is the FLUKA merge tool name
#
# https://github.com/kbat/mc-tools

if [ $# -ne 1 ]; then
    echo "Usage: $0 filename.ext"
    exit 1
fi

in="$1"
if [ ! -e ${in} ]; then
    echo "File ${in} does not exist"
    exit 2
fi

merge="${in##*.}"
if [ ${merge} = ${in} ]; then
    echo "${in} must have an extension"
    exit 3
fi

if [ ! -e ${FLUTIL}/${merge} ]; then
    echo "${FLUTIL}/${merge} does not exist"
    exit 4
fi

cat ${in} | ${FLUTIL}/${merge}
