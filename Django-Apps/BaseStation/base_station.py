class BaseStation:
    
    # Server Configuration functions
    def __init__(self): # Constructor
        self.node_list = []
        self.ssid = None
        self.password = None
        
    def initialize_server(self): # Function to initialize the server
        """ Sets up the server on the RPi to manage local communication between the host and the webapp. """
    
    def launch_webapp(self): # Function to launch the webapp
        """ Launches the webapp in the background on boot. Served locally on the server; accessible via HTTP."""
        
    # Wifi functions   
    def enter_network_mode(self): # Function to enter wifi mode
        """ Puts the server in wifi mode, allowing webapp to run on a local network."""
        
    def enter_access_point_mode(self): # Function to enter access point mode
        """ Puts the server in access point mode, allowing the webapp to run on Rpi's Hotspot."""
    
    def connect_to_wifi(self, ssid, password): # Function to connect to wifi
        """ Connects the server to a wifi network."""
        self.ssid = ssid
        self.password = password
    
    def disconnect_from_wifi(self): # Function to disconnect from wifi
        """ Disconnects the server from a wifi network."""
        self.ssid = None
        self.password = None
    

    
    
    

    # Node functions
    def connect_node(self,node_id): # Function to connect to a new node
        """ Connects to a new node using BLE. Uses the node_id to identify the node."""
    
    def disconnect_node(self,node_id): # Function to disconnect from a node
        """ Disconnects from the node with the given node_id."""
    
    def recieve_ble_data(self): # Function to recieve data from a connected node
        """Listens for incoming data (e.g. sensor data) from a connected node."""
    
    def send_ble_data(self): # Function to send data to a connected node
        """ Sends data to a connected node (e.g. commands for the node)."""
    
    def auto_connect(self): # Function to auto connect to a previously connected node
        """ Automatically connects to a previously connected node."""
    
    
    # WebApp functions
    def send_notification(self,data): # Function to send notification to the webapp
        """ Sends a notification to the webapp via an HTTP POST request, relaying data from the node for user alerts & updates."""

    def process_data_for_webapp(self, data): # Function to process data for the webapp
        """ Processes incoming data from the node, preparing it for HTTP transmission to the webapp via REST API."""
    
    def fetch_webapp_data(self): # Function to fetch data from the webapp
        """ Uses an HTTP GET request to fetch data from the webapp if needed for system status updates."""
    