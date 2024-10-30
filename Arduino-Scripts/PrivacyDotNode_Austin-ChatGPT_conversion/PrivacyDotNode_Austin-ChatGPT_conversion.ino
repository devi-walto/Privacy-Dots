#include <Arduino.h>
#include <WiFi.h>          // Include Wi-Fi library for ESP32
#include <BluetoothSerial.h> // Include Bluetooth library for ESP32

class PrivacyDotNode {
private:
    String node_id;
    bool motion_detected;
    bool connected;
    String wifi_mode;
    String ssid;
    String password;
    

    // BluetoothSerial object for Bluetooth communication
    BluetoothSerial SerialBT;

public:
    // Constructor
    PrivacyDotNode(const String& id) 
        : node_id(id), motion_detected(false), connected(false) {}

    void initialize_connection() {
        Serial.println("Initializing connection settings for Bluetooth communication...");
        SerialBT.begin(node_id);  // Start Bluetooth with node ID
        connected = true;
        Serial.println("Bluetooth initialized.");
    }

    void connect_to_base_station(const String& ip, int port) {
        if (connected) {
            Serial.println("Connecting to BaseStation at " + ip + ":" + String(port) + "...");
            // Add your socket connection logic here
            // Example: Create a WiFiClient and connect to the server
            Serial.println("Connected to BaseStation.");
        } else {
            Serial.println("Connection initialization required before connecting to BaseStation.");
        }
    }

    void detect_motion() {
        motion_detected = true;
        Serial.println("Node " + node_id + " detected motion!");
        String data = "node_id: " + node_id + ", motion: " + String(motion_detected) + ", Detection_time: " + String(millis());
        send_data(data);
    }

    void send_data(const String& data) {
        if (connected) {
            Serial.println("Sending data: " + data);
            // Implement Bluetooth or Wi-Fi data sending logic here
            // Example: SerialBT.println(data); // For Bluetooth
            // WiFiClient client; // For Wi-Fi
            // client.println(data); // Send data over Wi-Fi
        } else {
            Serial.println("Cannot send data, not connected.");
        }
    }

    void receive_command(const String& command) {
        Serial.println("Received command: " + command);
        // Implement command handling logic here
    }

    void wifi_setup(const String& mode, const String& ssid, const String& password) {
        this->wifi_mode = mode;
        this->ssid = ssid;
        this->password = password;
        Serial.println("Wi-Fi setup in " + mode + " mode with SSID '" + ssid + "'.");
        
        if (mode == "Client") {
            connect_to_wifi(ssid, password);
        } else if (mode == "Access Point") {
            setup_access_point();
        }
    }

    void setup_access_point() {
        Serial.println("Setting up Wi-Fi Access Point mode...");
        WiFi.softAP(ssid.c_str(), password.c_str());
        Serial.println("Access Point created.");
    }

    void connect_to_wifi(const String& ssid, const String& password) {
        Serial.println("Connecting to Wi-Fi network '" + ssid + "'...");
        WiFi.begin(ssid.c_str(), password.c_str());

        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
            Serial.print(".");
        }
        Serial.println("Connected to Wi-Fi!");
    }

    void self_check() {
        Serial.println("Running self-check diagnostics...");
        String ble_status = "Operational"; // Example status
        String wifi_status = (wifi_mode.length() > 0) ? "Operational" : "Not Configured";
        Serial.println("BLE Status: " + ble_status + ", Wi-Fi Status: " + wifi_status);
    }
};

void setup() {
    Serial.begin(9600);
    PrivacyDotNode node("Node1");

    node.initialize_connection();
    node.wifi_setup("Client", "MySSID", "MyPassword");
    node.self_check();
}

void loop() {
    // Simulate motion detection
    static unsigned long last_check = 0;
    if (millis() - last_check > 5000) {  // Check every 5 seconds
        last_check = millis();
        PrivacyDotNode node("Node1");  // Recreate node to simulate ongoing operation
        node.detect_motion();
    }
}
