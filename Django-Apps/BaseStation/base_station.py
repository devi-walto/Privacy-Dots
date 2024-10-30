import subprocess
import os
import bluetooth # Import pybluez library for Bluetooth communication
import re
class BaseStation:
    
    # Server Configuration functions
    def __init__(self): # Constructor
        self.connected_nodes = {} # Dictionary to store connected nodes
        
        # Wifi Configuration
        self.ssid = None
        self.password = None
        
        # Server status
        self.server_initialized = False
        self.server_running = False
        self.webapp_launched = False
        self.network_mode = False
        self.access_point_mode = False
        
        
        
    def install_dependencies(self):
        """ Installs the necessary dependencies for the BaseStation to run. """
        try:
            # Check if the dependencies.txt file exists
            if not os.path.exists("dependencies.txt") or os.path.exists("requirements.txt"):
                print(" dependencies.txt file not found. Creating one...")
                subprocess.run(["pip", "freeze", ">", "dependencies.txt"], shell=True) # Creates a dependencies.txt file
                
            if os.path.exists("dependencies.txt"):
                print("Installing dependencies...")
                subprocess.run(["pip", "install", "-r", "dependencies.txt"], shell=True)
                
            elif os.path.exists("requirements.txt"):
                print("Installing dependencies...")
                subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True)
            print("Dependencies installed successfully.")
        except Exception as e:
            print(f"Error installing dependencies: {e}") 
        
    def initialize_server(self): # Function to initialize the server
        """ Sets up the server on the RPi to manage local communication between the host and the webapp. """
        try:
             # Step 1: Install dependencies 
            print("Initializing server...")
            self.install_dependencies()
            # Add server initialization code here
            self.server_initialized = True
            print("Server initialized successfully.")
            
            # Step Set up sytemd service to run the server on boot
            service_file = 'etc/systemd/system/base_station.service'
            if not os.path.exists(service_file):
                with open(service_file, 'w') as f:
                    f.write(f"""[Unit]
                                Description=BaseStation Service
                                After=multi-user.target
                                
                                [Service]
                                ExecStart=/usr/bin/python3 /path/to/base_station.py runserver
                                WorkingDirectory= Django-Apps\BaseStation\base_station.py
                                Restart=always
                                
                                [Install]
                                WantedBy=multi-user.target""")
                    
                # Enable the service
                subprocess.run(["sudo", "systemctl", "enable", "base_station.service"], check = True)
                
            # Step 3: Start the server (if not already running)
            subprocess.run(["sudo", "systemctl", "start", "base_station.service"], check = True)
            
            # Mark the server as initialized / running
            self.server_initialized = True
            self.server_running = True
            print("Server initialized and running on boot.")
            
        except Exception as e:
            print(f"Error initializing server: {e}")
            self.server_initialized = False
            self.server_running = False
            
            
    
    def launch_webapp(self): # Function to launch the webapp
        """ Launches the webapp in the background on boot. Served locally on the server; accessible via HTTP."""
        try:
            web_app_path = "path/to/your/webapp" ####### @Diego: Please update this path to the actual path of the webapp
            entry_file = "server.js" ####### @Diego: Please update this to the actual entry file of the webapp
            
            os.chdir(web_app_path) # This line is optional, but it ensures that the webapp is launched from the correct directory
            
            # Start the webapp in the background
            self.webapp_process = subprocess.Popen(
                ["node", entry_file], # Command to start the webapp 
                stdout=subprocess.PIPE, # Redirects standard output to a pipe
                stderr=subprocess.PIPE  # Redirect standard error to a pipe
            )
            
            print("Webapp launched successfully.")
            
        except FileNotFoundError:
            print("Error Node.js or entry file not found. Please check the path to ensure Node.js is installed.")
            
        except Exception as e:
            print(f"Error launching webapp: {e}")
            
    def stop_webapp(self): # Function to stop the webapp
        """ Stops the webapp process if it is running."""
        if self.webapp_process and self.webapp_process.poll() is None:
            self.webapp_process.terminate()
            self.webapp_process.wait()
            print("Webapp stopped successfully.")
            
        else:
            print("Webapp not running.")
            
    # Wifi functions   
    def enter_network_mode(self): # Function to enter wifi mode
        """ Puts the server in wifi mode, allowing webapp to run on a local network."""
        if not self.ssid or not self.password:
            print("WiFi credentials not set. Use connect_to_wifi(ssid, password) to get credentials. ")
            return
        
        try:
            # Command to connect to specified wifi network
            connect_command = f"nmcli device wifi connect '{self.ssid}' password '{self.password}'"
            
            # Run the command and check for errors
            process = subprocess.run(connect_command, shell=True, capture_output=True)
            
            if process.returncode == 0:
                print( f" Connected to {self.ssid} successfully.")
            
            else:
                print(f"Failed to connect to {self.ssid}. Error: {process.stderr}")
                
        except Exception as e:
            print(f"Error encountered entering network mode: {e}")
            
    def enter_access_point_mode(self): # Function to enter access point mode
        """ Puts the server in access point mode, allowing the webapp to run on Rpi's Hotspot."""
        self.ssid = "Rpi-Hot"
        self.password = "password"
        try:
            # Step 1: Confiure hostapd (AP settings)
            with open("/etc/hostapd/hostapd.conf", "w") as f:
                f.write(f"""
                interface=wlan0
                driver=nl80211
                ssid={self.ssid}
                hw_mode=g
                channel=7
                wmm_enabled=0
                macaddr_acl=0
                auth_algs=1
                ignore_broadcast_ssid=0
                wpa=2
                wpa_passphrase={self.password}
                wpa_key_mgmt=WPA-PSK
                wpa_pairwise=TKIP
                rsn_pairwise=CCMP
                """)
                
            # Step 2: Configure DHCP server (dnsmasq)
            with open("/etc/dnsmasq.conf", "w") as f:
                f.write(f"""
                interface=wlan0
                dhcp-range= 192.168.4.20, 255.255.255.0,24h
                """)
                
            # Step 3: Set up static IP for wlan0
            subprocess.run("sudo ifconfig wlan0 192.168.4.1 netmask 255.255.255.0", shell=True)
            
            # Step 4: Enable hostapd and dnsmasq services
            subprocess.run("sudo systemctl start hostapd", shell=True)
            subprocess.run("sudo systemctl start dnsmasq", shell=True)
            
            print(f"Access Point mode enabled. SSID: {self.ssid} Password: {self.password}")
            
        except Exception as e:
            print(f"Error enabling access point mode: {e}")
     
    ########## NOT SURE IF THIS FUNCTION IS NEEDED / WORKS ##########       
    def exit_access_point_mode(self): # Function to exit access point mode
        """ Exits access point mode and reverts to client mode."""
        try:
            # Step 1: Stop hostapd and dnsmasq services
            subprocess.run("sudo systemctl stop hostapd", shell=True)
            subprocess.run("sudo systemctl stop dnsmasq", shell=True)
            
            # Step 2: Restart the wlan0 interface
            subprocess.run("sudo ifconfig wlan0 down", shell=True)
            subprocess.run("sudo ifconfig wlan0 up", shell=True)
            
            print("Access Point mode disabled.")
            
        except Exception as e:
            print(f"Error disabling access point mode: {e}")
            
    def connect_to_wifi(self, ssid, password): # Function to connect to wifi
        """ Connects the server to a wifi network."""
        self.ssid = ssid
        self.password = password
        print(f" Wfi credentials set. SSID: {self.ssid}, Password: {self.password}")
    
    def disconnect_from_wifi(self): # Function to disconnect from wifi
        """ Disconnects the server from a wifi network."""
        self.ssid = None
        self.password = None
    

    
    
    

    # Node functions
    def connect_node(self,node_id): # Function to connect to a new node
        """ Connects to a new node using BLE. Uses the node_id to identify the node."""
        print("BaseStation is scanning for nodes...")
        
        try:
            # Step 1: Start listening for nearby devices
            nearby_devices = bluetooth.discover_devices(duration = 8, lookup_names = True)
            
            # Step 2: Loop through devices to identify PrivacyDotNode devices
            for addr, name in nearby_devices:
                if "PrivacyDotNode" in name: # Assuming the node name contains "PrivacyDotNode"
                    print(f"Found node: {name} with address: {addr}")
                    print("Attempting to connect...")
                    
                    # Step 3: Iniitialize a connection with the PrivacyDotNode
                    node_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    node_socket.connect((addr, 1)) # Assuming the node is using RFCOMM channel 1
                    
                    # Step 4: AUTHENTICATE NODE
                    node_socket.send("REQUEST_NODE_ID") # Request the node to send its ID
                    node_id = node_socket.recv(1024).decode("utf-8") # Receive the node ID
                    
                    
                    if self.authenticate_node(node_id): # Check if the node is valid
                        print(f"Node {node_id} connected successfully.")
                        self.connected_nodes[node_id] = node_socket
                        self.connected = True
                        node_socket.send("CONNECTED") # Notify the node that it is connected
                    else:
                        print(f"Node {node_id} rejected.")
                        node_socket.send("AUTH_FAILED") # Notify the node that it is rejected
                        node_socket.close()
                        
        except bluetooth.BluetoothError as e:
            print(f"Error connecting to node: {e}")
            self.connected = False
            
            
      ########### Experimental code ###########              
    def authenticate_node(self, node_id): # Function to authenticate a node
        """ Authenticates the node with the given node_id. Ensurs that the format is 'PDN#123456'"""
        # Regular expression to match the 'PDN#' followed by 6 digits format (e.g. 'PDN#123456')
        pattern = re.compile(r"PDN#\d{6}")
        
        # Check if the node_id matches the pattern
        return re.match(pattern, node_id) is not None
               
        
    
    
    def disconnect_node(self,node_id): # Function to disconnect from a node
        """ Disconnects from the node with the given node_id."""
        if node_id in self.connected_nodes:
            self.connected_nodes[node_id].close()
            del self.connected_nodes[node_id]
            print(f"Node {node_id} disconnected successfully.")
        else:
            print(f"No node with ID {node_id} currently connected.")

    def auto_connect(self): # Function to auto connect to a previously connected node
        """ Automatically connects to a previously connected node."""
             
    def recieve_ble_data(self): # Function to recieve data from a connected node
        """Listens for incoming data (e.g. sensor data) from a connected node."""
    
    def send_ble_data(self): # Function to send data to a connected node
        """ Sends data to a connected node (e.g. commands for the node)."""
    

    
    
    # WebApp functions
    def send_notification(self,data): # Function to send notification to the webapp
        """ Sends a notification to the webapp via an HTTP POST request, relaying data from the node for user alerts & updates."""

    def process_data_for_webapp(self, data): # Function to process data for the webapp
        """ Processes incoming data from the node, preparing it for HTTP transmission to the webapp via REST API."""
    
    def fetch_webapp_data(self): # Function to fetch data from the webapp
        """ Uses an HTTP GET request to fetch data from the webapp if needed for system status updates."""
    