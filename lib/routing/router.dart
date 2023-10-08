import 'package:testdolby/pages/analytics/analytics.dart';
import 'package:testdolby/pages/audit_trial/audit_trial.dart';
import 'package:testdolby/pages/authentication/authentication.dart';
import 'package:testdolby/pages/dashboard/dashboard.dart';
import 'package:testdolby/pages/data_management/data_management.dart';
import 'package:testdolby/pages/tresholds/tresholds.dart';
import 'package:testdolby/pages/users/users.dart';
import 'package:testdolby/routing/routes.dart';
import 'package:flutter/material.dart';

Route<dynamic> generateRoute(RouteSettings settings) {
  switch (settings.name) {
    case DashViewPageRoute:
      return _getPageRoute(const DashboardPage());
    case UserPageRoute:
      return _getPageRoute(const UsersPage());
    case TresholdsPageRoute:
      return _getPageRoute(const TresholdsPage());
    case AnalyticsPageRoute:
      return _getPageRoute(const AnalyticsPage());
    case DataManagementPageRoute:
      return _getPageRoute(DataManagementPage());
    case AuditTrailPageRoute:
      return _getPageRoute(const AuditTrialPage());
    case AuthenticationPageRoute:
      return _getPageRoute(const AuthenticationPage());
    default:
      return _getPageRoute(const AuthenticationPage());
  }
}

PageRoute _getPageRoute(Widget child) {
  return MaterialPageRoute(builder: ((context) => child));
}
