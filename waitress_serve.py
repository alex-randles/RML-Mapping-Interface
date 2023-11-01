# waitress server is used to deploy the application on virtual machine 
# 'pip3 install waitress' can be used to download the package 
import waitress
import main
print("Waitress server running.....")
waitress.serve(main.app, host='0.0.0.0', port=9000)

