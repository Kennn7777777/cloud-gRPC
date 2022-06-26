Steps to setup (VSCode)
1.Extract contents of CloudLab .zip file
2.Enter the terminal from the root directory of the extracted folder(CloudLab)
3.From VSCode terminal(CMD), navigate to “../CloudLab/venv/Scripts” and run activate.bat to enable the virtual environment 
4.Navigate to the project directory(“../CloudLab/project”) and run “python server.py”. A message should be displayed “starting gRPC server…”
5.Open multiple new terminal in “command prompt” in the “/CloudLab/project” directory  and run “python client.py” when required for testing

Note: backup.zip file contains json file backups in case of anything
Please refer to the pdf report under "Test Plans" for instructions to test code. 