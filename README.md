Для тестирования использовался укороченный yml файл, в котором 5000 объектов, ввиду технических ограничений и желания ускорить процесс, ОДНАКО итерационная загрузка и обработка данных реализована даже в нем (в коде указан batch_size 1000), так что запуск большого файла исключительно вопрос времени. </br> </br>
Для запуска контейнеров postgres и elastic search:
```
docker-compose up -d --build
```

Для установки библиотек на Python:
```
pip install -r requirements.txt
```

Для работы сервиса:
```
python main.py 
```

Также среди аргументов можно выбрать:</br>
--load_to_postgres 0 (Default 1) </br>
--load_to_elastic 0 (Default 1) </br>
--find_similar 0 (Default 1) </br>
--file_size 50k (Default 5k) файл 50k.xml должен быть в папке с проектом</br>

Далее прикладываю скриншоты результатов поиска схожих объектов: </br>
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/1.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/2.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/3.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/4.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/5.png?raw=true)
