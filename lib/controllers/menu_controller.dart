import 'package:testdolby/constants/styles.dart';
import 'package:testdolby/routing/routes.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class MenuController extends GetxController {
  static MenuController instance = Get.find();
  var activeItem = DashViewPageRoute.obs;
  var hoverItem = "".obs;

  changeActiveItemTo(String itemName) {
    activeItem.value = itemName;
  }

  onHover(String itemName) {
    if (!isActive(itemName)) hoverItem.value = itemName;
  }

  isActive(String itemName) => activeItem.value == itemName;

  isHovering(String itemName) => hoverItem.value == itemName;

  Widget returnIconFor(String itemName) {
    switch (itemName) {
      case DashViewPageRoute:
        return _customIcon(Icons.punch_clock, itemName);
      case UserPageRoute:
        return _customIcon(Icons.account_circle, itemName);
      case TresholdsPageRoute:
        return _customIcon(Icons.punch_clock, itemName);
      case AnalyticsPageRoute:
        return _customIcon(Icons.access_alarm, itemName);
      case DataManagementPageRoute:
        return _customIcon(Icons.access_time_filled_rounded, itemName);
      case AuditTrailPageRoute:
        return _customIcon(Icons.youtube_searched_for, itemName);
      case AuthenticationPageRoute:
        return _customIcon(Icons.exit_to_app, itemName);
      default:
        return _customIcon(Icons.logout, itemName);
    }
  }

  Widget _customIcon(IconData icon, String itemName) {
    if (isActive(itemName)) return Icon(icon, size: 22, color: light);

    return Icon(icon, color: isHovering(itemName) ? Colors.black : lightGrey);
  }
}
