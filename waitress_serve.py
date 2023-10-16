# server to run python code on virtual machine
import waitress
import main
waitress.serve(main.app, host='0.0.0.0', port=8083)
print("Waitress server running.....")
