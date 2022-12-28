#! /bin/bash
# MEM

source ~/.profile

this=_mem
s2d_reset="^d^"
#color="^c#2D1B46^^b#335566^"
#color="^c#1A1A1A^^b#334466^"
#color="^c#1A1A1A^^b#D282E8^"
#color="^c#D08DB1^^b#292431^"
color="^c#1A1A1A^^b#334466^"
signal=$(echo "^s$this^" | sed 's/_//')

update() {
    mem_total=$(cat /proc/meminfo | grep "MemTotal:"|awk '{print $2}')
    mem_free=$(cat /proc/meminfo | grep "MemFree:"|awk '{print $2}')
    mem_buffers=$(cat /proc/meminfo | grep "Buffers:"|awk '{print $2}')
    mem_cached=$(cat /proc/meminfo | grep -w "Cached:"|awk '{print $2}')
    mem_usage=$(awk "BEGIN {printf \"%.2f\", ($mem_total - $mem_free - $mem_buffers - $mem_cached) * 0.01 / 10240}")
    mem_total=$(awk "BEGIN {printf \"%.2f\", $mem_total * 0.01 / 10240}")
	mem_icon=""
    mem_text="$mem_usage"G/"$mem_total"G
    text=" $mem_icon $mem_text "
    echo $text
    sed -i '/^export '$this'=.*$/d' $DWM/statusbar/temp
    printf "export %s='%s%s%s%s'\n" $this "$color" "$signal" "$text|" "$s2d_reset" >> $DWM/statusbar/temp
}

notify() {
    dunstify " Memory tops" "\n$(ps axch -o cmd:15,%mem --sort=-%mem | head)" -r 9527
}

click() {
    case "$1" in
        L) notify ;;
        M) ;;
        R) killall btop || st -g 82x25 -c noborder -e btop ;;
        U) ;;
        D) ;;
    esac
}

case "$1" in
    click) click $2 ;;
    notify) notify ;;
    *) update ;;
esac
