How to start project

install requirements: 
pip install -r requirements.txt

All urls used in this project.
Please use Postman instead of Swagger, because urls uses params.
Postman collection link.https://www.getpostman.com/collections/b7aeab97d0fe096a7a92

Admin Links

/admin/user	showUserAdmin	none - show all users, user_id - show all users with same user_id, email - show all users with same email.	Get

/admin/user/add	addUserAdmin	none	Get

/admin/user/edit	editUserAdmin	user_id - edit user with same user_id, username - edit user with same username, email - edit user with same email.	Get

/admin/user/delete	deleteUserAdmin	none - delete all users, user_id - delete user with same user_id, username - delete user with same username, email - delete user with same email.	Get

/admin/address	showAddressAdmin	user_id - show address with same user_id, id - show address with same id, distance - show address within distance(meter), latitude - show address with same latitude, longitude - show address with same longitude, street - show address with same street, state - show address with same state, city - show address with same city, pincode - show address with same pincode, addresstype - show address with same addresstype.	Get

/admin/address/add	addAddressAdmin	none - add address to user with '0' user_id, user_id - add address to user with same user_id.	Get

/admin/address/edit	editAddressAdmin	id - edit address with same id	Get

/admin/address/delete	deleteAddressAdmin	none - delete all addresss, user_id - delete address with same user_id, id - delete address with same id. Get


User Links

/user	showUser	none - show all info of user	Get

/user/add	addUser	none	Get

/user/edit	editUser	none	Get

/user/delete	deleteUser	none	Get

/address	showAddress	none - show all address, id - show address with same id, distance - show address within distance(meter), latitude - show address with same latitude, longitude - show address with same longitude, street - show address with same street, state - show address with same state, city - show address with same city, pincode - show address with same pincode, addresstype - show address with same addresstype.	Get

/address/add	addAddress	none - add address to user login user. Get

/address/edit	editAddress	id - edit address with same id	Get

/address/delete	deleteAddress	none - delete all addresss, id - delete address with same id.	Get

Create by anshaj

Email anshaj.dhiman.7@gmail.com
