#implementation of the nodes class for the Privacy Dots
import base_station
import time
#can be used to connect to the Base Station from each node.

class PrivacyDotNode:
    def __init__(self, node_id, base_station):
        """
        Initializes the PrivacyDotNode with a given node ID.
        """
        self.node_id = node_id
        self.base_station = base_station
        self.motion_detected = False
        self.connected = False
        self.wifi_mode = None
        self.ssid = None
        self.password = None

    def initialize_connection(self):
        """
        Initializes connection settings for BLE communication with the BaseStation.
        """
        print("Initializing connection settings for BLE communication...")
        # Initialization/connection logic here
        self.connected = True

    def connect_to_base_station(self):
        """
        Establishes a secure BLE connection to the BaseStation using the configured node ID.
        """
        if self.connected:
            print("Connecting to BaseStation...")
            self.base_station.connect_node(self.node_id)
            print(f"Connected to BaseStation with node ID {self.node_id}.")
        else:
            print("Connection initialization required before connecting to BaseStation.")

    def detect_motion(self):
        """
        Simulates detecting motion and sends data to the BaseStation if motion is detected.
        """
        self.motion_detected = True
        print(f"Node {self.node_id} detected motion!")
        self.send_data({"node_id": self.node_id, "motion": self.motion_detected, "Detection_time": self.time})

    def send_data(self, data):
        """
        Transmits data (e.g., motion alerts, sensor status) over BLE to BaseStation.
        """
        if self.connected:
            print(f"Sending data to BaseStation: {data}")
            self.base_station.recieve_ble_data(data)
        else:
            print("Cannot send data, not connected to BaseStation.")

    def receive_command(self, command):
        """
        Listens for and executes commands sent from BaseStation over BLE.
        """
        print(f"Received command from BaseStation: {command}")
        # Command handling logic here

    def wifi_setup(self, mode, ssid, password):
        """
        Configures Wi-Fi settings based on mode (Access Point or Client Mode).
        """
        self.wifi_mode = mode
        self.ssid = ssid
        self.password = password
        print(f"Wi-Fi setup in {mode} mode with SSID '{ssid}'.")
        # Wi-Fi setup logic here

    def access_point_mode(self):
        """
        Initiates the device's own Wi-Fi Access Point for initial setup.
        """
        print("Setting up Wi-Fi Access Point mode...")
        self.wifi_mode = "Access Point"
        # Access Point setup logic here

    def client_mode(self, ssid, password):
        """
        Connects to an existing Wi-Fi network.
        """
        print(f"Connecting to Wi-Fi network '{ssid}'...")
        self.wifi_mode = "Client"
        self.ssid = ssid
        self.password = password
        # Client mode connection logic here

    def self_check(self):
        """
        Runs diagnostics on the PrivacyDotNode to ensure components are operational.
        """
        print("Running self-check diagnostics...")
        # Diagnostics logic here
        ble_status = "Operational"  # Example status
        wifi_status = "Operational" if self.wifi_mode else "Not Configured"
        print(f"BLE Status: {ble_status}, Wi-Fi Status: {wifi_status}")

