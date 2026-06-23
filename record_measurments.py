import sys
from rplidar import RPLidar
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import time

PORT_NAME = '/dev/tty.usbserial-0001'

def run(j_max):
	epoch_time=str(int(round(time.time()*1000)))
	path=epoch_time+".txt"
	path_fig=epoch_time+".png"
	#df= pd.DataFrame(columns=["angle","distance"])
	data=[]
	lidar = RPLidar(PORT_NAME)
	j=0
	outfile = open(path, 'w')
	try:
		for measure in lidar.iter_measures():
			if measure[3]>0:
				if j< int(j_max):
					#print(measure)
					data=data+[{"angle":measure[2]*2*math.pi/360,"distance":measure[3]}]
					line = '\t'.join(str(v) for v in measure)
					outfile.write(line + '\n')
					j=j+1
				else:
					break
	except KeyboardInterrupt:
		print("Interrupted by user.")
	finally:
		stop(lidar,outfile)
		df=pd.DataFrame(data)

		fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10,10))


		label_loc = np.linspace(start=0, stop=2 * np.pi, num=360)

		bars = ax.bar(x = df["angle"], height=df["distance"], width=np.pi/800, 
		       edgecolor='black', zorder=2, alpha=0.8)

		plt.savefig(path_fig)
		outfile.close()



def stop(l,o):
	o.close()
	l.stop_motor()
	l.stop()
	l.disconnect()
	
if __name__ == '__main__':
	time.sleep(int(sys.argv[2]))
	while True:
		time.sleep(int(sys.argv[3]))
		run(sys.argv[1])
