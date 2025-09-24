import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'firebase_options.dart';
import 'locate_cow.dart';
import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';


// Background message handler
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  print('Background message received: ${message.notification?.title}');
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

  String? fcmToken = await FirebaseMessaging.instance.getToken();
  print("FCM Device Token: $fcmToken");

  runApp(HeatSentinelApp());
}

class HeatSentinelApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Heat Sentinel',
      theme: ThemeData(
        primarySwatch: Colors.green,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomePage(),
      routes: {
        '/locate_cow': (_) => LocateCowPage(),
      },
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _notificationMessage = "No notifications yet.";
  String city = "Loading location..."; // updated with device location

  // Example weather/advisory data
  final int temperature = 29;
  final int humidity = 58;
  final double wind = 8.48;
  final String weather = "Clouds";
  final String advisory = "Favourable body temperature for cows is 37";

  @override
  void initState() {
    super.initState();
    _getDeviceLocation();

    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      String title = message.notification?.title ?? "Alert";
      String body = message.notification?.body ?? "";

      setState(() {
        _notificationMessage = "$title\n$body";
      });

      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: Text(title),
          content: Text(body),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Dismiss'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                Navigator.pushNamed(context, '/locate_cow');
              },
              child: const Text('Locate Cow'),
            ),
          ],
        ),
      );
    });
  }

  Future<void> _getDeviceLocation() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      setState(() {
        city = "Location disabled";
      });
      return;
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        setState(() {
          city = "Permission denied";
        });
        return;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      setState(() {
        city = "Permission permanently denied";
      });
      return;
    }

    Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high);

    // Reverse geocoding
    try {
      List<Placemark> placemarks =
      await placemarkFromCoordinates(position.latitude, position.longitude);
      Placemark place = placemarks.first;
      setState(() {
        city = "${place.locality ?? place.subAdministrativeArea ?? 'Unknown'}, ${place.country ?? ''}";
      });
    } catch (e) {
      setState(() {
        city = "Unknown location";
      });
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text(
          'HeatSentinel',
          style: TextStyle(color: Colors.white),
        ),
        centerTitle: true,
        backgroundColor: Colors.green[700],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Notification banner
            if (_notificationMessage != "No notifications yet.")
              Card(
                color: Colors.red[100],
                child: ListTile(
                  leading: Icon(Icons.notification_important, color: Colors.red),
                  title: Text(_notificationMessage),
                  trailing: TextButton(
                    onPressed: () {
                      Navigator.pushNamed(context, '/locate_cow');
                    },
                    child: const Text("Locate Cow"),
                  ),
                ),
              ),
            const SizedBox(height: 16),

            // Options grid (3 buttons)
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              childAspectRatio: 1.1,
              children: [
                _buildOptionCard(Icons.videocam, "View Surveillance Feed", () {}),
                _buildOptionCard(Icons.pets, "Track Cows", () {
                  Navigator.pushNamed(context, '/locate_cow');
                }),
                _buildOptionCard(Icons.history, "View Incident Record", () {}),
              ],
            ),
            const SizedBox(height: 20),

            // Weather & Advisory card
            _buildWeatherAdvisoryCard(),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionCard(IconData icon, String label, VoidCallback onTap) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      elevation: 3,
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: onTap,
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 50, color: Colors.green[700]),
              const SizedBox(height: 8),
              Text(
                label,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildWeatherAdvisoryCard() {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: const [
                Icon(Icons.wb_sunny, color: Colors.orange, size: 22),
                SizedBox(width: 6),
                Text(
                  "Weather & Advisory",
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(city, style: const TextStyle(fontSize: 16)),
                Text(weather, style: TextStyle(color: Colors.grey[600])),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Text(
                  "$temperature°C",
                  style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                ),
                const SizedBox(width: 12),
                const Text(
                  "Feels like: 30°C",
                  style: TextStyle(color: Colors.grey),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Row(
              children: [
                Text("Humidity: $humidity%", style: const TextStyle(fontSize: 15)),
                const SizedBox(width: 18),
                Text("Wind: $wind m/s", style: const TextStyle(fontSize: 15)),
              ],
            ),
            const SizedBox(height: 12),
            Container(
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.orange[50],
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: Colors.orange[200]!),
              ),
              padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 6),
              child: Text(
                "Advisory: $advisory",
                style: TextStyle(color: Colors.orange[800], fontSize: 14),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
