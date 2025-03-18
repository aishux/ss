feedName=$1

if [[ $feedName == *.ctl ]]; then
    feedNameRegex=$feedName
else
    case "$feedName" in
        "GPCCLI-D-GEN") 
            echo "Processing feed: GPCCLI-D-GEN"
            feedNameRegex="^GPCCLI-D-GEN-[0-9]{8}(-[0-9]+)?\.csv\.gz$"
            ;;
        "GPCCLI-D-GEN-DIM") 
            echo "Processing feed: GPCCLI-D-GEN-DIM"
            feedNameRegex="^GPCCLI-D-GEN-DIM-[0-9]{8}(-[0-9]+)?\.csv\.gz$"
            ;;
        "GPCCLI-D-GEN_AUDIT") 
            echo "Processing feed: GPCCLI-D-GEN_AUDIT"
            feedNameRegex="^GPCCLI-D-GEN_AUDIT-[0-9]{8}(-[0-9]+)?\.csv\.gz$"
            ;;
        *)
            echo "Processing generic feed: $feedName"
            # Ensure "GPCCLI-D-GEN-DIM" is not included
            feedNameRegex="^(?!GPCCLI-D-GEN-DIM)$feedName[-_][0-9]{8}(-[0-9]+)?\.csv\.gz$"
            ;;
    esac
fi

expectedFeeds=$2

# Debugging: Show regex being used
echo "Using regex: $feedNameRegex"

all=$(echo "$allFilesFilt" | grep -E "$feedNameRegex")
