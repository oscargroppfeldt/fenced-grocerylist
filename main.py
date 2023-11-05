from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.popup import Popup

Builder.load_file("main.kv")

class ConfirmPopup(Popup):
    def __init__(self, item_name, item_widget, **kwargs):
        super(ConfirmPopup, self).__init__(**kwargs)
        self.title = "Bekräfta"
        self.content = Label(text=f"Är {item_name} inhandlat?")
        self.size_hint = (None, None)
        self.size = (300, 150)

        self.item_widget = item_widget
        self.item_name = item_name

        button_layout = BoxLayout(orientation='horizontal', spacing=10)
        yes_button = Button(text="Ja")
        no_button = Button(text="Nej")

        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        self.content.add_widget(button_layout)

        yes_button.bind(on_release=self.confirm_remove)
        no_button.bind(on_release=self.dismiss)

        self.has_been_confimed = False

    def confirm_remove(self):
        self.dismiss()
        self.has_been_confimed = True

class GroceryItem(BoxLayout):
    def __init__(self, item_name, checked=False, **kwargs):
        super(GroceryItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.checkbox = CheckBox(active=checked)
        self.label = Label(text=item_name)
        self.checkbox.bind(active=self.on_checkbox_active)
        self.value = checked

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

    def on_checkbox_active(self, instance, value):
        self.value = value


class GroceryListScreen(Screen):
    def __init__(self, **kwargs):
        if "grocery_handler" in kwargs:
            self.grocery_handler = kwargs["grocery_handler"]
            kwargs.pop("grocery_handler")
        super(GroceryListScreen, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.list_label = Label(text="Missing Groceries:")
        self.grocery_display = BoxLayout(orientation='vertical')

        self.layout.add_widget(self.list_label)
        self.layout.add_widget(self.grocery_display)

        self.confirm_removal = Button(text="Remove")
        self.add_widget(self.confirm_removal)
        self.confirm_removal.bind(on_release=self.remove_selection)

        self.add_widget(self.layout)

        self.add_goback = Button(text="Go Back")
        self.add_goback.bind(on_release=self.show_home_screen)
        self.layout.add_widget(self.add_goback)

    def on_pre_enter(self):
        self.update_grocery_display()

    def remove_selection(self):
        confirm_popup = ConfirmPopup()
        if confirm_popup.has_been_confimed:
            self.update_grocery_display()

    def update_grocery_display(self):
        self.grocery_display.clear_widgets()

        for item in self.grocery_handler.get_groceries():
            if not item['checked']:
                grocery_item = GroceryItem(item['name'], checked=item['checked'])
                self.grocery_display.add_widget(grocery_item)

    def show_home_screen(self, instance):
        self.manager.current = 'grocery_app'

class GroceryListApp(Screen):
    def __init__(self, **kwargs):
        if "grocery_handler" in kwargs:
            self.grocery_handler = kwargs["grocery_handler"]
            kwargs.pop("grocery_handler")
        super(GroceryListApp, self).__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.grocery_list = []

        self.title_label = Label(text="Grocery List")
        self.input_text = TextInput(hint_text="Enter missing grocery item")
        self.add_button = Button(text="Add Item")
        self.add_button.bind(on_release=self.add_item)

        self.list_button = Button(text="Missing Groceries")
        self.list_button.bind(on_release=self.show_grocery_list)

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.input_text)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.list_button)

        self.add_widget(self.layout)

    def add_item(self, instance):
        item = self.input_text.text
        if item:
            self.grocery_handler.add_grocery(item)
            self.input_text.text = ""

    def show_grocery_list(self, instance):
        self.manager.current = 'grocery_list_screen'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        grocery_handler = GroceryMemory()
        grocery_app = GroceryListApp(name='grocery_app', grocery_handler=grocery_handler)
        grocery_list_screen = GroceryListScreen(name='grocery_list_screen', grocery_handler=grocery_handler)
        sm.add_widget(grocery_app)
        sm.add_widget(grocery_list_screen)
        return sm

class GroceryMemory:
    def __init__(self):
        self.grocery_list = []

    def get_groceries(self):
        return self.grocery_list

    def add_grocery(self, name):
        self.grocery_list.append({'name': name, 'checked': False})

if __name__ == '__main__':
    MyApp().run()
