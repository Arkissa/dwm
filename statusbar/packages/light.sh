#! /bin/bash

source ~/.profile

this=_light
s2d_reset="^d^"
#color="^c#1A1A1A^^b#334466^"
#color="^c#1A1A1A^^b#D282E8^"
#color="^c#D08DB1^^b#292431^"
color="^c#1A1A1A^^b#334466^"
signal=$(echo "^s$this^" | sed 's/_//')

update() {
    light_num=$(light | awk -F '.' '{print $1}')
    light_icon=""
    if [ "$light_num" -lt 20 ];  then light_icon="";
    elif [ "$light_num" -lt 30 ];  then light_icon="";
    elif [ "$light_num" -lt 40 ];  then light_icon="";
    elif [ "$light_num" -lt 50 ];  then light_icon="";
    elif [ "$light_num" -lt 60 ];  then light_icon="";
    elif [ "$light_num" -lt 70 ];  then light_icon="";
    elif [ "$light_num" -lt 80 ];  then light_icon="";
    elif [ "$light_num" -lt 90 ];  then light_icon="";
    elif [ "$light_num" -lt 95 ];  then light_icon="";
    else light_icon=""; fi

    light_num=$light_num%

    text=" $light_icon $light_num "
    echo $text
    sed -i '/^export '$this'=.*$/d' $DWM/statusbar/temp
    printf "export %s='%s%s%s%s'\n" $this "$color" "$signal" "$text|" "$s2d_reset" >> $DWM/statusbar/temp
}

notify() {
    dunstify -r 9527 "Screen light" "$(update)"
}


click() {
    case "$1" in
        L) notify             ;; # 仅通知
        M)                    ;;
        R)                    ;;
        U) light -A 5; notify ;; # 亮度加
        D) light -U 5; notify ;; # 亮度减
    esac
}

case "$1" in
    click) click $2 ;;
    notify) notify ;;
    *) update ;;
esac
