#!bin/bash

LOGINUSERNAME="ad";
PASSWORD="pwd";
kURL="https://google.com";
SESSIONID="";
USERGPN=$1;

getSessionIdFromServer(){
    output=$(curl -s -X POST -H "Accept:application/JSON" -d 'username='$LOGINUSERNAME'&password'=$PASSWORD $kURL/rest/login);
    LENTOREAD='expr ${#output} - 27';
    SESSIONID='expr substr $output 25 $LENTOREAD';
}

DELETE(){
    getSessionIdFromServer
    output=$(curl -X DELETE \
    ''$kURL'/rest/user/'$USERGPN \ 
    -H "Accept:application/JSON" \
    -H sessionid:$SESIONID);
echo "$output";
}

DELETE
