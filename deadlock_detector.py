import sys
import networkx as nx
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox
)

class DeadlockDetector:
    def __init__(self):
        self.graph = {}

    def add_process(self, process):
        if process and process not in self.graph:
            self.graph[process] = []

    def add_resource(self, resource):
        if resource and resource not in self.graph:
            self.graph[resource] = []

    def request_resource(self, process, resource):
        """Process requests a resource (P -> R)"""
        if process in self.graph and resource in self.graph:
            self.graph[process].append(resource)

    def allocate_resource(self, resource, process):
        """Resource allocated to process (R -> P)"""
        if resource in self.graph and process in self.graph:
            self.graph[resource].append(process)

    def detect_deadlock(self):
        """Detects deadlock using cycle detection"""
        graph_nx = nx.DiGraph(self.graph)
        try:
            cycle = nx.find_cycle(graph_nx, orientation="original")
            return True, cycle
        except nx.NetworkXNoCycle:
            return False, []

class DeadlockGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.detector = DeadlockDetector()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        self.label = QLabel("<h2>Deadlock Detection Tool</h2>", self)
        layout.addWidget(self.label)

        # Log area
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        # Input fields
        self.process_input = QLineEdit(self)
        self.process_input.setPlaceholderText("Enter process name (e.g., P1)")
        layout.addWidget(self.process_input)

        self.resource_input = QLineEdit(self)
        self.resource_input.setPlaceholderText("Enter resource name (e.g., R1)")
        layout.addWidget(self.resource_input)

        # Buttons
        self.add_process_btn = QPushButton("Add Process", self)
        self.add_process_btn.clicked.connect(self.add_process)
        layout.addWidget(self.add_process_btn)

        self.add_resource_btn = QPushButton("Add Resource", self)
        self.add_resource_btn.clicked.connect(self.add_resource)
        layout.addWidget(self.add_resource_btn)

        self.request_btn = QPushButton("Request Resource (P -> R)", self)
        self.request_btn.clicked.connect(self.request_resource)
        layout.addWidget(self.request_btn)

        self.allocate_btn = QPushButton("Allocate Resource (R -> P)", self)
        self.allocate_btn.clicked.connect(self.allocate_resource)
        layout.addWidget(self.allocate_btn)

        self.check_deadlock_btn = QPushButton("Check Deadlock", self)
        self.check_deadlock_btn.clicked.connect(self.check_deadlock)
        layout.addWidget(self.check_deadlock_btn)

        self.setLayout(layout)
        self.setWindowTitle("Deadlock Detector")
        self.resize(400, 350)

    def log(self, message):
        self.log_area.append(message)

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

    def add_process(self):
        process = self.process_input.text().strip()
        if not process:
            self.show_message("Please enter a process name.")
            return
        self.detector.add_process(process)
        self.log(f"Added Process: {process}")
        self.process_input.clear()

    def add_resource(self):
        resource = self.resource_input.text().strip()
        if not resource:
            self.show_message("Please enter a resource name.")
            return
        self.detector.add_resource(resource)
        self.log(f"Added Resource: {resource}")
        self.resource_input.clear()

    def request_resource(self):
        process = self.process_input.text().strip()
        resource = self.resource_input.text().strip()
        if not process or not resource:
            self.show_message("Enter both Process and Resource names.")
            return
        self.detector.request_resource(process, resource)
        self.log(f"{process} requested {resource}")
        self.process_input.clear()
        self.resource_input.clear()

    def allocate_resource(self):
        resource = self.resource_input.text().strip()
        process = self.process_input.text().strip()
        if not process or not resource:
            self.show_message("Enter both Process and Resource names.")
            return
        self.detector.allocate_resource(resource, process)
        self.log(f"{resource} allocated to {process}")
        self.process_input.clear()
        self.resource_input.clear()

    def check_deadlock(self):
        has_deadlock, cycle = self.detector.detect_deadlock()
        if has_deadlock:
            self.log(f"⚠️ DEADLOCK DETECTED! Cycle: {cycle}")
            self.show_message("Deadlock detected! Check log for details.")
        else:
            self.log("✅ No Deadlock Detected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeadlockGUI()
    window.show()
    sys.exit(app.exec())
