PyCon Financial Aid Tools
=========================

Tools to generate financial aid award letters for PyCon.


Notes
-----

Much of the data that's processed with these tools is considered
confidential. To ensure that no confidential data is published, all
data files should have a .private suffix.


Usage
-----

The awards.private file in these examples should look like:

  first name,last name,email address,registration award,hotel award,travel award
  Fred,Flintstone,fred@slaterockandgravel.com,100,489,500


To test generate grant letters:

  $ ./generate_award_messages.py awards.private -f letters.private/                       


To send test grant letters to a test email account

  $ ./generate_award_messages.py award.private -g GMAIL_USERNAME -p GMAIL_PASSWORD -t EMAIL_ADDRESS


To send out grant letters:

  $ ./generate_award_messages.py award.private -g GMAIL_USERNAME -p GMAIL_PASSWORD


