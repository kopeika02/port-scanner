# port-scanner

Многопоточный сканер TCP-портов с определением служб по баннерам. Написан на Python.
A multi-threaded TCP port scanner that identifies services via banners. Written in Python.

## Запуск 
## Usage

python portScanner.py localhost -s 1 -e 1024 -b

## Параметры
## Parameters

-s, -e: диапазон портов, -t: таймаут, -w: число потоков, -b: показывать баннеры
-s, -e: port range, -t: timeout, -w: number of threads, -b: display banners

## Важно
## Important

Только для обучения. Сканируйте свои системы или те, на которые есть письменное разрешение.
For educational purposes only. Only scan your own systems or systems for which you have written permission.