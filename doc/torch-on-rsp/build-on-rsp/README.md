Запустить скрипт подготовки(для установки необходимых библиотек)
<code>chmod +x prepare.sh && chmod +x builder.sh <br> 
./prepare.sh</code><br>
Затем начать сборку(автоматически скачаются исходники PyTorch)<br>
<code>./builder.sh</code><br>
После сборки в папке dist будет собранный whl образ
<h4>Для установки:</h4>
<code>sudo -H pip3 install torch......whl</code><br>
<h4>Для проверки:</h4>
<code>
import torch
print(torch.__verion__)
<code>
