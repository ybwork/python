'''
	Оглавление

		Что это

		Отложенное выполнение задач

		Повторное выполнение команд

		Замена cron-a

		Роутинг

		Canvas
'''

# Что это
'''
	Celery - это инструмент, который позволяет выполнять задачи в фоновом режиме. Или распределённая очередь задач

	Использовать всё в одном процессе веб-сервера это плохая идея, потому что время отклика приложения будет долгим

	Если нет обмена задачами между приложениями, то можно использовать только Celery

	Если задача простая, то лучше использовать что-нибудь полегче, чем Celery

	Более простая альтернатива Celery это RQ
'''