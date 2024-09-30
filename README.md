Для тестирования использовался укороченный yml файл, в котором 5000 объектов, ввиду технических ограничений и желания ускорить процесс, ОДНАКО итерационная загрузка и обработка данных реализована даже в нем (в коде указан batch_size 1000), так что запуск большого файла исключительно вопрос времени. </br> </br>
Для запуска контейнеров postgres и elastic search:
```
docker-compose up -d --build
```

Для установки библиотек на Python:
```
pip install -r requirements.txt
```

Для парсинга файла и загрузки его в postgres:
```
python upload_to_postgres.py
```

Для загрузки данных в ElasticSearch и поиска похожих объектов:
```
python fetch_and_find_similar.py
```
</br>

Далее прикладываю скриншоты результатов поиска схожих объектов: </br>
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/1.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/2.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/3.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/4.png?raw=true)
![alt text](https://github.com/insuperabilez/testovoe/blob/main/images/5.png?raw=true)
