необходимы: tkinter (на винде по умолчанию), web3

1) кидаем приватники или мнемоники в wallets.txt каждый с новой строки
2) поля ввода:
	swaps: 1 свап = eth -> usd -> eth int
	vol  : сколько гоняет в $, которивки получает сам float
	gas  : сколько ставить газ на свап в $, лучше ставить 0.3 float
	time : в течени какого времени в часах будет выполняться float
3) жмем первый раз, скрипт считает предварительные данные
4) жмем второй раз в течении 5 сек после первого, запускаются свапы


*) если нажать не вводя данные 2 раза, будет работать по старым json конфигурациям

канал: https://t.me/SwissScripts