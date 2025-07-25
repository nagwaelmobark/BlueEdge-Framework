#!/usr/bin/env python3
"""
KIVY Installation Test
=====================

Quick test to verify KIVY installation is working correctly.
"""

try:
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.core.window import Window
    
    print("✅ All KIVY imports successful!")
    
    class TestApp(App):
        def build(self):
            # Set window size for testing
            Window.size = (400, 600)
            
            # Create main layout
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Title
            title = Label(
                text='🔵 BlueEdge Framework\nKIVY Test Successful! ✅',
                font_size='20sp',
                halign='center',
                text_size=(None, None)
            )
            
            # Test button
            test_btn = Button(
                text='KIVY is Working! 🎉',
                size_hint=(1, 0.3),
                font_size='16sp'
            )
            test_btn.bind(on_press=self.on_test_click)
            
            # Add widgets
            layout.add_widget(title)
            layout.add_widget(test_btn)
            
            return layout
        
        def on_test_click(self, instance):
            instance.text = "✅ Ready for BlueEdge Mobile App!"
            print("🎯 KIVY test successful - Ready for mobile development!")
    
    if __name__ == '__main__':
        print("🚀 Starting KIVY test app...")
        TestApp().run()
        
except ImportError as e:
    print(f"❌ KIVY import error: {e}")
    print("Please install KIVY with: pip install kivy[base] kivymd")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your Python installation") 
