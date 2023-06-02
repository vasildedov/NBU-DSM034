# NBU-DSM034

Формулировка на задачата:
1. Създайте система, която да зарежда модел за МО по ваш избор и предоставя REST набор от методи за работа с нея и в частност за прогнозиране. Имате свобода в избора на протокол и параметри на методите.

Системата трябва да издава адекватни грешки при некоректно подадени данни, при прогнозирането и др.

2. Създайте докерфайл, който да инсталира всички необходими зависимости (библиотеки, модели, source code) за системата и при създаване на снимка (image) от докервайла да може да се запускат контейнери чрез създадената система.


Задачата беше решена в Windows 11.

След навигиране в command prompt/еквивалента му в други ОС до правилната директория, в която се намират качените тук файлове, потребителя следва да изпълни main.py файла:

``` bash
python main.py
```

След което потребителя веднага може да отвори нов command prompt в който да получи достъп до модела чрез следната команда:

``` bash
curl -X POST -H "Content-Type: application/json" -d "{\"alcohol\": 13.75, \"malic_acid\": 1.73, \"ash\": 2.41, \"alcalinity_of_ash\": 16.0, \"magnesium\": 89.0, \"total_phenols\": 2.6, \"flavanoids\": 2.76, \"nonflavanoid_phenols\": 0.29, \"proanthocyanins\": 1.81, \"color_intensity\": 5.6, \"hue\": 1.15, \"od280_od315_of_diluted_wines\": 2.9, \"proline\": 1320.0}" http://localhost:5000/predict
```

Kомандата ползва curl за да прати POST заявка до endpoint-a на FastAPI, http://localhost:5000/predict, като входните данни са в JSON формат. Отговорът на сървъра в случая е: 
"{"linear_regression_prediction":0,"random_forest_prediction":0}"

Алтернативно, prediction_request_json.py има същата функционалност.

За да се построи fastapi-app от Docker, следната команда се ползва в command prompt:
``` bash
docker build -t fastapi-app .
```
Той ползва Dockerfile и requirements.txt където има списък с библиотеките, които са нужни за да се ползват моделите. Следната команда може да се ползва за да се провери, че е зареден fastapi-app:

``` bash
docker image ls
```

За да се зареди image-а на локален сървър, се ползва:
``` bash
docker run -p 5000:5000 --rm fastapi-app
```
След това може да се повтори същата процедура за ползването на модела за правене на prediction-и с curl или prediction_request_json.py.

По следния начин може да се ползва minikube за същото:

``` bash
minikube start
minikube docker-env
docker image save fastapi-app:latest | minikube ssh docker load
kubectl apply -f fastapi-deployment.yaml
minikube service fastapi-deployment
```
Последователно се случва следното:
1. Стартира се minikube
2. Конфигурира се локалния Docker да може да комуникира с Docker daemon в minikube 
3. Docker image fastapi-app се зарежда в minikube
4. Ползва се deployment.yaml файла за да се създаде FastAPI deployment в Minikube
5. URL-а на FastAPI service се зарежда. Дадения URL може да се ползва накрая на curl кода или с prediction_request_json.py като се смени URL-a
