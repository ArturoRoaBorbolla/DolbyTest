import 'dart:io';

import 'package:testdolby/helpers/encrypt.dart';
import 'package:testdolby/model/user.dart';
import 'package:sqflite/sqlite_api.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

class SqliteService {
  
  Future<Database> initDb() async {
    sqfliteFfiInit();
    Directory currentDir = Directory.current;
    print(currentDir.path);
    var database = '${currentDir.path}\\DataBase\\Dolby.db';
    var databaseFactory = databaseFactoryFfi;
    print(database);
    var db = await databaseFactory.openDatabase(database);
    databaseFactory.databaseExists(database);

    return db;      
  }    

  Future<String> createUser(User user) async{
    late String response;
    Database db = await initDb();
    user.password = EncryptData.encryptAES(user.password);
    await db.insert('USER', user.toJson()).
    then((value) {
      response = value.toString();
    });
    await db.close();
    return response;
  }

  Future updateUser(User user) async {
    late String response;
    Database db = await initDb();
    user.password = EncryptData.encryptAES(user.password);
    await db.update('USER', user.toJson(), where: "username = ?", whereArgs: [user.username]).
    then((value) {
      response = value.toString();
      print(response);
    });
    await db.close();
  }

  Future deleteUser(User user) async {
    late String response;
    Database db = await initDb();
    await db.delete('USER', where: "username = ?", whereArgs: [user.username])
    .then((value) {
      response = value.toString();
      print(response);
    });
    await db.close();
  }

  Future<User> getUser(String username) async{
    Database db = await initDb();
    List<Map<String, Object?>> result = await db.query('USER', where: 'username="$username"');
    User user = User.updadte(
                    result[0]['username'].toString(), 
                    result[0]['name'].toString(), 
                    result[0]['lastname'].toString(), 
                    result[0]['title'].toString(), 
                    int.parse(result[0]['role'].toString()));
    await db.close();
    return user;
  }

  Future<User> login(String username, String password) async{
    Database db = await initDb();
    password = EncryptData.encryptAES(password);
    List<Map<String, Object?>> result = await db.query(
      'USER',
      where: 'username="$username" and password="$password"'
    );
    User user = User.updadte(
                result[0]['username'].toString(), 
                result[0]['name'].toString(), 
                result[0]['lastname'].toString(), 
                result[0]['title'].toString(), 
                int.parse(result[0]['role'].toString()));
    await db.close();
    return user;
  }

  Future<List<String>> getAllTableNames() async {
    Database db = await initDb();
      
    List<Map> maps =
        await db.rawQuery('SELECT * FROM sqlite_master ORDER BY name;');

    List<String> tableNameList = [];
    if (maps.length > 0) {
      for (int i = 0; i < maps.length; i++) {
        try {
          tableNameList.add(maps[i]['name'].toString());
        } catch (e) {
          print('Exeption : $e');
        }
      }
    }
    tableNameList.remove('USER');
    tableNameList.remove('sqlite_autoindex_USER_1');
    return tableNameList;
  }

  Future<List<String>> getAllColumnNames(String tableName) async {
    Database db = await initDb();
      
    List<Map> maps =
        await db.rawQuery('PRAGMA table_info($tableName);');

    List<String> columnNameList = [];
    if (maps.isNotEmpty) {
      for (int i = 0; i < maps.length; i++) {
        try {
          columnNameList.add(maps[i]['name'].toString());
        } catch (e) {
          print('Exeption : $e');
        }
      }
    }
    return columnNameList;
  }

  Future<List<Map>> getRowsTable(String tableName) async {
    Database db = await initDb();
    return await db.rawQuery('SELECT * FROM $tableName LIMIT 1000;');
  }
}