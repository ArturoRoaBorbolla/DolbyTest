import 'package:testdolby/controllers/menu_controller.dart' as menu;
import 'package:testdolby/controllers/navigation_controller.dart';
import 'package:testdolby/pages/authentication/authentication.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:localstorage/localstorage.dart' as ls;

void main() {
  Get.put(menu.MenuController());
  Get.put(NavigationController());
  runApp(MyApp());
  final ls.LocalStorage storage = ls.LocalStorage('login');
  storage.setItem('is_loading', false);
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Bot Dashboard - Aiver',
      theme: ThemeData(
          scaffoldBackgroundColor: Colors.white,
          textTheme: GoogleFonts.mulishTextTheme(Theme.of(context).textTheme)
              .apply(bodyColor: Colors.black),
          pageTransitionsTheme: const PageTransitionsTheme(builders: {
            TargetPlatform.iOS: FadeUpwardsPageTransitionsBuilder(),
            TargetPlatform.android: FadeUpwardsPageTransitionsBuilder()
          }),
          primaryColor: Colors.blue),
      home: const AuthenticationPage(),
    );
  }
}
