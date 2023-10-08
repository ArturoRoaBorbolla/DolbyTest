import 'package:testdolby/constants/controllers.dart';
import 'package:testdolby/routing/router.dart';
import 'package:testdolby/routing/routes.dart';
import 'package:flutter/material.dart';

Navigator localNavigator() => Navigator(
      key: navigationController.navigationKey,
      initialRoute: DashViewPageRoute,
      onGenerateRoute: generateRoute,
    );
