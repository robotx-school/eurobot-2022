![alt text](https://raw.githubusercontent.com/robotx-school/eurobot-2022/develop/torchSegmentation/coords_detect/resulted_mask.png?token=ANGEBHJYOZWRGLHQWVYKKGTB2XNUO)
![alt text](https://raw.githubusercontent.com/robotx-school/eurobot-2022/develop/torchSegmentation/coords_detect/field_with_robots.png?token=ANGEBHJU44MMAJJEYMM6OTTB2XNYU)

new_net.py - Попытка проверки столкновения роботов с использованием масок.
Вокруг робота стороится прямоугольник. На двух нижних вершинах(те которые фактически являются основанием) ставятся точки. Далее каждая точка проверяется с точкой на других роботах. Проверяется = определяется расстояние между ними и сравнивается с константой(минимальным расстоянием, чтобы не было столкновения). 
![alt](demo.png)

Координты углов для более больших картинок [284, 432], [731, 431]
