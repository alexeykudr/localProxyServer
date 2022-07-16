#!/bin/bash
export PATH="$PATH:/usr/sbin"
SN="$(basename "$0")"
flag="0"
OF="<request><dataswitch>0</dataswitch></request>"
ON="<request><dataswitch>1</dataswitch></request>"
UMTS="<request><NetworkMode>02</NetworkMode><NetworkBand>3FFFFFFF</NetworkBand><LTEBand>7FFFFFFFFFFFFFFF</LTEBand></request>"
LTE="<request><NetworkMode>03</NetworkMode><NetworkBand>3FFFFFFF</NetworkBand><LTEBand>7FFFFFFFFFFFFFFF</LTEBand></request>"
AVTO="<request><NetworkMode>00</NetworkMode><NetworkBand>3FFFFFFF</NetworkBand><LTEBand>7FFFFFFFFFFFFFFF</LTEBand></request>"

function print_help() {
     printf "\n"
     printf "Использование: %s options...\n" "$SN"
     printf "Параметры:\n"
     printf " -i IP модема.\n"
     printf " -r Режим работы модема\n"
     printf " -h Справка.\n"
     printf "\n"
}

function a() {
    MODEM_IP=$1
    ip_before=`curl -s --connect-timeout 10 --interface $MODEM_IP"00" ipinfo.io/ip`
    
    ID2=`pgrep -f "[-]$MODEM_IP"00".cfg"`
    if [[ "$ID2" > "1" ]]; then
        kill -9 $ID2
    fi
    ( echo "atc 'AT+CFUN=7'"; sleep 5; echo "atc 'AT+CFUN=1'"; sleep 1; echo "atc 'AT+CFUN=1'"; sleep 1; echo "atc 'AT+CFUN=1'"; sleep 1; echo "quit"; ) | telnet $MODEM_IP >/dev/null 2>&1
    printf "IP сменился"
    printf "\n"
    n2=1
    while true
    do
        flag2="0"
        for i in {1..1}; do
            timeout -k 2 -s TERM 16 ping -w 2 -s 8 -c 1 -I $MODEM_IP"00" ipinfo.io >/dev/null 2>&1 || flag2=$((flag2+1))
        done
        if [ "$flag2" == "0" ]; then
#            break
            ip_after=`curl -s --connect-timeout 3 --interface $MODEM_IP"00" ipinfo.io/ip`
            if [ ! -z $ip_after ]; then
                if [ "$ip_before" != "$ip_after" ]; then
                    break
                    ( echo "atc 'AT+CFUN=7'"; sleep 1; echo "quit"; ) | telnet $MODEM_IP >/dev/null 2>&1
                fi
            fi
        fi
        ( echo "atc 'AT+CFUN=1'"; sleep 1; echo "atc 'AT+CFUN=1'"; sleep 1; echo "atc 'AT+CFUN=1'"; sleep 1; echo "quit"; ) | telnet $MODEM_IP >/dev/null 2>&1
        sleep 3
        #printf "\n"
        if [ "$n2" == "5" ]; then
            ( echo "atc 'AT^RESET'"; sleep 1; echo "quit"; ) | telnet $MODEM_IP >/dev/null 2>&1
            break
        fi
        ((n2+=1))
    done
}

# Если скрипт запущен без аргументов, открываем справку.
if [[ $# = 0 ]]; then
    print_help && exit 1
fi
while getopts ":i:r:h" opt ;
do
     case $opt in
         i) MODEM_IP=$OPTARG;
         ;;
         r) REJIM=$OPTARG;
         ;;
         h) print_help
         exit 1
         ;;
         *) printf "Неправильный параметр\n";
         printf "Для вызова справки запустите %s -h\n" "$SN";
         exit 1
         ;;
     esac
done

if [[ "$MODEM_IP" == "" ]] || [[ "$REJIM" == "" ]] ; then
     printf "\n"
     printf "Одна или несколько опций не указаны.\n"
     printf "Для справки наберите: %s -h\n" "$SN"
     printf "\n"
     exit 1
fi

a "$MODEM_IP"