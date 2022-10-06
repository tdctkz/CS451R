# CS451R's project

#Project Summary
You will be creating a web application that allows users to login and setup their own
fundraiser, track their donations, and view and donate to other user’s fundraisers. While
you must be able to track and make donations through your site, you are not processing
real transactions. Please use fake/dummy card numbers when appropriate to simulate the
process.

#Requirements
##Technical Requirements
• Must be a web application (not a desktop application) built in a “modern” web
development framework.
o .Net (C#) or Java preferably – if you choose another framework, support from
us will be limited
o You cannot use a CMS, such as WordPress
• Database should be in SQL server 2012 or above – if you choose another database
option, support from us will be limited.
• 10% code coverage for unit tests is required.
o xUnit is a good framework for .NET.
User Experience Requirements
• The application needs to be designed so that anyone, regardless of technical level,
should be able to understand and use your website.
o Text should be clearly visible across desktop and mobile views
▪ This includes font sizes, proper background colors for fonts, font
colors, contrast etc.
o Use everyday language that users will be able to understand
▪ Ex. Spelling out the date and time in a readable format instead of a
timestamp
o Text in tables need to be properly aligned for readability.
▪ Numeric needs to be right aligned.
▪ Alphanumeric needs to be left aligned.
o Pay attention to use of negative (or “white”) space in your design as well
Frontend Development Requirements
• Make the application mobile and web responsive and aesthetically pleasing.
2
• You must use at least one CSS framework
o We recommend Bootstrap.
• Front-end framework/libraries are up to you but must be included in project (aka no external resources).
Required Pages
Login Page
• A login and password field
o Mask the password field.
o Password requirements:
▪ 8 characters minimum
▪ 1 upper case letter
▪ 1 symbol
▪ 1 number
o Login Button
Homepage/Dashboard
• From this screen all fundraisers created by other users are displayed
o Fundraisers can be clicked on and viewed with the ability to donate
• User can create new fundraiser
Individual Fundraiser Pages
• Fundraiser pages must include:
o Fundraiser Title
o Fundraiser Description
o Fundraiser goal and how much has been raised so far
▪ Use a graphic of some sort to display the progress
• A list of most recent donation amounts and the donor’s name
• A donate button that leads to a donation form
Donation Form
• Form must include:
o Name and billing address
o Donation amount
o The option to donate from a bank account or a credit/debit card
User Profile and Settings
3
• User can view and edit their active fundraisers
• User can update personal information and password
