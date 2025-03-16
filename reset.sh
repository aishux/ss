feedName=$1

if [[ $feedName == *.ctl ]]; then
    feedNameRegex=$feedName
else
    case "$feedName" in
        "GPCCLI-D-GEN") 
            feedNameRegex="GPCCLI-D-GEN-[0-9]{8}(-[0-9]+)?\.csv\.gz"
            ;;
        "GPCCLI-D-GEN-DIM") 
            feedNameRegex="GPCCLI-D-GEN-DIM-[0-9]{8}(-[0-9]+)?\.csv\.gz"
            ;;
        "GPCCLI-D-GEN_AUDIT") 
            feedNameRegex="GPCCLI-D-GEN_AUDIT-[0-9]{8}(-[0-9]+)?\.csv\.gz"
            ;;
        *)
            feedNameRegex="$feedName-[0-9]{8}(-[0-9]+)?\.csv\.gz"  # Generic match for other files
            ;;
    esac
fi

expectedFeeds=$2

all=$(echo "$allFilesFilt" | grep -E "$feedNameRegex")
