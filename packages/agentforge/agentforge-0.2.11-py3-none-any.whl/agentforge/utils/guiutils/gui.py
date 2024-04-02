from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)
window_width = 650
label = Label()


@app.route('/layer_update', methods=['POST'])
def layer_update():
    data = request.json
    layer_number = data.get('layer_number')
    message = data.get('message', '')

    kivy_app.update_label(layer_number, message)
    return jsonify({"status": "received"})


def run_flask_app():
    app.run(port=5002, use_reloader=False, threaded=True)


class KivyApp(App):

    def __init__(self, **kwargs):
        super(KivyApp, self).__init__(**kwargs)

        # Initialize each layer's history - 7 items (0) for the console and (1-6) for layers 1 to 6
        self.history = [""] * 7

        # Initialize the GUI Elements
        self.main_layout = None
        self.tab_panel = None
        self.bottom_layout = None
        self.chat = None
        self.send_button = None
        self.tabs = []
        self.views = []
        self.labels = []

    def on_window_resize(self, window, width, height):
        print(f"Window resized to {width}x{height}")
        new_width = width - 20
        for label in self.labels:
            label.text_size = (new_width, None)


    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.tab_panel = TabbedPanel(do_default_tab=False)

        tab_titles = ['Chat', 'Console']

        for i, title in enumerate(tab_titles):
            global window_width
            self.history[i] = f"Listening to Messages...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            view = ScrollView()
            label = Label(
                text=self.history[i],
                size_hint_y=None,
                width=650,
                text_size=(window_width, None),
                halign='left',
                valign='top')

            label.bind(texture_size=label.setter('size'))
            view.add_widget(label)

            self.views.append(view)
            self.labels.append(label)

            # Create and populate the tabs
            tab = TabbedPanelItem(text=title)
            tab.add_widget(self.views[i])
            self.tabs.append(tab)

            # Add tabs to the tab panel
            self.tab_panel.add_widget(self.tabs[i])

        self.main_layout.add_widget(self.tab_panel)

        # Chat and Send button
        self.chat = TextInput(hint_text='Enter a message...')
        self.send_button = Button(text='Send', size_hint_x=None, width=100)
        self.send_button.bind(on_press=self.send_chat_message)

        self.bottom_layout = BoxLayout(size_hint_y=None, height=44)
        self.bottom_layout.add_widget(self.chat)
        self.bottom_layout.add_widget(self.send_button)

        self.main_layout.add_widget(self.bottom_layout)

        Window.bind(on_resize=self.on_window_resize)

        return self.main_layout

    def update_label(self, layer_number, message):
        # Check if the label attribute exists
        if self.labels[layer_number]:
            self.history[layer_number] += message + '\n'
            self.labels[layer_number].text = self.history[layer_number]
        else:
            print(f"Error: Layer {layer_number} does not have a matching label attribute.")

    def send_chat_message(self, instance):
        if self.chat.text:
            data = {
                "layer_number": 0,
                "message": self.chat.text
            }

            # Move the requests.post to a separate thread
            threading.Thread(target=self.send_message_thread, args=(data,)).start()

            # Clear the chat box after sending
            self.chat.text = ''

    def send_message_thread(self, data):
        try:
            self.result = requests.post('http://127.0.0.1:5001/bot', json=data)
            # Handle the response if needed
        except Exception as e:
            # Handle any exceptions here
            print(f"Error: {e}")


if __name__ == '__main__':
    Builder.load_file('kivy_theme.kv')

    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True  # This allows the Flask thread to exit when the main program exits
    flask_thread.start()

    # Run Kivy App
    kivy_app = KivyApp()
    kivy_app.run()