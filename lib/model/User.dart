class User{
  late String username; 
  late String name; 
  late String lastname; 
  late String title; 
  late int role; 
  late String password; 

  User(this.username, this.name, this.lastname, this.title, this.role,this.password);
  User.updadte(this.username, this.name, this.lastname, this.title, this.role);
  User.delete(this.username);

  Map<String, dynamic> toJson() {
    var map = <String, dynamic>{
      'username': username,
      'name': name,
      'lastname': lastname,
      'title': title,
      'role': role,
      'password': password
    };
    return map;
  }

  User.fromMap(Map<String, dynamic> map) {
    username = map['username'];
    name = map['name'];
    lastname = map['lastname'];
    title = map['title'];
    role = map['role'];
    password = map['password'];
  }
}