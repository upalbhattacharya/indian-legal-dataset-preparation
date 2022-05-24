#!/usr/bin/sh
# Birth: 2022-03-01 13:34:46.239037654 +0530
# Modify: 2022-03-01 13:54:07.219043947 +0530

# Move files from SRC to DEST based on file names in a given file

# Getting the source, destination and file to read names from.
while getopts s:d:f:e: option;
do 
    case "$option" in 
        s)
            SRC=$OPTARG
        ;;
        d)
            DEST=$OPTARG
        ;;
        f)
            FILE=$OPTARG
        ;;
        e)
            EXT=$OPTARG
        ;;
    esac
done

LINES=$(cat $FILE)

for line in $LINES
do
    echo $line
    path=$SRC/$line.$EXT
    echo $path
    cp $SRC/$line.$EXT $DEST
done
