import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class EngeldenKacan(Node):
    def __init__(self):
        super().__init__('engelden_kacan_node')
        # Tekerleklere hız komutu göndereceğimiz kanal (cmd_vel)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        # Lidar (Mesafe) sensöründen veri okuyacağımız kanal (scan)
        self.subscription = self.create_subscription(LaserScan, 'scan', self.sensor_callback, 10)
        self.get_logger().info('Engelden kacan robot sistemi baslatildi. Lidar sensoru dinleniyor...')

    def sensor_callback(self, msg):
        cmd = Twist()
        # Lidar'ın tam önümüzdeki (0 derecedeki) mesafe verisini alıyoruz
        on_mesafe = msg.ranges[0]
        
        # Engel 0.5 metreden (50 cm) yakınsa (Tıpkı HC-SR04 mantığı gibi)
        if on_mesafe < 0.5:
            cmd.linear.x = 0.0   # İleri gitmeyi durdur
            cmd.angular.z = 0.5  # Sağa dön
            self.get_logger().info('Engel algilandi! Yon degistiriliyor...')
        else:
            cmd.linear.x = 0.2   # Önümüz boş, 0.2 hızla düz gitmeye devam et
            cmd.angular.z = 0.0
            
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = EngeldenKacan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
