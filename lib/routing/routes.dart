const DashViewPageRoute = "Dashboard";
const UserPageRoute = "Users";
const TresholdsPageRoute = "Tresholds";
const AnalyticsPageRoute = "Analytics";
const DataManagementPageRoute = "Data Management";
const AuditTrailPageRoute = "Audit Trail";
const AuthenticationPageRoute = "Authtentication";

List<dynamic> sideMenuItemsUser = [
  DashViewPageRoute,
  AnalyticsPageRoute,
  DataManagementPageRoute,
  AuditTrailPageRoute,
  AuthenticationPageRoute
];

List<dynamic> sideMenuItemsAdmin = [
  DashViewPageRoute,
  UserPageRoute,
  AnalyticsPageRoute,
  DataManagementPageRoute,
  AuditTrailPageRoute,
  AuthenticationPageRoute
];

List<dynamic> sideMenuItemsSuperadmin = [
  DashViewPageRoute,
  UserPageRoute,
  TresholdsPageRoute,
  AnalyticsPageRoute,
  DataManagementPageRoute,
  AuditTrailPageRoute,
  AuthenticationPageRoute
];
