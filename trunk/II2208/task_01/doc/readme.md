<p style="text-align: center; line-height: 24px;">
МИНИСТЕРСТВО ОБРАЗОВАНИЯ РЕСПУБЛИКИ БЕЛАРУСЬ
<br>
УЧРЕЖДЕНИЕ ОБРАЗОВАНИЯ
<br>
“БРЕСТСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ”
<br>
ИНТЕЛЕКТУАЛЬНЫЕ ИНФОРМАЦИОННЫЕ ТЕХНОЛОГИИ
<br>
ОТЧЁТ
<br>
По лабораторной работе № 1
</p>
<div style="width: 100%; display: flex; justify-content: right;">
<p style="width: 200px; line-height: 20px;">
Выполнил:
<br>
Cтудент группы ИИ-22
<br>
Копанчук Е. Р.
<br>
Проверила:
<br>
Ситковец Я.С
</p>
</div>
<p style="text-align: center; line-height: 30px;">
Брест – 2024
</p>

<h5>Задание:</h5>
<p style="line-height: 20px;">
Составить программу, выполняющую фильтрацию изображения от импульсных помех.
<span style="font-weight: bold;">Необходимые характеристики:</span>
<div style="line-height: 20px;">
<li>Изображение хранится во внешнем файле;</li>
<li>программно в изображение вносятся помехи;</li>
<li>программа должна выводить исходное и отфильтрованное изображения;</li>
<li>Должна присутствовать возможность выбора уровня зашумления.</li>
<li>Использовать медианный фильтр. Окно должно осуществлять проход изображения по строкам и столбцам.</li>
</div>

<h5>Результат работы:</h5>

<div style="width: 100%; text-align: center;">
<img src="./program.png" style="width: 50%;"/>
</div>
<div style="line-height: 10px; width: 100%; text-align: center; font-size: 12px; padding-bottom: 20px;">ГУИ программы</div>

<img src="./examples.png"/>
<div style="line-height: 10px; width: 100%; text-align: center; font-size: 12px; padding-bottom: 20px;">1. Исходные изображение; 2. Зашумленные изображения; 3. Востановленные изображения.</div>

<h5>Код программы:</h5>
<a href="https://github.com/brstu/GIIS-2024/tree/main/trunk/II2208/task_01/src/main.py">Перейти к коду</a>