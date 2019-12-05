# Python-ATM



1. Project Overview	
ATM Software is an academic project developed in Python scripting language which resembles the existing ATM (Automatic Teller Machine) software. 

2. ATM Software
The major modules of the ATM project are: admin module and user module. Admin refers to the bank that has installed the proposed ATM software project and the users are the customers of bank with authenticated cards.
The admin module has following sub menus:
1.	Add New ATM Card: This menu is responsible for creating new ATM user account.The details to be filled in this form are account number, pin, account name, data of issue, expiry date, address, balance and two factor verification methods which are phone number and card status. (Note, since one account may have multiple cards bound to it, you may consider implementing ATM card and Account as two separate classes. The same in database schemes design.)

2.	View ATM Machine Status: This module helps to view the details of ATM machine. Using this module, admin can view ATM address, ATM Machine status, last refill date, next refill date, min balance enquiry and current balance options.


3.  Update ATM Card: This module is responsible for re-validating the expired card. In order to update the card, admin should enter ATM card number. This module has further six sub modules as listed below:
a)	Block ATM card: Sometimes the banks need to block some cards for various reasons such as when an ATM card is lost or stolen. With this feature, any claimed ATM card can be blocked by entering card number and submit.
b)	Activate ATM card: After the approval of card from the bank officials, it is activated using this sub-module of project on bank ATM software.
c)	Reset PIN: Sometimes the card user forgets the PIN and comes to bank office to recover it or the PIN needs to be changed. This menu facilitates to reset the PIN.
d)	Reset phone: This sub-module is useful in updating the phone number of customers.
e)	View history: With the help of this menu, the admin can view the history of transaction of money.
f)	Update expiring date: If the existing expiry date is to be modified, this sub-module is used by admin.
As for the user module, please see the user stories. Three (3)  required stories, three (3) optional stories.

3. Project Report
Write a project report that explains:
* Project management, develop a project schedule and plan, and monitor progress. 
* Version control, develop a version control strategy. 
* Define system requirements 
*	Create design models using UML. 
*	Implement the system. 
*	Develop test cases for system test, and document the test results. 
*	Present the project. 
