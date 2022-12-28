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

this=_blues
s2d_reset="^d^"
#color="^c#1A1A1A^^b#334466^"
#color="^c#1A1A1A^^b#D282E8^"
#color="^c#D08DB1^^b#292431^"
color="^c#1A1A1A^^b#334466^"
signal=$(echo "^s$this^" | sed 's/_//')
blues_status=$(bluetoothctl show | grep "Powered:" | awk -F ': ' '{print $2}')
blues_name=$(bluetoothctl info | grep "Name:" | sed 's/^[\t]*//g' |awk -F ':' '{print $2}' | sed 's/^[ ]//g')
blues_mac=$(bluetoothctl info | grep "^Device " | awk '{print $2}' |grep -E "\w+:\w+:\w+:\w+:\w+:\w+")
blues_info=$(bluetoothctl info)

update() {
    blues=()
    [ "$blues_status" == "no" ] && blues=(${blues[@]} "") \
    || [ "$blues_status" == "yes" ] && blues=(${blues[@]} "")
    [ "$(bluetoothctl info | grep 'Icon' | awk -F ': ' '{print $2}')" == "input-mouse" ] && blues=(${blues[@]} "")
    [ "$(bluetoothctl info | grep 'Icon' | awk -F ': ' '{print $2}')" == "audio-headset" ] && blues=(${blues[@]} "")
    [ "$blues_info" == 'Missing device address argument' ] && blues_name="--" && blues=("")
    
    sed -i '/^export '$this'=.*$/d' $DWM/statusbar/temp
    if [ "$blues" ]; then
        text=" ${blues[@]} $blues_name "
        echo $text
        printf "export %s='%s%s%s%s'\n" $this "$color" "$signal" "$text|" "$s2d_reset" >> $DWM/statusbar/temp
    fi
}

notify() {
    msg="蓝牙名: $blues_name\nMAC: $blues_mac"
    [ "$blues_info" == 'Missing device address argument' ] && msg='没有连接任何设备'
    dunstify -r 9527 " bluetooth" "$msg"
}

toggle() {
    if [ "$blues_status" == "yes" ]; then
        bluetoothctl power off
    elif [ "$blues_status" == "no" ]; then
        bluetoothctl power on
    fi
}


click() {
    case "$1" in
        L) notify                             ;; # 仅通知
        M) toggle; update;                    ;; # 切换蓝牙
        R) killall blueberry || blueberry &   ;; # 打开blueberry
        U)                                    ;; # 音量加
        D)                                    ;; # 音量减
    esac
}

case "$1" in
    click) click $2 ;;
    notify) notify ;;
    *) update ;;
esac
