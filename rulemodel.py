import numpy as np
import tensorflow as tf


class SmartEncode(tf.keras.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def eval(self, x):
        is_filter = 5
        is_multi_video = 6
        src_bitrate = 7
        wifi = 10
        publish_wifi_speed_avg = 1
        publish_mobile_speed_avg = 2
        upload_probe_speed = 0
        publish_success_rate = 3
        is_hd_video = 8
        cpu_score = 4
        if (
            x[is_filter] == 1
            or x[is_multi_video] == 1
            or x[src_bitrate] > 10 * (10**3)
        ):
            return 0
        else:
            persona_speed = (
                x[publish_wifi_speed_avg]
                if x[wifi] == 1
                else x[publish_mobile_speed_avg]
            )
            if persona_speed > 0:
                upload_speed = x[upload_probe_speed] * 0.7 + persona_speed
            else:
                upload_speed = upload_probe_speed

            if (upload_speed < 150 or x[publish_success_rate] < 0.6) and x[
                is_hd_video
            ] != 1:
                if x[cpu_score] > 8:
                    return 1
                else:
                    return 0
            else:
                return 2

    def call(self, x):
        """
        0:upload_probe_speed
        1:publish_wifi_speed_avg
        2 :publish_mobile_speed_avg
        3 :publish_success_rate
        4: cpu_score
        5: is_filter
        6 :is_multi_video
        7 :src_bitrate
        8 :is_hd_video
        9: "mobile"
        10 :"wifi"
        11: "2G"
        12 :"3G"
        13 :"4G"
        14: "unknown"
        """
        is_filter = 5
        is_multi_video = 6
        src_bitrate = 7
        wifi = 10
        publish_wifi_speed_avg = 1
        publish_mobile_speed_avg = 2
        upload_probe_speed = 0
        publish_success_rate = 3
        is_hd_video = 8
        cpu_score = 4

        real_success_rate = tf.where(
            tf.math.greater(0.0, x[0, publish_success_rate]),
            0.0,
            x[0, publish_success_rate],
        )

        real_probe_speed = tf.where(
            tf.math.greater(0.0, x[0, upload_probe_speed]),
            0.0,
            x[0, upload_probe_speed],
        )

        real_wifi_speed = tf.where(
            tf.math.greater(0.0, x[0, publish_wifi_speed_avg]),
            0.0,
            x[0, publish_wifi_speed_avg],
        )

        real_mobile_speed = tf.where(
            tf.math.greater(0.0, x[0, publish_mobile_speed_avg]),
            0.0,
            x[0, publish_mobile_speed_avg],
        )

        encode_type = tf.ones((1,), dtype=tf.float32) * 3
        hard = tf.zeros((1,), dtype=tf.float32)
        soft = tf.ones((1,), dtype=tf.float32)
        skip = tf.ones((1,), dtype=tf.float32) * 2

        cond = tf.logical_or(
            tf.logical_or(x[0, is_filter] == 1, x[0, is_multi_video] == 1),
            x[0, src_bitrate] > 10 * (10**3),
        )  #
        encode_type = tf.where(cond, hard, encode_type)
        encode_type = tf.where(encode_type == 3.0, skip, encode_type)

        persona_speed = tf.where(x[0, wifi] == 1, real_wifi_speed, real_mobile_speed)
        upload_speed = tf.where(
            persona_speed > 0,
            persona_speed * 0.3 + real_probe_speed * 0.7,
            real_probe_speed,
        )
        upload_speed_cond = upload_speed < 150
        upload_speed_cond = tf.logical_or(
            upload_speed_cond, x[0, publish_success_rate] < 0.6
        )  # True = 弱网
        cpu = tf.where(x[0, cpu_score] > 8, soft, hard)
        cond = tf.logical_and(upload_speed_cond, x[0, is_hd_video] != 1)
        encode_type = tf.where(cond, cpu, encode_type)

        return encode_type


if __name__ == "__main__":
    se = SmartEncode()
    x = [300, 320, 310, 0.7, 9.0, 0, 0, 5 * (10**3), 1, 0, 1, 0, 0, 0, 0]
    print(se.eval(x))
    print(se(tf.convert_to_tensor(x, tf.float32)[tf.newaxis, ...]))j01
