#! /bin/bash
# DATE 获取日期和时间的脚本

source ~/.profile

this=_date
s2d_reset="^d^"
#color="^c#1A1A1A^^b#334466^"
#color="^c#1A1A1A^^b#D282E8^"
#color="^c#D08DB1^^b#292431^"
color="^c#1A1A1A^^b#334466^"
signal=$(echo "^s$this^" | sed 's/_//')

update() {
    time_text="$(date '+%Y/%m/%d %H:%M:%S')"
    case "$(date '+%I')" in
        "01") time_icon="" ;;
        "02") time_icon="" ;;
        "03") time_icon="" ;;
        "04") time_icon="" ;;
        "05") time_icon="" ;;
        "06") time_icon="" ;;
        "07") time_icon="" ;;
        "08") time_icon="" ;;
        "09") time_icon="" ;;
        "10") time_icon="" ;;
        "11") time_icon="" ;;
        "12") time_icon="" ;;
    esac

    text=" $time_icon $time_text "
    echo $text
    sed -i '/^export '$this'=.*$/d' $DWM/statusbar/temp
    printf "export %s='%s%s%s%s'\n" $this "$color" "$signal" "$text" "$s2d_reset" >> $DWM/statusbar/temp
}

notify() {
    dunstify "  Calendar" "\n$(cal --color=always | sed 1,2d | sed 's/..7m/<b><span color="#4F5C80">/;s/..27m/<\/span><\/b>/' )" -r 9527
}

notify_todo() {
    dunstify "TODO" "\n$(cat ~/.todo.md | sed 's/\(- \[x\] \)\(.*\)/<span color="#ff79c6">\1<s>\2<\/s><\/span>/' | sed 's/- \[[ |x]\] //')" -r 9527
}

click() {
    case "$1" in
        L) notify ;;
        M) alacritty --class float -e nvim ~/.todo.md ;;
        R) notify_todo ;;
        U) ;;
        D) ;;
    esac
}

case "$1" in
    click) click $2 ;;
    notify) notify ;;
    *) update ;;
esac
