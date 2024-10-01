import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Bus Booking System')),
      body: Column(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              decoration: InputDecoration(labelText: 'Enter Source'),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              decoration: InputDecoration(labelText: 'Enter Destination'),
            ),
          ),
          ElevatedButton(
            child: Text('Search Buses'),
            onPressed: () {
              // Navigate to the bus list page
              Navigator.pushNamed(context, '/busList');
            },
          ),
        ],
      ),
    );
  }
}
