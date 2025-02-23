from PyQt5.QtCore import QObject, QEvent, QVariantAnimation, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QWidget

class HoverEffectFilter(QObject):
    """ Global event filter to apply hover effects to buttons & list items """

    def eventFilter(self, obj, event):
        if isinstance(obj, QPushButton):  # If it's a button
            return self.handle_button_hover(obj, event)
        
        return super().eventFilter(obj, event)

    def handle_button_hover(self, button, event):
        """ Handle hover animation for QPushButton """
        if event.type() == QEvent.Enter:
            self.animate_widget(button, True)
        elif event.type() == QEvent.Leave:
            self.animate_widget(button, False)
        return False

    def animate_widget(self, widget, enter):
        """ Animate background color smoothly & store animation inside the widget """
        if not hasattr(widget, "_hover_animation"):  
            widget._hover_animation = QVariantAnimation(widget)  # Store animation in widget

        animation = widget._hover_animation
        animation.setDuration(200)  # Speed of hover effect
        animation.setStartValue(QColor(74, 144, 226) if enter else QColor(227, 229, 232))
        animation.setEndValue(QColor(227, 229, 232) if enter else QColor(74, 144, 226))
        animation.valueChanged.connect(lambda color: self.set_widget_background(widget, color))
        animation.start()

    def set_widget_background(self, widget, color):
        """ Apply background color change """
        widget.setStyleSheet(f"background-color: {color.name()};")
