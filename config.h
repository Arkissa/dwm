#include <X11/XF86keysym.h>

static int showsystray                   = 1;         /* 是否显示托盘栏 */
static const int newclientathead         = 0;         /* 定义新窗口在栈顶还是栈底 */
static const unsigned int borderpx       = 1;         /* 窗口边框大小 */
static const unsigned int systraypinning = 0;         /* 托盘跟随的显示器 0代表不指定显示器 */
static const unsigned int systrayspacing = 1;         /* 托盘间距 */
static int gappi                         = 12;        /* 窗口与窗口 缝隙大小 */
static int gappo                         = 12;        /* 窗口与边缘 缝隙大小 */
static const int _gappo                  = 12;        /* 窗口与窗口 缝隙大小 不可变 用于恢复时的默认值 */
static const int _gappi                  = 12;        /* 窗口与边缘 缝隙大小 不可变 用于恢复时的默认值 */
static const int overviewgappi           = 24;        /* overview时 窗口与边缘 缝隙大小 */
static const int overviewgappo           = 60;        /* overview时 窗口与窗口 缝隙大小 */
static const int vertpad                 = 10;       /* vertical padding of bar */
static const int sidepad                 = 10;       /* horizontal padding of bar */
static const int showbar                 = 1;         /* 是否显示状态栏 */
static const int topbar                  = 1;         /* 指定状态栏位置 0底部 1顶部 */
static const float mfact                 = 0.5;         /* 主工作区 大小比例 */
static const int   nmaster               = 1;         /* 主工作区 窗口数量 */
static const unsigned int snap           = 10;        /* 边缘依附宽度 */
//static const unsigned int baralpha       = 0xc0;      /* 状态栏透明度 */
//static const unsigned int borderalpha    = 0x1f4;      /* 边框透明度 */
static const unsigned int baralpha       = 0x3e8;      /* 状态栏透明度 */
static const unsigned int borderalpha    = 0x3e8;      /* 边框透明度 */
static const char *fonts[]               = { "JetBrainsMono Nerd Font:style=medium:size=12", "monospace:size=13" };
//static const char *fonts[]               = { "Monaco Nerd Font Complete Mono:style=medium:size=13", "monospace:size=13" };
static const char *colors[][3]           = {          /* 颜色设置 ColFg, ColBg, ColBorder */ 
    [SchemeNorm] = { "#babbf1", "#1a1b26", "#444444" },
    [SchemeSel] = { "#ffffff", "#1a1b26", "#5D78B9" },
    [SchemeSelGlobal] = { "#ffffff", "#37474F", "#FFC0CB" },
    [SchemeHid] = { "#c0caf5", "#1a1b26", "#444444" },
    [SchemeSystray] = { "#c0caf5", "#1a1b26", NULL },
    [SchemeUnderline] = { "#bafbf1", NULL, NULL }, 
    [SchemeNormTag] = { "#babbf1", "#1a1b26", NULL },
    [SchemeSelTag] = { "#babbf1", "#1a1b26", NULL },
    [SchemeBarEmpty] = { NULL, "#111111", NULL },
};
static const unsigned int alphas[][3]    = {          /* 透明度设置 ColFg, ColBg, ColBorder */ 
    [SchemeNorm] = { OPAQUE, baralpha, borderalpha }, 
    [SchemeSel] = { OPAQUE, baralpha, borderalpha },
    [SchemeSelGlobal] = { OPAQUE, baralpha, borderalpha },
    [SchemeNormTag] = { OPAQUE, baralpha, borderalpha }, 
    [SchemeSelTag] = { OPAQUE, baralpha, borderalpha },
    [SchemeBarEmpty] = { NULL, 0xa0a, NULL },
    [SchemeStatusText] = { OPAQUE, baralpha, borderalpha },
};

/* 自定义脚本位置 */
static const char *autostartscript = "~/scripts/autostart.sh";
static const char *statusbarscript = "~/.config/dwm/statusbar/statusbar.py";

/* 自定义 scratchpad instance */
static const char scratchpadname[] = "scratchpad";

/* 自定义tag名称 */
/* 自定义特定实例的显示状态 */
//            ﮸  ﭮ 切
// 对应的tag序号以及快捷键:   0:1  1:2  2:3  3:4  4:5  5:c  6:m  7:0  8:w  9:d  10:d
static const char *tags[] = { "", "", "", "", "", "", "", "ﬄ", "﬐", "", ""};
static const Rule rules[] = {
    /* class                 instance              title                tags mask     isfloating  isglobal    isnoborder monitor */
    {"chrome",               NULL,                 NULL,                1 << 5,       0,          0,          0,        -1 },
    {"Chromium",             NULL,                 NULL,                1 << 5,       0,          0,          0,        -1 },
    {"music",                NULL,                 NULL,                1 << 6,       1,          0,          1,        -1 },
    {"TelegramDesktop",      NULL,                 NULL,                1 << 7,       0,          0,          0,        -1 },
    { NULL,                 "wechat",              NULL,                1 << 8,       1,          0,          0,        -1 },
//    { NULL,                 "wxwork",              NULL,                1 << 11,      0,          0,          0,        -1 },
    { NULL,                  NULL,                "broken",             0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "图片查看",           0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "图片预览",           0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "虚拟系统管理器",     0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "防火墙配置",         0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "自定义外观和体验",   0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "Qt5 配置工具",       0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "Fcitx 配置",         0,            1,          0,          0,        -1 },
    { NULL,                  NULL,                "crx_",               0,            1,          0,          0,        -1 },
    {"flameshot",            NULL,                 NULL,                0,            1,          0,          0,        -1 },
    {"wemeetapp",            NULL,                 NULL,                TAGMASK,      1,          1,          0,        -1 }, // 腾讯会议在切换tag时有诡异bug导致退出 变成global来规避该问题
    {"fm",                   NULL,                 NULL,                TAGMASK,      1,          0,          0,        -1 }, // pcmanfm 浮动
    {NULL,                   NULL,                 "Burp Suite",        0,            1,          0,          0,        -1 }, // Burp Suite 浮动
    {"tlpui",                "tlpui",              "Tlp-UI",            0,            1,          0,          0,        -1 }, // Burp Suite 浮动
    {NULL,                   NULL,                 "Timeshift",         0,            1,          0,          0,        -1 }, // Burp Suite 浮动
    {NULL,                   NULL,                 "百度网盘",          0,            1,          0,          0,        -1 }, // Burp Suite 浮动
    {NULL,                   NULL,                 "音量控制",          0,            1,          0,          0,        -1 }, // Burp Suite 浮动
    {NULL,                   NULL,                 "蓝牙",              0,            1,          0,          0,        -1 }, // Burp Suite 浮动
    {"float",                NULL,                 NULL,                0,            1,          0,          0,        -1 }, // 特殊class client默认浮动
    {"noborder",             NULL,                 NULL,                0,            1,          0,          1,        -1 }, // 特殊class client默认无边框
    {"global",               NULL,                 NULL,                TAGMASK,      1,          1,          0,        -1 }, // 特殊class client全局于所有tag
};
static const char *overviewtag = "OVERVIEW";
static const Layout overviewlayout = { "舘",  overview };

/* 自定义布局 */
static const Layout layouts[] = {
    { "﬿",  tile },         /* 主次栈 */
    { "﩯",  magicgrid },    /* 网格 */
};

#define SHCMD(cmd) { .v = (const char*[]){ "/bin/sh", "-c", cmd, NULL } }
#define MODKEY Mod4Mask
#define MODALT Mod1Mask
#define TAGKEYS(KEY, TAG, cmd1, cmd2) \
    { MODKEY,              KEY, view,       {.ui = 1 << TAG, .v = cmd1} }, \
    { MODKEY|ShiftMask,    KEY, tag,        {.ui = 1 << TAG, .v = cmd2} }, \
    { MODKEY|ControlMask,  KEY, toggleview, {.ui = 1 << TAG} }, \

static Key keys[] = {
    /* modifier            key              function          argument */
    { MODKEY,              XK_equal,        togglesystray,    {0} },                     /* super +            |  切换 托盘栏显示状态 */

    { MODKEY,              XK_Tab,          focusstack,       {.i = +1} },               /* super tab          |  本tag内切换聚焦窗口 */
    { MODKEY|ShiftMask,    XK_Tab,          focusstack,       {.i = -1} },               /* super shift tab    |  本tag内切换聚焦窗口 */

    { MODALT,              XK_h,            viewtoleft,       {0} },                     /* super left         |  聚焦到左边的tag */
    { MODALT,              XK_l,            viewtoright,      {0} },                     /* super right        |  聚焦到右边的tag */
    { MODALT|ShiftMask,    XK_h,            tagtoleft,        {0} },                     /* super shift left   |  将本窗口移动到左边tag */
    { MODALT|ShiftMask,    XK_l,            tagtoright,       {0} },                     /* super shift right  |  将本窗口移动到右边tag */

    { MODKEY,              XK_a,            toggleoverview,   {0} },                     /* super a            |  显示所有tag 或 跳转到聚焦窗口的tag */

    { MODKEY,              XK_comma,        setmfact,         {.f = -0.05} },            /* super ,            |  缩小主工作区 */
    { MODKEY,              XK_period,       setmfact,         {.f = +0.05} },            /* super .            |  放大主工作区 */

    { MODKEY,              XK_u,            hidewin,          {0} },                     /* super h            |  隐藏 窗口 */
    { MODKEY|ShiftMask,    XK_u,            restorewin,       {0} },                     /* super shift h      |  取消隐藏 窗口 */

    { MODKEY|ShiftMask,    XK_Return,       zoom,             {0} },                     /* super shift enter  |  将当前聚焦窗口置为主窗口 */

    { MODKEY,              XK_t,            togglefloating,   {0} },                     /* super t            |  开启/关闭 聚焦目标的float模式 */
    { MODKEY|ShiftMask,    XK_t,            toggleallfloating,{0} },                     /* super shift t      |  开启/关闭 全部目标的float模式 */
    { MODKEY,              XK_f,            fullscreen,       {0} },                     /* super f            |  开启/关闭 全屏 */
    { MODKEY|ShiftMask,    XK_f,            togglebar,        {0} },                     /* super shift f      |  开启/关闭 状态栏 */
    { MODKEY,              XK_g,            toggleglobal,     {0} },                     /* super g            |  开启/关闭 全局 */
    { MODKEY,              XK_c,            incnmaster,       {.i = +1} },               /* super e            |  改变主工作区窗口数量 (1 2中切换) */

    { MODKEY,              XK_i,            focusmon,         {.i = +1} },               /* super b            |  光标移动到另一个显示器 */
    { MODKEY|ShiftMask,    XK_i,            tagmon,           {.i = +1} },               /* super shift b      |  将聚焦窗口移动到另一个显示器 */

    { MODKEY,              XK_q,            killclient,       {0} },                     /* super q            |  关闭窗口 */
    { MODKEY|ControlMask,  XK_q,            forcekillclient,  {0} },                     /* super ctrl q       |  强制关闭窗口(处理某些情况下无法销毁的窗口) */
    { MODKEY|ControlMask,  XK_F12,          quit,             {0} },                     /* super ctrl f12     |  退出dwm */

	{ MODKEY|ShiftMask,    XK_space,        selectlayout,     {.v = &layouts[1]} },      /* super shift space  |  切换到网格布局 */
	{ MODKEY,              XK_o,            showonlyorall,    {0} },                     /* super o            |  切换 只显示一个窗口 / 全部显示 */

    { MODKEY|ControlMask,  XK_equal,        setgap,           {.i = -6} },               /* super ctrl +       |  窗口增大 */
    { MODKEY|ControlMask,  XK_minus,        setgap,           {.i = +6} },               /* super ctrl -       |  窗口减小 */
    { MODKEY|ControlMask,  XK_space,        setgap,           {.i = 0} },                /* super ctrl space   |  窗口重置 */

    { MODKEY|ControlMask,  XK_k,            movewin,          {.ui = UP} },              /* super ctrl up      |  移动窗口 */
    { MODKEY|ControlMask,  XK_j,            movewin,          {.ui = DOWN} },            /* super ctrl down    |  移动窗口 */
    { MODKEY|ControlMask,  XK_h,            movewin,          {.ui = LEFT} },            /* super ctrl left    |  移动窗口 */
    { MODKEY|ControlMask,  XK_l,            movewin,          {.ui = RIGHT} },           /* super ctrl right   |  移动窗口 */

    { MODKEY,     XK_k,           resizewin,        {.ui = V_REDUCE} },        /* super k    |  调整窗口 */
    { MODKEY,     XK_j,           resizewin,        {.ui = V_EXPAND} },        /* super j    |  调整窗口 */
    { MODKEY,     XK_h,           resizewin,        {.ui = H_REDUCE} },        /* super h    |  调整窗口 */
    { MODKEY,     XK_l,           resizewin,        {.ui = H_EXPAND} },        /* super l    |  调整窗口 */

    /* spawn + SHCMD 执行对应命令(已下部分建议完全自己重新定义) */
    { MODKEY,              XK_s,           togglescratch, SHCMD("kitty -T scratchpad --class float") },          /* super s            | 打开scratch终端        */
    { MODKEY,              XK_Return,      spawn, SHCMD("kitty") },                                              /* super enter        | 打开st终端             */
    { MODKEY,              XK_minus,       spawn, SHCMD("kitty --class global") },                               /* super +            | 打开全局st终端         */
    { MODKEY,              XK_space,       spawn, SHCMD("kitty --class float") },                                /* super space        | 打开浮动st终端         */
    { MODALT|ShiftMask,    XK_Return,      spawn, SHCMD("rofi -show tool -modi \"tool:~/scripts/rofi.py\" -terminal st -theme /home/bulabula/.config/rofi/config/tool.rasi") },         /* alt return         | rofi: 菜单             */
    { MODKEY|ControlMask,  XK_Return,      spawn, SHCMD("~/.config/rofi/bin/powermenu") },                           /* super shift return | rofi: 电源菜单         */
    { MODALT,              XK_Return,      spawn, SHCMD("~/.config/rofi/bin/launcher") },                            /* alt shift return   | rofi: 执行命令         */
    { MODKEY,              XK_p,           spawn, SHCMD("~/scripts/bin/blurlock.sh") },                              /* super p            | 锁定屏幕               */
    { MODKEY,              XK_F6,          spawn, SHCMD("~/scripts/bin/light.sh up") },                              /* super shift up     | 音量加                 */
    { MODKEY,              XK_F5,          spawn, SHCMD("~/scripts/bin/light.sh down") },                            /* super shift down   | 音量减                 */
    { MODKEY,              XK_F3,          spawn, SHCMD("~/scripts/bin/vol.sh up") },                                /* super shift up     | 音量加                 */
    { MODKEY,              XK_F2,          spawn, SHCMD("~/scripts/bin/vol.sh down") },                              /* super shift down   | 音量减                 */
    { MODKEY,              XK_F1,          spawn, SHCMD("pcmanfm") },                                                /* super f1           | 文件管理器                 */
    { MODALT|ShiftMask,    XK_a,           spawn, SHCMD("~/.config/rofi/bin/screenshot") },                          /* super shift a      | 截图                   */
    { MODKEY|ShiftMask,    XK_a,           spawn, SHCMD("flameshot gui -c -p ~/Pictures/screenshots") },             /* super shift a      | 截图                   */
    { MODKEY|ShiftMask,    XK_q,           spawn, SHCMD("kill -9 $(xprop | grep _NET_WM_PID | awk '{print $3}')") }, /* super shift q      | 选中某个窗口并强制kill */
    { ShiftMask|ControlMask, XK_c,         spawn, SHCMD("xclip -o | xclip -selection c") },                          /* super shift c      | 进阶复制               */

    /* super key : 跳转到对应tag */
    /* super shift key : 将聚焦窗口移动到对应tag */
    /* 若跳转后的tag无窗口且附加了cmd1或者cmd2就执行对应的cmd */
    /* key tag cmd1 cmd2 */
    TAGKEYS(XK_1,  0,  0,  0)
    TAGKEYS(XK_2,  1,  0,  0)
    TAGKEYS(XK_3,  2,  0,  0)
    TAGKEYS(XK_4,  3,  0,  0)
    TAGKEYS(XK_5,  4,  "obs",  0)
    TAGKEYS(XK_e,  5,  "google-chrome-stable", 0)
    TAGKEYS(XK_m,  6,  "~/scripts/bin/music.sh", "pavucontrol")
    TAGKEYS(XK_0,  7,  "tencent-qq", 0)
    TAGKEYS(XK_w,  8, "/opt/apps/com.qq.weixin.deepin/files/run.sh", 0)
    TAGKEYS(XK_d,  9, "virt-manager", 0)
    TAGKEYS(XK_r,  10, "~/apps/burpsuite/run.sh", 0)
};
static Button buttons[] = {
    /* click               event mask       button            function       argument  */
    /* 点击窗口标题栏操作 */
    { ClkWinTitle,         0,               Button1,          hideotherwins, {0} },                                   // 左键        |  点击标题     |  隐藏其他窗口仅保留该窗口
    { ClkWinTitle,         0,               Button3,          togglewin,     {0} },                                   // 右键        |  点击标题     |  切换窗口显示状态
    /* 点击窗口操作 */
    { ClkClientWin,        MODKEY,          Button1,          movemouse,     {0} },                                   // super+左键  |  拖拽窗口     |  拖拽窗口
    { ClkClientWin,        MODKEY,          Button3,          resizemouse,   {0} },                                   // super+右键  |  拖拽窗口     |  改变窗口大小
    /* 点击tag操作 */
    { ClkTagBar,           0,               Button1,          view,          {0} },                                   // 左键        |  点击tag      |  切换tag
	{ ClkTagBar,           0,               Button3,          toggleview,    {0} },                                   // 右键        |  点击tag      |  切换是否显示tag
    { ClkTagBar,           MODKEY,          Button1,          tag,           {0} },                                   // super+左键  |  点击tag      |  将窗口移动到对应tag
    { ClkTagBar,           0,               Button4,          viewtoleft,    {0} },                                   // 鼠标滚轮上  |  tag          |  向前切换tag
	{ ClkTagBar,           0,               Button5,          viewtoright,   {0} },                                   // 鼠标滚轮下  |  tag          |  向后切换tag
    /* 点击状态栏操作 */
    { ClkStatusText,       0,               Button1,          clickstatusbar,{0} },                                   // 左键        |  点击状态栏   |  根据状态栏的信号执行 ~/scripts/dwmstatusbar.sh $signal L
    { ClkStatusText,       0,               Button2,          clickstatusbar,{0} },                                   // 中键        |  点击状态栏   |  根据状态栏的信号执行 ~/scripts/dwmstatusbar.sh $signal M
    { ClkStatusText,       0,               Button3,          clickstatusbar,{0} },                                   // 右键        |  点击状态栏   |  根据状态栏的信号执行 ~/scripts/dwmstatusbar.sh $signal R
    { ClkStatusText,       0,               Button4,          clickstatusbar,{0} },                                   // 鼠标滚轮上  |  状态栏       |  根据状态栏的信号执行 ~/scripts/dwmstatusbar.sh $signal U
    { ClkStatusText,       0,               Button5,          clickstatusbar,{0} },                                   // 鼠标滚轮下  |  状态栏       |  根据状态栏的信号执行 ~/scripts/dwmstatusbar.sh $signal D
};
