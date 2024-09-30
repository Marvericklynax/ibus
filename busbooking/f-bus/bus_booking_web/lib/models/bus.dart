class Bus {
  final String number;
  final String route;

  Bus({required this.number, required this.route});

  factory Bus.fromJson(Map<String, dynamic> json) {
    return Bus(
      number: json['number'],
      route: json['route'],
    );
  }
}
