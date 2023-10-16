# server to run python code on virtual machine
from waitress import serve
import main
serve(main.app, host='0.0.0.0', port=8083)
print("Waitress server running.....")
