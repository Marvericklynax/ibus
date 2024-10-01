import 'package:flutter/material.dart';
import 'home_page.dart';
import 'bus_list_page.dart';
import 'booking_page.dart';

void main() {
  runApp(BusBookingApp());
}

class BusBookingApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bus Booking System',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
      routes: {
        '/busList': (context) => BusListPage(),
        '/booking': (context) => BookingPage(),
      },
    );
  }
}
