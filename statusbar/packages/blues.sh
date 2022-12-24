#! /bin/bash
# VOL 音量脚本
# 本脚本需要你自行修改音量获取命令
# 例如我使用的是 pipewire
#
# $ pactl lisk sinks | grep RUNNING -A 8
#         State: RUNNING
#         Name: bluez_output.88_C9_E8_14_2A_72.1
#         Description: WH-1000XM4
#         Driver: PipeWire
#         Sample Specification: float32le 2ch 48000Hz
#         Channel Map: front-left,front-right
#         Owner Module: 4294967295
# 静音 -> Mute: no                                                                                 
# 音量 -> Volume: front-left: 13183 /  20% / -41.79 dB,   front-right: 13183 /  20% / -41.79 dB

source ~/.profile

this=_vol
s2d_reset="^d^"
#color="^c#553388^^b#334466^"
color="^c#1A1A1A^^b#334466^"
signal=$(echo "^s$this^" | sed 's/_//')
blues_status=$(bluetoothctl show | grep "Powered:" | awk -F ': ' '{print $2}')

update() {
    blues=()
    [ "$blues_status" == "yes" ] && blues=(${blues[@]} "")
    [ "$blues_status" == "no" ] && blues=(${blues[@]} "")
    [ "$(bluetoothctl info 64:03:7F:7C:81:15 | grep 'Connected: yes')" ] && icons=(${icons[@]} "")
    [ "$(bluetoothctl info 8C:DE:F9:E6:E5:6B | grep 'Connected: yes')" ] && icons=(${icons[@]} "")
    [ "$(bluetoothctl info 88:C9:E8:14:2A:72 | grep 'Connected: yes')" ] && icons=(${icons[@]} "")
    [ "$AUTOSCREEN" = "OFF" ] && icons=(${icons[@]} "ﴸ")

    sed -i '/^export '$this'=.*$/d' $DWM/statusbar/temp
    if [ "$icons" ]; then
        text=" ${icons[@]} "
        echo $text
        printf "export %s='%s%s%s%s'\n" $this "$color" "$signal" "$text" "$s2d_reset" >> $DWM/statusbar/temp
    fi
}

notify() {
    str=$(pactl list sinks | grep -E "Description:"  | sed 's/^[\t]*//g' | tr -d 'Description:' | sed 's/^[ ]*//g' | tr '\n' ':')
    IFS=":"
    arr=($str)
    dunstify -r 9527 ${arr[-1]} "$($DWM/statusbar/statusbar.sh update vol)" -i audio-volume-medium
}


click() {
    case "$1" in
        L) notify                                           ;; # 仅通知
        M) pactl set-sink-mute @DEFAULT_SINK@ toggle        ;; # 切换静音
        R) killall pavucontrol || pavucontrol &             ;; # 打开pavucontrol
        U) pactl set-sink-volume @DEFAULT_SINK@ +5%; notify ;; # 音量加
        D) pactl set-sink-volume @DEFAULT_SINK@ -5%; notify ;; # 音量减
    esac
}

case "$1" in
    click) click $2 ;;
    notify) notify ;;
    *) update ;;
esac
