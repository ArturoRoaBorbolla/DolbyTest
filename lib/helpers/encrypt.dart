import 'package:encrypt/encrypt.dart';
import 'dart:convert';


class EncryptData{
  static Encrypted? encrypted;
  static var decrypted;

/*
  static String encryptAES(plainText){
    final key = Key.fromUtf8('my 32 length key................');
    final iv = IV.fromLength(16);
    final encrypter = Encrypter(AES(key));
    encrypted = encrypter.encrypt(plainText, iv: iv);
    return encrypted!.base64;
  }

  static String decryptAES(plainText){
    final key = Key.fromUtf8('my 32 length key................');
    final iv = IV.fromLength(16);
    final encrypter = Encrypter(AES(key));
    decrypted = encrypter.decrypt(encrypted!, iv: iv);
    return decrypted;
  }
}*/



  static String encryptAES(plainText){
  List<int> mydataint = utf8.encode(plainText);
  String bs64str = base64.encode(mydataint);
  print(bs64str);
  //final key = Key.fromUtf8('my 32 length key................');
  //final iv = IV.fromLength(16);
  //final encrypter = Encrypter(AES(key));
  //encrypted = encrypter.encrypt(plainText, iv: iv);
  //var decrypted = encrypter.decrypt(encrypted!, iv: iv);
  //print(decrypted);
  //return encrypted!.base64;
  //print(bs64str);
  return bs64str;
  }

  static String decryptAES(plainText){
  List<int> decodedint = base64.decode(plainText);
  String decodedstring = utf8.decode(decodedint);
  return decodedstring;
  //final key = Key.fromUtf8('my 32 length key................');
  //final iv = IV.fromLength(16);
  //final encrypter = Encrypter(AES(key));
  //decrypted = encrypter.decrypt(encrypted!, iv: iv);
  //return decrypted;
  }
  }