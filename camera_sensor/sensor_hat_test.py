from sense_hat import SenseHat
sense = SenseHat()

R = [255, 0, 0]  # 赤
O = [0, 0, 0]    # 黒（消灯）

# "H" のような文字のパターン
pixels = [
    R, O, R, O, R, O, R, O,
    R, O, R, O, R, O, R, O,
    R, R, R, O, R, R, R, O,
    R, O, R, O, R, O, R, O,
    R, O, R, O, R, O, R, O,
    R, O, R, O, R, O, R, O,
    R, O, R, O, R, O, R, O,
    R, O, R, O, R, O, R, O
]

sense.set_pixels(pixels)
