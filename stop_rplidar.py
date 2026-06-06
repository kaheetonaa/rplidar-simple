from rplidar import RPLidar

lidar=RPLidar('/dev/tty.usbserial-0001')
lidar.stop()
lidar.stop_motor()
lidar.disconnect()
