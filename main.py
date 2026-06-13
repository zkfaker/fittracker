"""FitTracker - AI减肥管理应用"""

from kivy.config import Config
Config.set("graphics", "width", "420")
Config.set("graphics", "height", "780")
Config.set("kivy", "keyboard_mode", "system")

import os
import sys
import datetime
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDFlatButton, MDRaisedButton, MDFloatingActionButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.properties import StringProperty, NumericProperty, ListProperty

import database

# ── Theme Colors ──────────────────────────────────────────────
PRIMARY = "#4CAF50"
PRIMARY_LIGHT = "#81C784"
SECONDARY = "#2196F3"
ACCENT = "#FF9800"
DANGER = "#F44336"
BG_COLOR = "#F5F5F5"
CARD_WHITE = "#FFFFFF"
TEXT_PRIMARY = "#212121"
TEXT_SECONDARY = "#757575"

# ── KV Layout ────────────────────────────────────────────────
KV = """
ScreenManager:
    id: sm
    HomeScreen:
        name: "home"
    FoodDiaryScreen:
        name: "food"
    ExerciseLogScreen:
        name: "exercise"
    PlanScreen:
        name: "plan"
    CalendarScreen:
        name: "calendar"
    SettingsScreen:
        name: "settings"


<HomeScreen>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "FitTracker"
            md_bg_color: "#4CAF50"
            specific_text_color: 1, 1, 1, 1
            elevation: 2
            right_action_items: [["cog", lambda x: app.go_to_settings()]]

        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: home_container
                orientation: "vertical"
                spacing: dp(12)
                padding: [dp(16), dp(16), dp(16), dp(100)]
                size_hint_y: None
                height: self.minimum_height

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            md_bg_color: "#FFFFFF"
            padding: dp(8)

            MDIconButton:
                icon: "home"
                theme_text_color: "Custom"
                text_color: "#4CAF50"
                on_release: app.go_home()

            MDIconButton:
                icon: "food-apple"
                theme_text_color: "Custom"
                text_color: "#757575"
                on_release: app.go_to_food()

            MDIconButton:
                icon: "run"
                theme_text_color: "Custom"
                text_color: "#757575"
                on_release: app.go_to_exercise()

            MDIconButton:
                icon: "calendar-month"
                theme_text_color: "Custom"
                text_color: "#757575"
                on_release: app.go_to_calendar()

            MDIconButton:
                icon: "chart-line"
                theme_text_color: "Custom"
                text_color: "#757575"
                on_release: app.go_to_plan()


<FoodDiaryScreen>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "饮食记录"
            md_bg_color: "#4CAF50"
            specific_text_color: 1, 1, 1, 1
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: food_container
                orientation: "vertical"
                spacing: dp(12)
                padding: [dp(16), dp(16), dp(16), dp(80)]
                size_hint_y: None
                height: self.minimum_height


<ExerciseLogScreen>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "运动记录"
            md_bg_color: "#4CAF50"
            specific_text_color: 1, 1, 1, 1
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: exercise_container
                orientation: "vertical"
                spacing: dp(12)
                padding: [dp(16), dp(16), dp(16), dp(80)]
                size_hint_y: None
                height: self.minimum_height


<PlanScreen>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "减肥计划"
            md_bg_color: "#4CAF50"
            specific_text_color: 1, 1, 1, 1
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: plan_container
                orientation: "vertical"
                spacing: dp(12)
                padding: [dp(16), dp(16), dp(16), dp(80)]
                size_hint_y: None
                height: self.minimum_height


<CalendarScreen>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "日历"
            md_bg_color: "#4CAF50"
            specific_text_color: 1, 1, 1, 1
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: calendar_container
                orientation: "vertical"
                spacing: dp(12)
                padding: [dp(16), dp(16), dp(16), dp(16)]
                size_hint_y: None
                height: self.minimum_height


<SettingsScreen>:
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "设置"
            md_bg_color: "#4CAF50"
            specific_text_color: 1, 1, 1, 1
            elevation: 2
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)

            BoxLayout:
                id: settings_container
                orientation: "vertical"
                spacing: dp(12)
                padding: [dp(16), dp(16), dp(16), dp(80)]
                size_hint_y: None
                height: self.minimum_height
"""


class HomeScreen(MDScreen):
    pass

class FoodDiaryScreen(MDScreen):
    pass

class ExerciseLogScreen(MDScreen):
    pass

class PlanScreen(MDScreen):
    pass

class CalendarScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass


class CalendarWidget(BoxLayout):
    """自定义日历组件"""
    selected_date = StringProperty("")
    current_month = NumericProperty(0)
    current_year = NumericProperty(0)
    on_date_select = None

    WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(4)
        today = datetime.date.today()
        self.current_year = today.year
        self.current_month = today.month - 1
        self.selected_date = today.isoformat()
        self.build_calendar()

    def build_calendar(self):
        self.clear_widgets()

        # Header with month/year
        header = BoxLayout(
            size_hint_y=None,
            height=dp(50),
        )

        prev_btn = MDFlatButton(
            text="<",
            size_hint_x=0.2,
            on_release=lambda x: self.prev_month()
        )
        header.add_widget(prev_btn)

        month_names = ["1月", "2月", "3月", "4月", "5月", "6月",
                       "7月", "8月", "9月", "10月", "11月", "12月"]
        title_label = MDLabel(
            text=f"{self.current_year}年 {month_names[self.current_month]}",
            font_style="H6",
            halign="center",
            size_hint_x=0.6,
        )
        header.add_widget(title_label)

        next_btn = MDFlatButton(
            text=">",
            size_hint_x=0.2,
            on_release=lambda x: self.next_month()
        )
        header.add_widget(next_btn)
        self.add_widget(header)

        # Weekday headers
        weekday_grid = GridLayout(
            cols=7,
            size_hint_y=None,
            height=dp(35),
        )
        for day in self.WEEKDAYS:
            label = MDLabel(
                text=day,
                halign="center",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=self._rgba("#757575"),
            )
            weekday_grid.add_widget(label)
        self.add_widget(weekday_grid)

        # Days grid
        days_in_month = self._get_days_in_month()
        first_day = self._get_first_day_of_month()
        if first_day == 0:
            first_day = 7

        days_grid = GridLayout(
            cols=7,
            size_hint_y=None,
            height=dp(240),
            padding=dp(2),
            spacing=dp(2),
        )

        # Empty cells before first day
        for _ in range(first_day - 1):
            days_grid.add_widget(Widget())

        # Day cells
        today_str = datetime.date.today().isoformat()
        for day in range(1, days_in_month + 1):
            date_str = f"{self.current_year}-{self.current_month + 1:02d}-{day:02d}"
            is_today = date_str == today_str
            is_selected = date_str == self.selected_date

            btn = MDFlatButton(
                text=str(day),
                size_hint=(1, 1),
                on_release=lambda x, d=date_str: self.select_date(d),
            )

            if is_today:
                btn.md_bg_color = self._rgba("#4CAF50")
                btn.theme_text_color = "Custom"
                btn.text_color = (1, 1, 1, 1)
            elif is_selected:
                btn.md_bg_color = self._rgba("#FF9800")
                btn.theme_text_color = "Custom"
                btn.text_color = (1, 1, 1, 1)

            days_grid.add_widget(btn)

        self.add_widget(days_grid)

    def select_date(self, date_str):
        self.selected_date = date_str
        self.build_calendar()
        if self.on_date_select:
            self.on_date_select(date_str)

    def prev_month(self):
        if self.current_month == 0:
            self.current_month = 11
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 11:
            self.current_month = 0
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()

    def _get_days_in_month(self):
        return (datetime.date(self.current_year, self.current_month + 1 + 1, 1) -
                datetime.date(self.current_year, self.current_month + 1, 1)).days

    def _get_first_day_of_month(self):
        return datetime.date(self.current_year, self.current_month + 1, 1).weekday()

    def _rgba(self, hex_color):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1,)


class FitTrackerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        database.init_db()
        self.selected_date = datetime.date.today().isoformat()

    def build(self):
        self._register_cjk_fonts()
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def _register_cjk_fonts(self):
        import platform
        system = platform.system()

        font_regular = None
        font_bold = None
        font_medium = None

        # 项目目录中的捆绑字体（最可靠，APK打包后直接可用）
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bundled_regular = os.path.join(base_dir, "fonts", "NotoSansSC-Regular.otf")
        bundled_bold = os.path.join(base_dir, "fonts", "NotoSansSC-Bold.otf")
        bundled_medium = os.path.join(base_dir, "fonts", "NotoSansSC-Medium.otf")

        # 1) 优先使用捆绑字体
        if os.path.exists(bundled_regular):
            font_regular = bundled_regular
            print(f"[Font] Using bundled: {bundled_regular}")
            if os.path.exists(bundled_bold):
                font_bold = bundled_bold
            if os.path.exists(bundled_medium):
                font_medium = bundled_medium
        elif system == "Windows":
            font_regular = "C:/Windows/Fonts/msyh.ttc"
            font_bold = "C:/Windows/Fonts/msyhbd.ttc"
            if not os.path.exists(font_regular):
                font_regular = "C:/Windows/Fonts/simhei.ttf"
                font_bold = font_regular
                font_medium = font_regular
        elif system == "Linux":
            # Android字体路径 - 覆盖主流品牌
            android_fonts = [
                bundled_regular,
                "/system/fonts/NotoSansSC-Regular.otf",
                "/system/fonts/NotoSansCJK-Regular.ttc",
                "/system/fonts/NotoSansSC-Regular.ttf",
                "/system/fonts/DroidSansFallback.ttf",
                # Xiaomi (小米)
                "/system/fonts/MiSans-Regular.ttf",
                "/system/fonts/MiSans.ttf",
                # Huawei (华为)
                "/system/fonts/HarmonyOS_Sans_SC_Regular.ttf",
                "/system/fonts/HarmonyOS-Sans.ttf",
                # OPPO / vivo
                "/system/fonts/OPPOSans-Regular.ttf",
                "/system/fonts/OnePlusSans-Regular.ttf",
                # Samsung (三星)
                "/system/fonts/NotoSansKR-Regular.otf",
                "/system/fonts/SamsungOne-400.ttf",
                # 通用后备
                "/system/fonts/NotoSerifCJK-Regular.ttc",
                "/system/fonts/CJK_CN.ttf",
            ]
            for f in android_fonts:
                if os.path.exists(f):
                    font_regular = f
                    break

            # Bold 字体搜索
            android_bold_fonts = [
                bundled_bold,
                "/system/fonts/NotoSansSC-Bold.otf",
                "/system/fonts/NotoSansCJK-Bold.ttc",
                "/system/fonts/NotoSansSC-Bold.ttf",
                "/system/fonts/DroidSans-Bold.ttf",
                "/system/fonts/MiSans-Bold.ttf",
                "/system/fonts/HarmonyOS_Sans_SC_Bold.ttf",
            ]
            for f in android_bold_fonts:
                if os.path.exists(f):
                    font_bold = f
                    break
            if not font_bold:
                font_bold = font_regular

            # Medium 字体搜索
            android_medium_fonts = [
                bundled_medium,
                "/system/fonts/NotoSansSC-Medium.otf",
                "/system/fonts/NotoSansSC-Medium.ttf",
                "/system/fonts/MiSans-Medium.ttf",
            ]
            for f in android_medium_fonts:
                if os.path.exists(f):
                    font_medium = f
                    break
            if not font_medium:
                font_medium = font_regular

        if font_regular and os.path.exists(font_regular):
            print(f"[Font] Registering: {font_regular}")
            # 注册所有KivyMD使用的字体名称
            for name in ["Roboto", "RobotoLight", "RobotoThin", "Default"]:
                LabelBase.register(
                    name=name,
                    fn_regular=font_regular,
                    fn_bold=font_bold or font_regular,
                )
            # RobotoMedium 使用 Medium 变体（更精准的字重）
            LabelBase.register(
                name="RobotoMedium",
                fn_regular=font_medium or font_regular,
                fn_bold=font_bold or font_regular,
            )
        else:
            print("[Font] WARNING: No CJK font found, Chinese may display as boxes")


    def on_start(self):
        self.today_str = datetime.date.today().isoformat()
        self.refresh_home()

    def refresh_home(self):
        home = self.root.get_screen("home")
        container = home.ids.home_container
        container.clear_widgets()

        self.today_str = datetime.date.today().isoformat()
        user_data = database.get_user_profile()
        today_log = database.get_daily_log(self.today_str)

        intake = today_log["total_intake"] if today_log else 0
        burned = today_log["total_burned"] if today_log else 0
        net = intake - burned

        # 今日概览卡片
        overview_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            radius=dp(12),
            elevation=2,
            padding=dp(16),
            md_bg_color=self._rgba("#FFFFFF"),
        )
        overview_layout = BoxLayout(orientation="vertical", spacing=dp(8))

        overview_title = MDLabel(
            text="今日概览",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            bold=True,
            size_hint_y=None,
            height=dp(30),
        )
        overview_layout.add_widget(overview_title)

        stats_layout = BoxLayout(orientation="horizontal", spacing=dp(16), size_hint_y=None, height=dp(60))

        intake_box = BoxLayout(orientation="vertical")
        intake_box.add_widget(MDLabel(
            text=str(int(intake)),
            font_style="H5",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            bold=True,
            size_hint_y=None,
            height=dp(30),
        ))
        intake_box.add_widget(MDLabel(
            text="摄入(kcal)",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=self._rgba("#757575"),
            size_hint_y=None,
            height=dp(20),
        ))
        stats_layout.add_widget(intake_box)

        burn_box = BoxLayout(orientation="vertical")
        burn_box.add_widget(MDLabel(
            text=str(int(burned)),
            font_style="H5",
            theme_text_color="Custom",
            text_color=self._rgba("#2196F3"),
            bold=True,
            size_hint_y=None,
            height=dp(30),
        ))
        burn_box.add_widget(MDLabel(
            text="消耗(kcal)",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=self._rgba("#757575"),
            size_hint_y=None,
            height=dp(20),
        ))
        stats_layout.add_widget(burn_box)

        net_box = BoxLayout(orientation="vertical")
        net_color = "#F44336" if net > 0 else "#4CAF50"
        net_box.add_widget(MDLabel(
            text=str(int(net)),
            font_style="H5",
            theme_text_color="Custom",
            text_color=self._rgba(net_color),
            bold=True,
            size_hint_y=None,
            height=dp(30),
        ))
        net_box.add_widget(MDLabel(
            text="净热量(kcal)",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=self._rgba("#757575"),
            size_hint_y=None,
            height=dp(20),
        ))
        stats_layout.add_widget(net_box)

        overview_layout.add_widget(stats_layout)
        overview_card.add_widget(overview_layout)
        container.add_widget(overview_card)

        # 快捷操作按钮
        actions_card = MDCard(
            size_hint_y=None,
            height=dp(80),
            radius=dp(12),
            elevation=2,
            padding=dp(12),
            md_bg_color=self._rgba("#FFFFFF"),
        )
        actions_layout = BoxLayout(orientation="horizontal", spacing=dp(8))

        food_btn = MDRaisedButton(
            text="记录饮食",
            md_bg_color=self._rgba("#4CAF50"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_x=0.33,
            on_release=lambda x: self.go_to_food(),
        )
        actions_layout.add_widget(food_btn)

        exercise_btn = MDRaisedButton(
            text="记录运动",
            md_bg_color=self._rgba("#2196F3"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_x=0.33,
            on_release=lambda x: self.go_to_exercise(),
        )
        actions_layout.add_widget(exercise_btn)

        plan_btn = MDRaisedButton(
            text="查看计划",
            md_bg_color=self._rgba("#FF9800"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_x=0.33,
            on_release=lambda x: self.go_to_plan(),
        )
        actions_layout.add_widget(plan_btn)

        actions_card.add_widget(actions_layout)
        container.add_widget(actions_card)

        # 今日饮食记录
        container.add_widget(MDLabel(
            text="今日饮食",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        meals = database.get_today_meals(self.today_str)
        if not meals:
            no_meal_card = MDCard(
                size_hint_y=None,
                height=dp(60),
                radius=dp(8),
                elevation=1,
                padding=dp(12),
                md_bg_color=self._rgba("#F5F5F5"),
            )
            no_meal_card.add_widget(MDLabel(
                text="还没有记录，点击上方按钮添加",
                theme_text_color="Custom",
                text_color=self._rgba("#9E9E9E"),
                size_hint_y=None,
                height=dp(40),
            ))
            container.add_widget(no_meal_card)
        else:
            for meal in meals[:5]:
                # 创建可滑动删除的卡片
                swipe_card = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(50),
                    spacing=dp(4),
                )

                meal_card = MDCard(
                    size_hint_x=0.85,
                    radius=dp(8),
                    elevation=1,
                    padding=[dp(12), dp(8)],
                    md_bg_color=self._rgba("#FFFFFF"),
                )
                meal_layout = BoxLayout(orientation="horizontal")
                meal_layout.add_widget(MDLabel(
                    text=f"{meal['meal_type']} - {meal['food_name']}",
                    size_hint_x=0.6,
                ))
                meal_layout.add_widget(MDLabel(
                    text=f"{int(meal['calories'])} kcal",
                    theme_text_color="Custom",
                    text_color=self._rgba("#4CAF50"),
                    size_hint_x=0.4,
                    halign="right",
                ))
                meal_card.add_widget(meal_layout)

                # 删除按钮
                del_btn = MDRaisedButton(
                    text="删除",
                    size_hint_x=0.15,
                    md_bg_color=self._rgba("#F44336"),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, mid=meal['id']: self._confirm_delete("meal", mid),
                )

                swipe_card.add_widget(meal_card)
                swipe_card.add_widget(del_btn)
                container.add_widget(swipe_card)

        # 今日运动记录
        container.add_widget(MDLabel(
            text="今日运动",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#2196F3"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        exercises = database.get_today_exercises(self.today_str)
        if not exercises:
            no_exercise_card = MDCard(
                size_hint_y=None,
                height=dp(60),
                radius=dp(8),
                elevation=1,
                padding=dp(12),
                md_bg_color=self._rgba("#F5F5F5"),
            )
            no_exercise_card.add_widget(MDLabel(
                text="还没有运动记录",
                theme_text_color="Custom",
                text_color=self._rgba("#9E9E9E"),
                size_hint_y=None,
                height=dp(40),
            ))
            container.add_widget(no_exercise_card)
        else:
            for ex in exercises[:5]:
                # 创建可删除的卡片
                swipe_card = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(50),
                    spacing=dp(4),
                )

                ex_card = MDCard(
                    size_hint_x=0.85,
                    radius=dp(8),
                    elevation=1,
                    padding=[dp(12), dp(8)],
                    md_bg_color=self._rgba("#FFFFFF"),
                )
                ex_layout = BoxLayout(orientation="horizontal")
                ex_layout.add_widget(MDLabel(
                    text=f"{ex['exercise_type']} - {ex['duration']}分钟",
                    size_hint_x=0.6,
                ))
                ex_layout.add_widget(MDLabel(
                    text=f"{int(ex['calories_burned'])} kcal",
                    theme_text_color="Custom",
                    text_color=self._rgba("#2196F3"),
                    size_hint_x=0.4,
                    halign="right",
                ))
                ex_card.add_widget(ex_layout)

                # 删除按钮
                del_btn = MDRaisedButton(
                    text="删除",
                    size_hint_x=0.15,
                    md_bg_color=self._rgba("#F44336"),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, eid=ex['id']: self._confirm_delete("exercise", eid),
                )

                swipe_card.add_widget(ex_card)
                swipe_card.add_widget(del_btn)
                container.add_widget(swipe_card)

        # 显示热量换算 - 净热量对应的体重变化
        if today_log:
            net = today_log["total_intake"] - today_log["total_burned"]
            weight_change = net / 7700  # 7700 kcal = 1kg fat
            if net != 0:
                change_color = "#F44336" if net > 0 else "#4CAF50"
                change_text = f"+{weight_change:.3f}" if weight_change > 0 else f"{weight_change:.3f}"
                change_hint = "增重" if net > 0 else "减重"

                container.add_widget(MDLabel(
                    text="热量换算",
                    font_style="H6",
                    theme_text_color="Custom",
                    text_color=self._rgba("#FF9800"),
                    bold=True,
                    size_hint_y=None,
                    height=dp(40),
                ))

                calc_card = MDCard(
                    size_hint_y=None,
                    height=dp(70),
                    radius=dp(8),
                    elevation=1,
                    padding=dp(12),
                    md_bg_color=self._rgba("#FFF3E0"),
                )
                calc_layout = BoxLayout(orientation="vertical", spacing=dp(4))
                calc_layout.add_widget(MDLabel(
                    text=f"净热量: {int(net)} kcal",
                    font_style="Body1",
                    size_hint_y=None,
                    height=dp(25),
                ))
                calc_layout.add_widget(MDLabel(
                    text=f"预计体重变化: {change_text} kg ({change_hint})",
                    font_style="H6",
                    theme_text_color="Custom",
                    text_color=self._rgba(change_color),
                    size_hint_y=None,
                    height=dp(30),
                ))
                calc_card.add_widget(calc_layout)
                container.add_widget(calc_card)

    def _confirm_delete(self, record_type, record_id):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(12), dp(20), dp(12)],
        )

        content.add_widget(MDLabel(
            text="确定要删除这条记录吗？",
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(30),
        ))

        btn_layout = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(12))
        cancel_btn = MDFlatButton(text="取消")
        confirm_btn = MDFlatButton(
            text="删除",
            theme_text_color="Custom",
            text_color=self._rgba("#F44336"),
        )
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(confirm_btn)
        content.add_widget(btn_layout)

        popup = Popup(
            title="确认删除",
            content=content,
            size_hint=(0.8, None),
            height=dp(150),
            auto_dismiss=False,
        )

        cancel_btn.bind(on_release=lambda *_: popup.dismiss())
        confirm_btn.bind(on_release=lambda *_: self._do_delete(record_type, record_id, popup))
        popup.open()

    def _do_delete(self, record_type, record_id, popup):
        if record_type == "meal":
            database.delete_meal(record_id)
        elif record_type == "exercise":
            database.delete_exercise(record_id)
        popup.dismiss()
        self.refresh_home()

    def _rgba(self, hex_color):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1,)

    def go_home(self):
        self.root.current = "home"
        self.refresh_home()
        self._update_nav_color("home")

    def go_to_food(self):
        self.root.current = "food"
        self.refresh_food()
        self._update_nav_color("food")

    def go_to_exercise(self):
        self.root.current = "exercise"
        self.refresh_exercise()
        self._update_nav_color("exercise")

    def go_to_plan(self):
        self.root.current = "plan"
        self.refresh_plan()
        self._update_nav_color("plan")

    def go_to_calendar(self):
        self.root.current = "calendar"
        self.refresh_calendar()
        self._update_nav_color("calendar")

    def go_to_settings(self):
        self.root.current = "settings"
        self.refresh_settings()

    def _update_nav_color(self, active):
        pass

    # ── Calendar ──────────────────────────────────────────────
    def refresh_calendar(self):
        screen = self.root.get_screen("calendar")
        container = screen.ids.calendar_container
        container.clear_widgets()

        # 日期选择
        date_label = MDLabel(
            text=f"选中日期: {self.selected_date}",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#FF9800"),
            size_hint_y=None,
            height=dp(40),
        )
        container.add_widget(date_label)

        # 日历组件
        calendar = CalendarWidget(
            size_hint_y=None,
            height=dp(380),
        )
        calendar.selected_date = self.selected_date
        calendar.on_date_select = self._on_calendar_date_select
        container.add_widget(calendar)

        # 当天记录
        container.add_widget(MDLabel(
            text="当天记录",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#FF9800"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        # 饮食记录
        meals = database.get_today_meals(self.selected_date)
        if meals:
            container.add_widget(MDLabel(
                text="饮食",
                font_style="Subtitle1",
                size_hint_y=None,
                height=dp(25),
            ))
            for meal in meals:
                meal_card = MDCard(
                    size_hint_y=None,
                    height=dp(40),
                    radius=dp(6),
                    elevation=1,
                    padding=[dp(10), dp(4)],
                    md_bg_color=self._rgba("#FFFFFF"),
                )
                meal_card.add_widget(MDLabel(
                    text=f"{meal['meal_type']} - {meal['food_name']}: {int(meal['calories'])} kcal",
                    font_style="Body2",
                ))
                container.add_widget(meal_card)

        # 运动记录
        exercises = database.get_today_exercises(self.selected_date)
        if exercises:
            container.add_widget(MDLabel(
                text="运动",
                font_style="Subtitle1",
                size_hint_y=None,
                height=dp(25),
            ))
            for ex in exercises:
                ex_card = MDCard(
                    size_hint_y=None,
                    height=dp(40),
                    radius=dp(6),
                    elevation=1,
                    padding=[dp(10), dp(4)],
                    md_bg_color=self._rgba("#FFFFFF"),
                )
                ex_card.add_widget(MDLabel(
                    text=f"{ex['exercise_type']}: {ex['duration']}分钟, {int(ex['calories_burned'])} kcal",
                    font_style="Body2",
                ))
                container.add_widget(ex_card)

        # 当日汇总
        daily_log = database.get_daily_log(self.selected_date)
        if daily_log:
            summary_card = MDCard(
                size_hint_y=None,
                height=dp(80),
                radius=dp(12),
                elevation=2,
                padding=dp(12),
                md_bg_color=self._rgba("#E8F5E9"),
            )
            summary_layout = BoxLayout(orientation="vertical", spacing=dp(4))
            summary_layout.add_widget(MDLabel(
                text=f"摄入: {int(daily_log['total_intake'])} kcal  |  消耗: {int(daily_log['total_burned'])} kcal",
                font_style="Body1",
                size_hint_y=None,
                height=dp(25),
            ))
            net = daily_log['total_intake'] - daily_log['total_burned']
            net_color = "#F44336" if net > 0 else "#4CAF50"
            summary_layout.add_widget(MDLabel(
                text=f"净热量: {int(net)} kcal",
                font_style="H6",
                theme_text_color="Custom",
                text_color=self._rgba(net_color),
                size_hint_y=None,
                height=dp(30),
            ))
            summary_card.add_widget(summary_layout)
            container.add_widget(summary_card)

    def _on_calendar_date_select(self, date_str):
        self.selected_date = date_str
        self.refresh_calendar()

    # ── Food Diary ────────────────────────────────────────────
    def refresh_food(self):
        screen = self.root.get_screen("food")
        container = screen.ids.food_container
        container.clear_widgets()

        camera_btn = MDRaisedButton(
            text="拍照识别食物",
            md_bg_color=self._rgba("#4CAF50"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self._take_photo(),
        )
        container.add_widget(camera_btn)

        manual_btn = MDRaisedButton(
            text="手动添加",
            md_bg_color=self._rgba("#2196F3"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self.show_add_food_dialog(),
        )
        container.add_widget(manual_btn)

        container.add_widget(MDLabel(
            text="今日饮食记录",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        meals = database.get_today_meals(self.today_str)
        if not meals:
            container.add_widget(MDLabel(
                text="还没有记录",
                theme_text_color="Custom",
                text_color=self._rgba("#9E9E9E"),
                size_hint_y=None,
                height=dp(60),
            ))
        else:
            total_calories = sum(m['calories'] for m in meals)
            container.add_widget(MDLabel(
                text=f"总计: {int(total_calories)} kcal",
                font_style="H6",
                theme_text_color="Custom",
                text_color=self._rgba("#FF9800"),
                size_hint_y=None,
                height=dp(30),
            ))
            for meal in meals:
                # 可删除的卡片
                swipe_card = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(70),
                    spacing=dp(4),
                )

                meal_card = MDCard(
                    size_hint_x=0.85,
                    radius=dp(8),
                    elevation=1,
                    padding=dp(12),
                    md_bg_color=self._rgba("#FFFFFF"),
                )
                meal_layout = BoxLayout(orientation="vertical", spacing=dp(4))
                meal_layout.add_widget(MDLabel(
                    text=f"{meal['meal_type']} - {meal['food_name']}",
                    font_style="Subtitle1",
                    size_hint_y=None,
                    height=dp(25),
                ))
                meal_info = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(25))
                meal_info.add_widget(MDLabel(
                    text=f"蛋白质: {meal.get('protein', 0):.1f}g  碳水: {meal.get('carbs', 0):.1f}g  脂肪: {meal.get('fat', 0):.1f}g",
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=self._rgba("#757575"),
                ))
                meal_info.add_widget(MDLabel(
                    text=f"{int(meal['calories'])} kcal",
                    theme_text_color="Custom",
                    text_color=self._rgba("#4CAF50"),
                    bold=True,
                    halign="right",
                ))
                meal_layout.add_widget(meal_info)
                meal_card.add_widget(meal_layout)

                # 删除按钮
                del_btn = MDRaisedButton(
                    text="删除",
                    size_hint_x=0.15,
                    md_bg_color=self._rgba("#F44336"),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, mid=meal['id']: self._confirm_delete("meal", mid),
                )

                swipe_card.add_widget(meal_card)
                swipe_card.add_widget(del_btn)
                container.add_widget(swipe_card)

    def _take_photo(self):
        """拍照识别食物 - 直接打开系统相机"""
        if self._is_android():
            self._request_camera()
        else:
            # 桌面环境用文件选择器调试
            self._open_file_chooser()

    def _is_android(self):
        """判断是否运行在 Android 环境"""
        try:
            import android  # noqa: F401
            return True
        except ImportError:
            try:
                import jnius  # noqa: F401
                # 如果有 jnius 且系统是 Linux，也可能是 Android
                import platform
                return platform.system() == "Linux"
            except ImportError:
                return False

    def _request_camera(self):
        """请求相机权限（Android 6+ 需要运行时权限）"""
        try:
            from android.permissions import request_permissions, \
                Permission, check_permission
            if check_permission(Permission.CAMERA):
                self._start_camera()
            else:
                def on_permissions(permissions, results):
                    if results and all(results):
                        self._start_camera()
                    else:
                        self._show_error_popup("需要「相机」权限才能拍照识别食物\n请在系统设置中开启相机权限")
                request_permissions([Permission.CAMERA], on_permissions)
        except ImportError:
            # 非 Android 或有异常时直接尝试
            self._start_camera()

    def _start_camera(self):
        """打开系统相机拍照"""
        import datetime
        from plyer import camera

        # 照片保存目录（公共 Pictures 目录，相机 APP 需要有写入权限）
        photo_dir = "/storage/emulated/0/Pictures/FitTracker"
        try:
            os.makedirs(photo_dir, exist_ok=True)
        except Exception:
            # 降级到应用私有目录
            photo_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "photos"
            )
            os.makedirs(photo_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(photo_dir, f"food_{timestamp}.jpg")

        try:
            print(f"[Camera] Opening camera, save to: {filename}")
            self._camera_file = filename  # 防止 GC
            camera.take_picture(filename, self._on_camera_complete)
        except Exception as e:
            print(f"[Camera] Failed to open camera: {e}")
            self._show_error_popup("无法打开相机，请确保已授予相机权限")

    def _on_camera_complete(self, image_path):
        """相机拍照结束回调"""
        from kivy.clock import Clock
        print(f"[Camera] Callback with: {image_path}")
        if image_path and os.path.exists(str(image_path)):
            Clock.schedule_once(
                lambda dt: self._show_recognition_result(str(image_path)), 0
            )
        else:
            Clock.schedule_once(
                lambda dt: self._show_error_popup("拍照取消或失败，请重试"), 0
            )

    def _show_error_popup(self, message):
        """通用错误提示弹窗"""
        from kivy.uix.popup import Popup
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(12), dp(20), dp(12)],
        )
        content.add_widget(MDLabel(
            text=message,
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(40),
        ))
        btn_layout = BoxLayout(size_hint_y=None, height=dp(44))
        ok_btn = MDFlatButton(text="确定", size_hint_x=0.5)
        btn_layout.add_widget(ok_btn)
        content.add_widget(btn_layout)
        popup = Popup(
            title="提示",
            content=content,
            size_hint=(0.8, None),
            height=dp(160),
            auto_dismiss=False,
        )
        ok_btn.bind(on_release=lambda *_: popup.dismiss())
        popup.open()

    def _open_file_chooser(self):
        """（桌面调试用）从文件选择图片"""
        from kivy.uix.filechooser import FileChooserIconView
        from kivy.uix.popup import Popup
        import platform

        system = platform.system()
        if system == "Windows":
            initial_path = "C:/Users"
        else:
            initial_path = "/storage/emulated/0"
            if os.path.exists("/storage/emulated/0/DCIM"):
                initial_path = "/storage/emulated/0/DCIM"

        content = BoxLayout(orientation='vertical')

        filechooser = FileChooserIconView(
            path=initial_path,
            filters=['*.png', '*.jpg', '*.jpeg'],
            size_hint_y=0.85,
        )
        content.add_widget(filechooser)

        btn_layout = BoxLayout(size_hint_y=0.15, spacing=dp(10), padding=dp(10))
        cancel_btn = MDFlatButton(text='取消', size_hint_x=0.5)
        select_btn = MDFlatButton(text='识别', size_hint_x=0.5,
                                  md_bg_color=self._rgba("#4CAF50"),
                                  theme_text_color="Custom",
                                  text_color=(1, 1, 1, 1))
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(select_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='选择食物图片', content=content,
                      size_hint=(0.95, 0.9), auto_dismiss=False)

        def select_image(*args):
            if filechooser.selection:
                image_path = filechooser.selection[0]
                popup.dismiss()
                self._show_recognition_result(image_path)

        cancel_btn.bind(on_release=lambda *_: popup.dismiss())
        select_btn.bind(on_release=select_image)
        popup.open()

    def _show_recognition_result(self, image_path):
        import threading

        # 创建加载提示
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(12), dp(20), dp(12)],
        )

        loading_label = MDLabel(
            text="正在识别食物...",
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(30),
        )
        content.add_widget(loading_label)

        self.food_popup = Popup(
            title="AI识别中",
            content=content,
            size_hint=(0.9, None),
            height=dp(200),
            auto_dismiss=False,
        )
        self.food_popup.open()

        def recognize_in_thread():
            try:
                from food_recognition import recognize_food, get_food_calories
                result = recognize_food(image_path)

                if result and result.get('name'):
                    food_name = result['name']
                    calories = result.get('calories', 0)
                    if calories == 0:
                        calories = get_food_calories(food_name)
                else:
                    # 识别失败，降级到本地查询
                    food_name = "未知食物"
                    calories = 100

                # 在主线程更新UI
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self._update_food_popup(food_name, calories, image_path), 0)

            except Exception as e:
                print(f"识别出错: {e}")
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self._update_food_popup("未知食物", 100, image_path), 0)

        threading.Thread(target=recognize_in_thread, daemon=True).start()

    def _update_food_popup(self, food_name, calories, image_path):
        # 关闭加载提示，显示识别结果
        self.food_popup.dismiss()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(12), dp(20), dp(12)],
        )

        content.add_widget(MDLabel(
            text=f"识别结果: {food_name}",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            size_hint_y=None,
            height=dp(30),
        ))

        content.add_widget(MDLabel(
            text=f"预估热量: {int(calories)} 千卡/100g",
            font_style="Body1",
            size_hint_y=None,
            height=dp(25),
        ))

        # 餐次选择
        meal_types = ["早餐", "午餐", "晚餐", "加餐"]
        meal_type_layout = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(40))
        self.meal_type_buttons = []
        for mt in meal_types:
            btn = MDFlatButton(
                text=mt,
                size_hint_x=0.25,
                on_release=lambda x, t=mt: self._select_meal_type(t),
            )
            self.meal_type_buttons.append(btn)
            meal_type_layout.add_widget(btn)
        content.add_widget(meal_type_layout)

        self.food_name_input = TextInput(
            text=food_name,
            multiline=False,
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        content.add_widget(self.food_name_input)

        self.food_calories_input = TextInput(
            text=str(int(calories)),
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        content.add_widget(self.food_calories_input)

        btn_layout = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(12))
        cancel_btn = MDFlatButton(text="取消")
        add_btn = MDFlatButton(
            text="添加",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
        )
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(add_btn)
        content.add_widget(btn_layout)

        self.food_popup = Popup(
            title="添加饮食记录",
            content=content,
            size_hint=(0.9, None),
            height=dp(320),
            auto_dismiss=False,
        )

        cancel_btn.bind(on_release=lambda *_: self.food_popup.dismiss())
        add_btn.bind(on_release=lambda *_: self._add_food())
        self.food_popup.open()
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(12), dp(20), dp(12)],
        )

        meal_types = ["早餐", "午餐", "晚餐", "加餐"]
        meal_type_layout = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(40))
        self.meal_type_buttons = []
        for mt in meal_types:
            btn = MDFlatButton(
                text=mt,
                size_hint_x=0.25,
                on_release=lambda x, t=mt: self._select_meal_type(t),
            )
            self.meal_type_buttons.append(btn)
            meal_type_layout.add_widget(btn)
        content.add_widget(meal_type_layout)

        self.food_name_input = TextInput(
            hint_text="食物名称",
            multiline=False,
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        content.add_widget(self.food_name_input)

        self.food_calories_input = TextInput(
            hint_text="热量(千卡)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        content.add_widget(self.food_calories_input)

        btn_layout = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(12))
        cancel_btn = MDFlatButton(text="取消")
        add_btn = MDFlatButton(
            text="添加",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
        )
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(add_btn)
        content.add_widget(btn_layout)

        self.food_popup = Popup(
            title="添加饮食记录",
            content=content,
            size_hint=(0.9, None),
            height=dp(300),
            auto_dismiss=False,
        )

        cancel_btn.bind(on_release=lambda *_: self.food_popup.dismiss())
        add_btn.bind(on_release=lambda *_: self._add_food())
        self.food_popup.open()

    def show_add_food_dialog(self):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(12), dp(20), dp(12)],
        )

        meal_types = ["早餐", "午餐", "晚餐", "加餐"]
        meal_type_layout = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(40))
        self.meal_type_buttons = []
        for mt in meal_types:
            btn = MDFlatButton(
                text=mt,
                size_hint_x=0.25,
                on_release=lambda x, t=mt: self._select_meal_type(t),
            )
            self.meal_type_buttons.append(btn)
            meal_type_layout.add_widget(btn)
        content.add_widget(meal_type_layout)

        self.food_name_input = TextInput(
            hint_text="食物名称",
            multiline=False,
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        content.add_widget(self.food_name_input)

        self.food_calories_input = TextInput(
            hint_text="热量(千卡)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        content.add_widget(self.food_calories_input)

        btn_layout = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(12))
        cancel_btn = MDFlatButton(text="取消")
        add_btn = MDFlatButton(
            text="添加",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
        )
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(add_btn)
        content.add_widget(btn_layout)

        self.food_popup = Popup(
            title="添加饮食记录",
            content=content,
            size_hint=(0.9, None),
            height=dp(300),
            auto_dismiss=False,
        )

        cancel_btn.bind(on_release=lambda *_: self.food_popup.dismiss())
        add_btn.bind(on_release=lambda *_: self._add_food())
        self.food_popup.open()

    def _select_meal_type(self, meal_type):
        self.selected_meal_type = meal_type
        for btn in self.meal_type_buttons:
            if btn.text == meal_type:
                btn.md_bg_color = self._rgba("#4CAF50")
                btn.theme_text_color = "Custom"
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.md_bg_color = self._rgba("#F5F5F5")
                btn.theme_text_color = "Custom"
                btn.text_color = self._rgba("#757575")

    def _add_food(self):
        food_name = self.food_name_input.text.strip()
        try:
            calories = float(self.food_calories_input.text)
        except ValueError:
            calories = 0

        if food_name and calories > 0:
            meal_type = getattr(self, 'selected_meal_type', '午餐')
            database.add_meal(self.today_str, meal_type, food_name, calories)
            self.food_popup.dismiss()
            self.refresh_food()

    # ── Exercise Log ──────────────────────────────────────────
    def refresh_exercise(self):
        screen = self.root.get_screen("exercise")
        container = screen.ids.exercise_container
        container.clear_widgets()

        exercise_types = [
            ("walking_moderate", "快走", 3.5),
            ("running_slow", "慢跑", 8.0),
            ("running_moderate", "中速跑", 9.8),
            ("cycling_moderate", "骑行", 6.0),
            ("swimming_moderate", "游泳", 7.0),
            ("strength_training", "力量训练", 5.0),
            ("yoga", "瑜伽", 3.0),
            ("jumping_rope", "跳绳", 12.0),
        ]

        container.add_widget(MDLabel(
            text="选择运动类型",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#2196F3"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        # 用GridLayout替代BoxLayout，4列2行
        grid = GridLayout(
            cols=4,
            rows=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(120),
            padding=dp(4),
        )

        self.exercise_type_buttons = []
        selected_type = getattr(self, 'selected_exercise_type', None)

        for etype, name, met in exercise_types:
            btn = MDRaisedButton(
                text=f"{name}\nMET:{met}",
                size_hint_y=None,
                height=dp(50),
                on_release=lambda x, t=etype, n=name, m=met: self._select_exercise_type(t, n, m),
            )
            # 如果是已选中的类型，高亮显示
            if etype == selected_type:
                btn.md_bg_color = self._rgba("#2196F3")
                btn.theme_text_color = "Custom"
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.md_bg_color = self._rgba("#E0E0E0")
            self.exercise_type_buttons.append((etype, btn))
            grid.add_widget(btn)

        container.add_widget(grid)

        container.add_widget(MDLabel(
            text="运动时长(分钟)",
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(30),
        ))

        self.exercise_duration_input = TextInput(
            hint_text="30",
            multiline=False,
            input_filter="int",
            text="30",
            size_hint_y=None,
            height=dp(44),
            font_size=dp(16),
        )
        container.add_widget(self.exercise_duration_input)

        add_btn = MDRaisedButton(
            text="添加运动记录",
            md_bg_color=self._rgba("#2196F3"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self._add_exercise(),
        )
        container.add_widget(add_btn)

        container.add_widget(MDLabel(
            text="今日运动记录",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#2196F3"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        exercises = database.get_today_exercises(self.today_str)
        if not exercises:
            container.add_widget(MDLabel(
                text="还没有运动记录",
                theme_text_color="Custom",
                text_color=self._rgba("#9E9E9E"),
                size_hint_y=None,
                height=dp(60),
            ))
        else:
            total_burned = sum(e['calories_burned'] for e in exercises)
            container.add_widget(MDLabel(
                text=f"总计消耗: {int(total_burned)} kcal",
                font_style="H6",
                theme_text_color="Custom",
                text_color=self._rgba("#FF9800"),
                size_hint_y=None,
                height=dp(30),
            ))
            for ex in exercises:
                # 可删除的卡片
                swipe_card = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(50),
                    spacing=dp(4),
                )

                ex_card = MDCard(
                    size_hint_x=0.85,
                    radius=dp(8),
                    elevation=1,
                    padding=[dp(12), dp(8)],
                    md_bg_color=self._rgba("#FFFFFF"),
                )
                ex_layout = BoxLayout(orientation="horizontal")
                ex_layout.add_widget(MDLabel(
                    text=f"{ex['exercise_type']} - {ex['duration']}分钟",
                    size_hint_x=0.6,
                ))
                ex_layout.add_widget(MDLabel(
                    text=f"{int(ex['calories_burned'])} kcal",
                    theme_text_color="Custom",
                    text_color=self._rgba("#2196F3"),
                    size_hint_x=0.4,
                    halign="right",
                ))
                ex_card.add_widget(ex_layout)

                # 删除按钮
                del_btn = MDRaisedButton(
                    text="删除",
                    size_hint_x=0.15,
                    md_bg_color=self._rgba("#F44336"),
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x, eid=ex['id']: self._confirm_delete("exercise", eid),
                )

                swipe_card.add_widget(ex_card)
                swipe_card.add_widget(del_btn)
                container.add_widget(swipe_card)

    def _select_exercise_type(self, etype, name, met):
        self.selected_exercise_type = etype
        self.selected_exercise_name = name
        self.selected_exercise_met = met

        # 更新按钮高亮
        if hasattr(self, 'exercise_type_buttons'):
            for btn_type, btn in self.exercise_type_buttons:
                if btn_type == etype:
                    btn.md_bg_color = self._rgba("#2196F3")
                    btn.theme_text_color = "Custom"
                    btn.text_color = (1, 1, 1, 1)
                else:
                    btn.md_bg_color = self._rgba("#E0E0E0")
                    btn.theme_text_color = "Custom"
                    btn.text_color = self._rgba("#757575")

    def _add_exercise(self):
        etype = getattr(self, 'selected_exercise_type', None)
        met = getattr(self, 'selected_exercise_met', 4.0)

        try:
            duration = int(self.exercise_duration_input.text)
        except ValueError:
            duration = 30

        if etype and duration > 0:
            user_data = database.get_user_profile()
            weight = user_data["weight"] if user_data else 70

            calories = met * weight * (duration / 60)
            database.add_exercise(self.today_str, etype, duration, calories)
            self.refresh_exercise()

    # ── Plan ──────────────────────────────────────────────────
    def refresh_plan(self):
        screen = self.root.get_screen("plan")
        container = screen.ids.plan_container
        container.clear_widgets()

        user_data = database.get_user_profile()

        container.add_widget(MDLabel(
            text="个人数据",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#FF9800"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        height_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44))
        height_layout.add_widget(MDLabel(text="身高(cm):", size_hint_x=0.4))
        self.height_input = TextInput(
            text=str(user_data["height"]) if user_data else "170",
            multiline=False,
            input_filter="float",
            size_hint_x=0.6,
            font_size=dp(16),
        )
        height_layout.add_widget(self.height_input)
        container.add_widget(height_layout)

        weight_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44))
        weight_layout.add_widget(MDLabel(text="体重(kg):", size_hint_x=0.4))
        self.weight_input = TextInput(
            text=str(user_data["weight"]) if user_data else "70",
            multiline=False,
            input_filter="float",
            size_hint_x=0.6,
            font_size=dp(16),
        )
        weight_layout.add_widget(self.weight_input)
        container.add_widget(weight_layout)

        age_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44))
        age_layout.add_widget(MDLabel(text="年龄:", size_hint_x=0.4))
        self.age_input = TextInput(
            text=str(user_data["age"]) if user_data else "30",
            multiline=False,
            input_filter="int",
            size_hint_x=0.6,
            font_size=dp(16),
        )
        age_layout.add_widget(self.age_input)
        container.add_widget(age_layout)

        gender_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44))
        gender_layout.add_widget(MDLabel(text="性别:", size_hint_x=0.4))
        self.gender_male_btn = MDRaisedButton(
            text="男",
            size_hint_x=0.3,
            on_release=lambda x: self._select_gender("male"),
        )
        self.gender_female_btn = MDRaisedButton(
            text="女",
            size_hint_x=0.3,
            md_bg_color=self._rgba("#E0E0E0"),
            on_release=lambda x: self._select_gender("female"),
        )
        # 默认选中男性
        self.selected_gender = "male"
        gender_layout.add_widget(self.gender_male_btn)
        gender_layout.add_widget(self.gender_female_btn)
        container.add_widget(gender_layout)

        target_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(44))
        target_layout.add_widget(MDLabel(text="目标体重(kg):", size_hint_x=0.4))
        self.target_input = TextInput(
            text=str(user_data["target_weight"]) if user_data and user_data.get("target_weight") else "65",
            multiline=False,
            input_filter="float",
            size_hint_x=0.6,
            font_size=dp(16),
        )
        target_layout.add_widget(self.target_input)
        container.add_widget(target_layout)

        save_btn = MDRaisedButton(
            text="保存并生成计划",
            md_bg_color=self._rgba("#FF9800"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self._save_plan(),
        )
        container.add_widget(save_btn)

        plan = database.get_active_plan()
        if plan:
            container.add_widget(MDLabel(
                text="当前计划",
                font_style="H6",
                theme_text_color="Custom",
                text_color=self._rgba("#4CAF50"),
                bold=True,
                size_hint_y=None,
                height=dp(40),
            ))

            plan_card = MDCard(
                size_hint_y=None,
                height=dp(150),
                radius=dp(12),
                elevation=2,
                padding=dp(16),
                md_bg_color=self._rgba("#FFFFFF"),
            )
            plan_layout = BoxLayout(orientation="vertical", spacing=dp(8))
            plan_layout.add_widget(MDLabel(
                text=f"每日目标: {int(plan['daily_calorie_target'])} kcal",
                font_style="Subtitle1",
                size_hint_y=None,
                height=dp(30),
            ))
            plan_layout.add_widget(MDLabel(
                text=f"目标体重: {plan['target_weight']} kg",
                size_hint_y=None,
                height=dp(25),
            ))
            plan_layout.add_widget(MDLabel(
                text=f"蛋白质: {plan['protein_percent']}%  碳水: {plan['carbs_percent']}%  脂肪: {plan['fat_percent']}%",
                theme_text_color="Custom",
                text_color=self._rgba("#757575"),
                size_hint_y=None,
                height=dp(25),
            ))
            plan_card.add_widget(plan_layout)
            container.add_widget(plan_card)

    def _select_gender(self, gender):
        self.selected_gender = gender
        if gender == "male":
            self.gender_male_btn.md_bg_color = self._rgba("#4CAF50")
            self.gender_male_btn.theme_text_color = "Custom"
            self.gender_male_btn.text_color = (1, 1, 1, 1)
            self.gender_female_btn.md_bg_color = self._rgba("#E0E0E0")
            self.gender_female_btn.theme_text_color = "Custom"
            self.gender_female_btn.text_color = self._rgba("#757575")
        else:
            self.gender_female_btn.md_bg_color = self._rgba("#4CAF50")
            self.gender_female_btn.theme_text_color = "Custom"
            self.gender_female_btn.text_color = (1, 1, 1, 1)
            self.gender_male_btn.md_bg_color = self._rgba("#E0E0E0")
            self.gender_male_btn.theme_text_color = "Custom"
            self.gender_male_btn.text_color = self._rgba("#757575")

    def _save_plan(self):
        try:
            height = float(self.height_input.text)
            weight = float(self.weight_input.text)
            age = int(self.age_input.text)
            target_weight = float(self.target_input.text)
        except ValueError:
            return

        gender = getattr(self, 'selected_gender', 'male')

        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        tdee = bmr * 1.55
        daily_calories = tdee - 500

        database.save_user_profile(height, weight, age, gender, target_weight)

        start_date = datetime.date.today().isoformat()
        end_date = (datetime.date.today() + datetime.timedelta(weeks=12)).isoformat()
        database.save_plan(start_date, end_date, target_weight, daily_calories)

        self.refresh_plan()

    # ── Settings ──────────────────────────────────────────────
    def refresh_settings(self):
        screen = self.root.get_screen("settings")
        container = screen.ids.settings_container
        container.clear_widgets()

        container.add_widget(MDLabel(
            text="个人信息",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        user_data = database.get_user_profile()
        if user_data:
            info_card = MDCard(
                size_hint_y=None,
                height=dp(120),
                radius=dp(12),
                elevation=2,
                padding=dp(16),
                md_bg_color=self._rgba("#FFFFFF"),
            )
            info_layout = BoxLayout(orientation="vertical", spacing=dp(8))
            info_layout.add_widget(MDLabel(
                text=f"身高: {user_data['height']} cm  |  体重: {user_data['weight']} kg",
                size_hint_y=None,
                height=dp(25),
            ))
            info_layout.add_widget(MDLabel(
                text=f"年龄: {user_data['age']} 岁  |  性别: {'男' if user_data['gender'] == 'male' else '女'}",
                size_hint_y=None,
                height=dp(25),
            ))
            if user_data.get('target_weight'):
                info_layout.add_widget(MDLabel(
                    text=f"目标体重: {user_data['target_weight']} kg",
                    theme_text_color="Custom",
                    text_color=self._rgba("#FF9800"),
                    size_hint_y=None,
                    height=dp(25),
                ))
            info_card.add_widget(info_layout)
            container.add_widget(info_card)
        else:
            container.add_widget(MDLabel(
                text="还没有设置个人信息",
                theme_text_color="Custom",
                text_color=self._rgba("#9E9E9E"),
                size_hint_y=None,
                height=dp(60),
            ))

        container.add_widget(MDLabel(
            text="数据管理",
            font_style="H6",
            theme_text_color="Custom",
            text_color=self._rgba("#4CAF50"),
            bold=True,
            size_hint_y=None,
            height=dp(40),
        ))

        clear_btn = MDRaisedButton(
            text="清除所有数据",
            md_bg_color=self._rgba("#F44336"),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self._clear_data(),
        )
        container.add_widget(clear_btn)

    def _clear_data(self):
        database.clear_all_data()
        self.go_home()


if __name__ == "__main__":
    FitTrackerApp().run()
