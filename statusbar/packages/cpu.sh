#! /bin/bash
# CPU 获取CPU使用率和温度的脚本

source ~/.profile

this=_cpu
s2d_reset="^d^"
#color="^c#1A1A1A^^b#334466^"
#color="^c#1A1A1A^^b#D282E8^"
#color="^c#D08DB1^^b#292431^"
color="^c#1A1A1A^^b#334466^"
signal=$(echo "^s$this^" | sed 's/_//')

update() {
    cpu_icon="閭"
    cpu_text=$(top -n 1 -b | sed -n '3p' | awk '{printf "%02d%", 100 - $8}')
    temp_text=$(sensors | grep Tctl | awk '{printf "%d", $2}')  

    [ "$temp_text" -ge 85 ] \
        && temp_icon="" \
        && dunstify -r 9627 -u critical  "温度过高: $temp_icon $temp_text"

    if [ "$temp_text" -ge 85 ]; then temp_icon="";
    elif [ "$temp_text" -ge 70 ]; then temp_icon="";
    elif [ "$temp_text" -ge 60 ]; then temp_icon="";
    elif [ "$temp_text" -ge 50 ]; then temp_icon="";
    else temp_icon=""; fi

    text=" $cpu_icon $cpu_text | $temp_icon $temp_text°C "
    echo $text
    sed -i '/^export '$this'=.*$/d' $DWM/statusbar/temp
    printf "export %s='%s%s%s%s'\n" $this "$color" "$signal" "$text|" "$s2d_reset" >> $DWM/statusbar/temp
}

notify() {
    dunstify "閭 CPU tops" "\n$(ps axch -o cmd:15,%cpu --sort=-%cpu | head)\\n\\n(100% per core)" -r 9527
}

click() {
    case "$1" in
        L) notify ;;
        M) ;;
        R) killall btop || alacritty --class noborder -e btop &;;
        U) ;;
        D) ;;
    esac
}

case "$1" in
    click) click $2 ;;
    notify) notify ;;
    *) update ;;
esac
