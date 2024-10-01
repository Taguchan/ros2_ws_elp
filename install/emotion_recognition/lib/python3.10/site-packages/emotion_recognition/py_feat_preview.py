import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from feat import Detector

class EmotionRecognitionNode(Node):
    def __init__(self):
        super().__init__('emotion_recognition_node')
        self.subscription = self.create_subscription(
            Image, 'camera/image_raw', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(Image, 'camera/image_with_feat', 10)
        self.br = CvBridge()
        
        # Py-FeatのDetectorを初期化
        self.emotion_detector = Detector(
            face_model="retinaface",      # 顔検出モデル
            landmark_model="mobilenet",   # 顔ランドマークモデル
            au_model="svm",               # Action Unitモデル
            emotion_model="resmasknet"    # 感情認識モデル
        )

    def listener_callback(self, data):
        frame = self.br.imgmsg_to_cv2(data, 'bgr8')
        
        # 表情認識処理
        result = self.emotion_detector.detect_image(frame)

        # 結果が取得できた場合、顔と感情を描画
        if not result.empty:
            for _, row in result.iterrows():
                # 顔の位置
                x1, y1, x2, y2 = int(row["facebox_x1"]), int(row["facebox_y1"]), int(row["facebox_x2"]), int(row["facebox_y2"])
                
                # 検出された顔に矩形を描画
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # 感情とスコアを取得
                emotion = row["emotion"]
                emotion_score = row["confidence"]

                # 表情とスコアを表示
                cv2.putText(frame, f'{emotion}: {emotion_score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

                # 表情とスコアをターミナルに出力
                self.get_logger().info(f'Emotion: {emotion}, Score: {emotion_score:.2f}')

        # パブリッシュ用のメッセージに変換
        msg = self.br.cv2_to_imgmsg(frame, 'bgr8')
        msg.header.frame_id = "camera_frame"  # フレームIDを設定
        self.publisher_.publish(msg)

        # # フレームを表示
        # cv2.imshow("Emotion Recognition", frame)
        # if cv2.waitKey(1) == ord('q'):
        #     rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    emotion_recognition_node = EmotionRecognitionNode()
    rclpy.spin(emotion_recognition_node)
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
