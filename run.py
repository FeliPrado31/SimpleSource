import time
import os

def main():
	try:
		data = os.system("Source.py")
	except KeyboardInterrupt:
		data = 2
	print data
	if data == 1:
		print "[ERROR] Ha ocurrido un error"
		time.sleep(1)
		print "Presione uno (1) para salir"
		print "Presione uno (2) para reiniciar servidor"
		x = 0
		try:
			while( x > 2 or x < 1):
				x = input("Accion: ")
		except: x = 2
		if x == 2:
			os.system("cls")
			print("[Start] Reiniciando servidor despues de error interno")
			main()
	elif data in [2]:
		os.system("cls")
		print "="*50
		print "="*50
		print("[Start] Reinicio Forzado")
		print "="*50
		print "="*50
		main()
	elif data in [5,1280]:
		print "[CENTRALMICE ES] Servidor CAIDO!"
		raw_input("")
	elif data in [11,2816]:
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 10 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 9 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 8 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 7 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 6 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 5 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 4 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 3 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 2 segundos"
		time.sleep(1)
		print "[ERROR] Error a los puertos del Servidor. Reiniciando el Servidor en 1 segundo"
		time.sleep(1)
		os.system("cls")
		main()
	else:
		print "[ERROR] Servidor apagado! Reiniciando servidor en 1 segundos..."
		time.sleep(1)
		os.system("cls")
		main()

if __name__=="__main__":
	os.system("cls")
	main()
