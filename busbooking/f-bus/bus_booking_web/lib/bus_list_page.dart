import 'package:flutter/material.dart';

// Define the Bus class
class Bus {
  final String number;
  final String route;

  Bus({required this.number, required this.route});
}

// Simulate API call to fetch buses
Future<List<Bus>> fetchBuses() async {
  await Future.delayed(Duration(seconds: 2));

  // Simulated bus data
  return [
    Bus(number: '123', route: 'Downtown to Uptown'),
    Bus(number: '456', route: 'Midtown to City Center'),
    Bus(number: '789', route: 'Airport to Station'),
  ];
}

class BusListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Available Buses')),
      body: FutureBuilder<List<Bus>>(
        future: fetchBuses(), // Call API to get buses
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final buses = snapshot.data;

          if (buses == null || buses.isEmpty) {
            return Center(child: Text('No buses available at the moment.'));
          }

          return ListView.builder(
            itemCount: buses.length,
            itemBuilder: (context, index) {
              final bus = buses[index];
              return ListTile(
                title: Text('Bus Number: ${bus.number}'),
                subtitle: Text(bus.route),
                onTap: () {
                  Navigator.pushNamed(context, '/booking');
                },
              );
            },
          );
        },
      ),
    );
  }
}
