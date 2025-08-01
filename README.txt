INSTRUCTIONS
____________
(The following instructions are for initial setup, if you've already done this, go to Step 7.)
(If your computer lets you use the app found in ImageConverter > dist > "ImageConverter", disregard all steps)

1. Go to Microsoft Store
2. In the search bar, type "Python 3.11", then choose the option below the search option (should have the symbol of a blue and yellow snake).
3. Press the "Get" button, and wait for it to download.

4. Once it is download, open your Windows search bar and type "Windows PowerShell". 
____________
4a. It may not be necessary, but you can right-click on it and press "Run as Administrator" to avoid any issues with permissions.
____________

5. In PowerShell type the following: pip install pillow
6. In PowerShell type the following: pip install pillow_heif

7. (This is officially past the initial setup. Always open Windows PowerShell to start process back up) Type the following: cd "[the directory where this application is]"
____________
8a. For instance, if your application is in the Downloads folder, you'd type: cd "C:\Users\[YourUsername]\Downloads" (or if you've downloaded it with the folder still intact, you'd add "\ImageConverter" to the end).
8b. You can find the directory of your application by right-clicking it, pressing "Copy as path", and then pasting it (make sure to delete the converter_gui.py portion off of the end of it.
8c. For instance, doing so would net you "C:\Users\[YourUsername]\Downloads\ImageConverter\converter_gui.py". You would then turn this into "C:\Users\[YourUsername]\Downloads\ImageConverter".
____________

9. Finally, you will type: python converter_gui.py, which will open the application for you to use it.
