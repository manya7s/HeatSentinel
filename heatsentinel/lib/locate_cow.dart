import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_compass/flutter_compass.dart';
import 'package:wifi_iot/wifi_iot.dart';

class LocateCowPage extends StatefulWidget {
  @override
  _LocateCowPageState createState() => _LocateCowPageState();
}

class _LocateCowPageState extends State<LocateCowPage> {
  double? _heading = 0;
  int? _signalStrength;
  Timer? _timer;

  @override
  void initState() {
    super.initState();

    // Listen for compass changes
    FlutterCompass.events!.listen((event) {
      setState(() {
        _heading = event.heading;
      });
    });

    // Poll Wi-Fi RSSI every 2s
    _timer = Timer.periodic(Duration(seconds: 2), (timer) async {
      var rssi = await WiFiForIoTPlugin.getCurrentSignalStrength();
      setState(() {
        _signalStrength = rssi;
      });
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    String strengthText =
    _signalStrength == null ? "No signal" : "${_signalStrength} dBm";

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Locate Cow",
          style: TextStyle(color: Colors.white),
        ),
        centerTitle: true,
        elevation: 4,
        backgroundColor: Colors.green[700],
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min, // shrink to content
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Compass heading
              Card(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12)),
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      Text(
                        "Compass Heading",
                        style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.green[800]),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        "${_heading?.toStringAsFixed(2)}°",
                        style: const TextStyle(
                            fontSize: 20, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Wi-Fi Signal strength
              Card(
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12)),
                elevation: 4,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      Text(
                        "Wi-Fi Signal Strength",
                        style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.green[800]),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        strengthText,
                        style: const TextStyle(
                            fontSize: 20, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 40),

              // Arrow with map background
              SizedBox(
                height: 250,
                width: 250,
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    // Static map background
                    ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Image.asset(
                        'assets/map_bg.png', // your static map image in assets
                        fit: BoxFit.cover,
                        height: 250,
                        width: 250,
                      ),
                    ),
                    // Arrow pointer
                    Transform.rotate(
                      angle: (_heading ?? 0) * (3.1415926535 / 180) * -1,
                      child: Icon(
                        Icons.arrow_upward,
                        size: 120,
                        color: _signalStrength != null && _signalStrength! > -60
                            ? Colors.green
                            : Colors.red,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Proximity status
              Text(
                _signalStrength != null && _signalStrength! > -60
                    ? "You are close!"
                    : "Move around to locate",
                style:
                const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
