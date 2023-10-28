# server to run python code on virtual machine
import waitress
import main
print("Waitress server running.....")
waitress.serve(main.app, host='0.0.0.0', port=9000)

