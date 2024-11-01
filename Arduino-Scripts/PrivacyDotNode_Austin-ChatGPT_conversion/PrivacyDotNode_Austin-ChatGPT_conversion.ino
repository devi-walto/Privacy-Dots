#include <Arduino.h>
#include <WiFi.h>
#include <BLEDevice.h>
#include <nlohmann/json.hpp>  // Include the nlohmann JSON library

using json = nlohmann::json;

class PrivacyDotNode {
private:
    String node_id;
    bool motion_detected;
    bool connected;
    String wifi_mode;
    String ssid;
    String password;

    WiFiClient wifi_client;
    BLEServer *pServer = NULL;
    BLECharacteristic *pCharacteristic = NULL;

public:
    // Constructor
    PrivacyDotNode(const String& id) 
        : node_id(id), motion_detected(false), connected(false) {}

    void initialize_connection() {
        Serial.println("Initializing connection settings for Bluetooth communication...");
        BLEDevice::init(node_id.c_str());
        pServer = BLEDevice::createServer();
        pCharacteristic = pServer->createCharacteristic(
          BLEUUID((uint16_t)0x2A19), 
            BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE
        );

        pCharacteristic->setValue("Initialized");
        pServer->start();
        connected = true;
        Serial.println("BLE initialized.");
    }

    void connect_to_base_station(const String& ip, int port) {
        if (connected) {
            Serial.println("Connecting to BaseStation at " + ip + ":" + String(port) + "...");
            if (wifi_client.connect(ip.c_str(), port)) {
                Serial.println("Connected to BaseStation over Wi-Fi.");
            } else {
                Serial.println("Failed to connect to BaseStation.");
            }
        } else {
            Serial.println("Connection initialization required before connecting to BaseStation.");
        }
    }

    void detect_motion() {
        motion_detected = true;
        Serial.println("Node " + node_id + " detected motion!");
        send_data();
    }

    void send_data() {
        if (connected) {
            // Create a JSON object
            json data = {
                {"node_id", node_id.c_str()},
                {"motion_detected", motion_detected},
                {"Detection_time", millis()}
            };

            String json_data = String(data.dump().c_str());  // Convert JSON to string
            Serial.println("Sending data: " + json_data);
            
            if (wifi_mode == "Client" && wifi_client.connected()) {
                wifi_client.println(json_data);  // Send data over Wi-Fi
            } else if (pServer->getConnectedCount() > 0) {
                pCharacteristic->setValue(json_data.c_str());  // Update BLE characteristic
                pCharacteristic->notify();  // Send data over BLE
            } else {
                Serial.println("No active connection for data transmission.");
            }
        } else {
            Serial.println("Cannot send data, not connected.");
        }
    }

    void receive_command(const String& command) {
        Serial.println("Received command: " + command);
        // Parse the JSON command
        auto json_command = json::parse(command.c_str());

        std::string method = json_command["method"];
        // Here you can implement specific command handling based on the method received
        if (method == "trigger_motion_detection") {
            detect_motion();  // Call detect_motion if the method matches
        }
        // Handle other commands as needed
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
        Serial.println("Access Point created with SSID: " + ssid);
    }

    void connect_to_wifi(const String& ssid, const String& password) {
        Serial.println("Connecting to Wi-Fi network '" + ssid + "'...");
        WiFi.begin(ssid.c_str(), password.c_str());

        while (WiFi.status() != WL_CONNECTED) {
            delay(500);
            Serial.print(".");
        }
        Serial.println("\nConnected to Wi-Fi!");
    }

    void self_check() {
        Serial.println("Running self-check diagnostics...");
        String ble_status = "Operational";  // Example status
        String wifi_status = (WiFi.status() == WL_CONNECTED) ? "Connected" : "Not Connected";
        Serial.println("BLE Status: " + ble_status + ", Wi-Fi Status: " + wifi_status);
    }
};

// Declare the node globally to retain state
PrivacyDotNode node("Node1");

void setup() {
    Serial.begin(9600);
    node.initialize_connection();
    node.wifi_setup("Client", "MySSID", "MyPassword");
    node.self_check();
}

void loop() {
    static unsigned long last_check = 0;
    if (millis() - last_check > 5000) {  // Check every 5 seconds
        last_check = millis();
        node.detect_motion();
    }

    // Here you would implement code to listen for incoming commands and pass them to receive_command
}
