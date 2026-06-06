import sys
from rplidar import RPLidar


PORT_NAME = '/dev/tty.usbserial-0001'

def run(path,j_max):
	lidar = RPLidar(PORT_NAME)
	j=0
	outfile = open(path, 'w')
	try:
		for measure in lidar.iter_measures():
			if measure[3]>0:
				if j< int(j_max):
					print(measure)
					line = '\t'.join(str(v) for v in measure)
					outfile.write(line + '\n')
					j=j+1
				else:
					break
	except KeyboardInterrupt:
		print("Interrupted by user.")
	finally:
		stop(lidar,outfile) 

def stop(l,o):
	o.close()
	l.stop_motor()
	l.stop()
	l.disconnect()
	
if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2])
