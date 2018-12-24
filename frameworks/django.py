'''
	Оглавление:

		Установка

		Модели и базы данных

			Один ко многим

			Многие ко многим

			Один к одному

			Связь моделей из разных модулей

			Мета настройки

			Методы модели

			Наследование моделей

			Абстрактные модели

			Multi-table наследование

			Proxy-модели

			Множественное наследование

			Переопределение полей при наследовании

			Создание

			Обновление

			Получение

			Ограничение выборки

			Фильтры

			Фильтры по связанным объектам

			Сравнение одного поля с другим

			Кэширование и QuerySets

			Сложные запросы с помощью объектов Q

			Сравнение объектов

			Удаление

			Копирование объекта

			Агрегация

			Менеджеры

			Использование чистого SQL

			Транзакции

			Использование нескольких баз данных

			Табличные пространства

			Оптимизация работы с базой данных

		Обработка HTTP запросов

			Менеджер URL-ов

			Создание представлений

			Декораторы представлений

			Загрузка файлов

			Вспомогательные функции

			Промежуточный слой (Middleware)

			Как использовать сессии

		Книги

		Развёртывание (docker + nginx + gunicorn + django)
'''

# Установка
'''
	django-admin startproject mysite

	python manage.py startapp polls
'''

# Модели
'''
	Обычно одна модель представляет одну таблицу в базе данных.

	Каждая модель это класс унаследованный от models.Model.

	Атрибут модели представляет поле в базе данных.

	Команды для работы с моделями:

		python manage.py makemigrations

		python manage.py migrate

	Чтобы миграции выполнились нужно подключить приложение в INSTALLED_APPS.

	Каждое поле в вашей модели должно быть экземпляром соответствующего Field класса.

	Поле первичного ключа доступно только для чтения. Если вы поменяете значение первичного ключа для существующего объекта, а зачем сохраните его, будет создан новый объект рядом с существующим.

	Для переопределения первичного ключа просто укажите primary_key=True для одного из полей. При этом Django не добавит поле id.

	Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField, первым аргументом принимает необязательное читабельное название. Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.

	ForeignKey, ManyToManyField и OneToOneField первым аргументом принимает класс модели, поэтому для того чтобы задать имя полю используется keyword аргумент verbose_name.

	Название поля не может быть слово зарезервированное Python.

	Название поля не может содержать несколько нижних подчеркиваний.

	Если ни одно существующее поле не удовлетворяет вашим потребностям, или вам необходимо использовать какие-либо особенности поля, присущие определенной базе данных - вы можете создать собственный тип поля.
'''
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    # позволяет выбирать значение для поля и автоматически создаёт select на его основе
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    first_name = models.CharField(max_length=30)
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name="the related poll",
    )

# Один ко многим
'''
	Для определения связи один ко многим используется models.ForeignKey.

	Для ForeignKey необходимо указать класс связанной модели. Желательно, но не обязательно, чтобы название ForeignKey поля было названием модели в нижнем регистре.

	Для создания рекурсивной связи – объект со связью один ко многим на себя или связь на модель, которая еще не определена, вы можете использовать имя модели вместо класса.
'''
class Manufacturer(models.Model):
    '''
        
    '''
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )

'''
	ForeignKey принимает дополнительные аргументы, которые определяют, как должна работать связь.

	on_delete=models.CASCADE - удаляет объекты, связанные через ForeignKey

	on_delete=models.PROTECT - препятствует удалению связанного объекта 

	on_delete=models.SET_NULL - устанавливает ForeignKey в NULL, возможно только если null равен True

	on_delete=models.SET_DEFAULT - устанавливает ForeignKey в значение по умолчанию, значение по-умолчанию должно быть указано для ForeignKey

	on_delete=models.SET - устанавливает ForeignKey в значение указанное в SET()
'''

# Многие ко многим
'''
	Для определения связи многие-ко-многим, используйте ManyToManyField.

	Для ManyToManyField необходимо указать обязательный позиционный аргумент: класс связанной модели.

	Так же, как и с ForeignKey, вы можете создать рекурсивную связь (объект со связью многие-ко-многим на себя) и связь с моделью, которая еще неопределенна.

	Обычно, ManyToManyField необходимо добавить в модель, которая будет редактироваться в форме. В примере выше, toppings добавлено в Pizza (вместо того, чтобы добавить поле pizzas типа ManyToManyField в модель Topping), потому что обычно думают о пицце с ингредиентами, а не об ингредиентах в различных пиццах. В примере выше, форма для Pizza позволит пользователям редактировать ингредиенты для пиццы.

	Django позволяет определить модель для хранения связи многие-ко-многим и дополнительной информации. Эту промежуточную модель можно указать в поле ManyToManyField используя аргумент through, который указывает на промежуточную модель. В промежуточной модели необходимо добавить внешние ключи на модели, связанные отношением многие-ко-многим. Эти ключи указывают как связаны модели.

	Промежуточная модель должна содержать только одну связь с исходной моделью
'''
class Topping(models.Model):
    pass

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping, through='History')

class History(models.Model):
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

# Один к одному
'''
	Для определения связи один к одному используется OneToOneField.

	Для OneToOneField необходимо указать обязательный позиционный аргумент: класс связанной модели.

	Создаются 2 таблицы. Например таблица с водителями (drivers) и таблица с машинами (cars). У одной машины может быть только один водитель. Соответственно в таблице cars будет поле driver_id.

	Или другой пример, где у ресторана может быть только одно место.
'''
class Place(models.Model):
    name = models.CharField(max_length=50)

class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_pizza = models.BooleanField(default=False)

# Связь моделей из разных модулей
'''
	Для этого, импортируйте связанную модель перед определением главной модели и используйте как аргумент для поля.
'''
from geography.models import ZipCode

class Restaurant(models.Model):
    zip_code = models.ForeignKey(
        ZipCode,
        on_delete=models.SET_NULL,
    )

# Мета настройки
'''
	Дополнительные настройки для модели можно определить через class Meta.
'''
class Car(models.Model):
    number = models.IntegerField()

    class Meta:
        ordering = ['id'] # сортировка
        verbose_name_plural = 'super_cars' # переопределение названия таблицы

# Методы модели
'''
	Методы модели работают с конкретной записью в таблице.

	Это хороший подход для хранения бизнес логики работы с данными в одном месте, то есть в модели.
'''
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    def baby_boomer_status(self):
        if self.birth_date < datetime.date(1945, 8, 1):
            return "Pre-boomer"
        elif self.birth_date < datetime.date(1965, 1, 1):
            return "Baby boomer"
        else:
            return "Post-boomer"

'''
	Методы, которые автоматически добавляются в модель и которые можно переопределить:

	__str__ - использует для отображения объектов в интерфейсе администратора Django и в качестве значения, вставляемого в шаблон, при отображении объекта.

	__eq__ - проверяет объекты, если два объекта содержат одинаковый первичный ключ и являются экземплярами одно класса, тогда они равны.

	__hash__ - использует значение первичного ключа

	get_absolute_url - используется для вычисления урла объекта и интерфейсе администратора для указания ссылки 'показать на сайте', которая приведет к странице отображения объекта. Хорошая практика использовать get_absolute_url() в шаблонах.

	get_foo_display() - для каждого поля, которое содержит choices, объект будет иметь метод get_foo_display(), где foo имя поля. Этот метод возвращает удобное для восприятия название для значения поля.

	Также можно переопределить методы save и delete.
'''
super(Blog, self).save(*args, **kwargs)

# Наследование моделей
'''
	Базовый класс модели должен наследоваться от models.Model.

	Также нужно определить должна ли родительская модель быть независимой моделью (с собственной таблицей в базе данных), или же это просто контейнер для хранения информации, доступной только через дочерние модели.
'''

# Абстрактные модели
'''
	Абстрактные модели удобны при определении общих, для нескольких моделей, полей.

	Для этой модели не будет создана таблица в базе данных.
	
	Если дочерний класс не определяет собственный класс Meta, он унаследует родительский класс Meta. 

	Если дочерняя модель хочет расширить родительский Meta класс, она может унаследовать его. 

	Используя атрибут related_name для ForeignKey или ManyToManyField, вы должны всегда определять уникальное название для обратной связи. Это имя будет использовано вместо field_set в выражении b.field_set.all()
'''
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True

class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

    class Meta(CommonInfo.Meta):
        db_table = 'student_info'

# Multi-table наследование
'''
	Каждая модель будет независимой и 

	Каждая модель имеет собственную таблицу в базе данных и может быть использована независимо. 
	
	Наследование использует связь между родительской и дочерней моделью (через автоматически созданное поле OneToOneField).

	Дочерняя модель не имеет доступа к родительскому классу Meta.
'''
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

# Все поля Place будут доступны и в Restaurant, в то время как данные будут храниться в разных таблицах
class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    class Meta:
    	# Если родительская модель определяет сортировку, но вы не хотите ее наследовать в дочерней модели, вы можете указать это таким способом
    	ordering = []

# Proxy-модели
'''
	Proxy-модели используются для переопределения поведения модели не меняя структуры базы данных.

	Другими словами можно изменить сортировку по-умолчанию или менеджер по умолчанию в proxy-модели, без изменения оригинальной модели.

	Proxy-модели создаются так же, как и обычная модель. Указать что это proxy-модель можно установив атрибут proxy в классе Meta в True.

	Вы не можете унаследоваться от нескольких не абстрактных моделей т.к. proxy-модель не может хранить информации о полях в нескольких таблицах базы данных.

	Proxy-модель может наследоваться от нескольких абстрактных моделей при условии, что они не определяют поля модели.

	Если вы не определите ни один менеджер для proxy-модели, он будет унаследован от родительской модели. 
'''
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

# Модель MyPerson использует ту же таблицу в базе данных, что и класс Person. Также каждый новый экземпляр модели Person` будет доступен через модель MyPerson, и наоборот.
class MyPerson(Person):
    class Meta:
    	ordering = ['last_name']
        proxy = True

    def do_something(self):
        pass

# Множественное наследование
'''
	В большинстве случаев вам не нужно будет использовать множественное наследование. В основном множественное наследование используют для mix-in классов: добавление дополнительных полей и методов для каждой модели унаследованной от mix-in класса. Старайтесь содержать иерархию наследования настолько простой и понятной, насколько это возможно, чтобы не возникало проблем с определением, откуда взялась та или другая информация.
'''

# Переопределение полей при наследовании
'''
	В Python можно переопределять атрибуты класса-родителя в дочернем классе. В Django это запрещено для атрибутов, которые являются экземплярами Field. Если родительская модель имеет поле author, вы не можете создать поле с именем author в дочерних моделях.
'''

# Выполнение запросов
'''
	Класс модели представляет таблицу, а экземпляр модели - запись в этой таблице.

	Чтобы создать объект, нужно создать экземпляр класса модели.
'''
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    comments = models.IntegerField()
    pingbacks = models.IntegerField()
    rating = models.IntegerField()

# Создание
'''
	Чтобы создать объект, создайте экземпляр класса модели, указав необходимые поля в аргументах и вызовите метод save() чтобы сохранить его в базе данных.
'''
b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
b.save()

# Обновление
'''
	Для сохранения изменений в объект, который уже существует в базе данных, используйте save().

	Обновление ForeignKey работает так же, как и сохранение обычных полей, просто назначьте полю объект необходимого типа.

	Обновление ManyToManyField работает немного по-другому, используйте метод add() поля, чтобы добавить связанный объект.

	Метод update() использует непосредственно SQL запрос. Это операция для массового изменения, при этом метод save() модели не будет вызван и сигналы pre_save и post_save не сработают.
'''
b.name = 'New name'
b.save()

# ForeignKey update
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()

# ManyToManyField update
joe = Author.objects.create(name="Joe")
entry.authors.add(joe)

# multiple ManyToManyField update
john = Author.objects.create(name="John")
paul = Author.objects.create(name="Paul")
entry.authors.add(john, paul)

# обновление нескольких объектов, которые соотвествуют условию
Entry.objects.filter(
	pub_date__year=2007
).update(
	headline='Everything is the same'
)

# обновляет все записи в связанном объекте
b = Blog.objects.get(pk=1)
Entry.objects.all().update(blog=b)

# если нужно сохранить каждый объект в QuerySet и удостовериться что метод save() вызван для каждого объекта
for item in my_queryset:
    item.save()

Entry.objects.all().update(pingbacks=F('pingbacks') + 1)

# Получение
'''
	Для получения объектов из базы данных, создается QuerySet через Manager модели.

	QuerySet представляет выборку объектов из базы данных.

	Обратиться к менеджерам можно только через модель и нельзя через ее экземпляр.

	После каждого изменения QuerySet, вы получаете новый QuerySet, который никак не связан с предыдущим QuerySet.

	QuerySets – ленивы, создание QuerySet не выполняет запросов к базе данных, пока QuerySet не вычислен.
'''
Blog.objects.all()

Entry.objects.filter(pub_date__year=2006)

Entry.objects.filter(
	headline__startswith='What'
).exclude(
	pub_date__gte=datetime.date.today()
)

# уникальность QuerySet
q1 = Entry.objects.filter(headline__startswith="What")
q2 = q1.exclude(pub_date__gte=datetime.date.today())
q3 = q1.filter(pub_date__gte=datetime.date.today())

# ленивость QuerySet
q = Entry.objects.filter(headline__startswith="What")
q = q.exclude(pub_date__gte=datetime.date.today())
q = q.filter(pub_date__gte=datetime.date.today())
print(q) # запрос был выполнен только сейчас и только один

# если объекта нет, то выбросит исключение DoesNotExist или MultipleObjectsReturned если запрос вернул больше одной записи
one_entry = Entry.objects.get(pk=1)

# получение объектов по связи один ко многим
e = Entry.objects.get(id=2)
e.blog

b = Blog.objects.get(id=1)
b.entry_set.all()

# получение объектов по связи многие ко многим
e = Entry.objects.get(id=3)
e.authors.all()
e.authors.count()
e.authors.filter(name__contains='John')

a = Author.objects.get(id=5)
a.entry_set.all()

# получение объектов по связи один к одному
class EntryDetail(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
    details = models.TextField()

ed = EntryDetail.objects.get(id=2)
ed.entry

e = Entry.objects.get(id=2)
e.entrydetail

# запросы со связанными объектами (все 3 запроса идентичны)
Entry.objects.filter(blog=b)
Entry.objects.filter(blog=b.id)
Entry.objects.filter(blog=5)

# Ограничение выборки
'''
	Для ограничения результата выборки QuerySet используются срезы. Они эквивалент таких операторов SQL как LIMIT и OFFSET.

	QuerySet возвращает новый QuerySet и запрос не выполняется. Исключением является использовании “шага” в срезе.

	Отрицательные срезы (например, Entry.objects.all()[-1]) не поддерживаются.

	Именованные аргументы функции filter() и др. – объединяются оператором 'AND'.
'''
# возвращает первые 5 объектов
Entry.objects.all()[:5] 

# для получения одного объекта используйте индекс вместо среза
Entry.objects.order_by('headline')[0] 

# Точное совпадение
Entry.objects.get(id__exact=14)


# Фильтры

	# Точное совпадение, регистро-независимое
	Entry.objects.filter(name__iexact='beatles blog')

	# Регистрозависимая проверка на вхождение
	Entry.objects.filter(headline__contains='Lennon')

	# знак % экранировать не нужно
	Entry.objects.filter(headline__contains='%')

	# Регистронезависимая проверка на вхождение
	Entry.objects.filter(headline__icontains='Lennon')

	# Больше чем
	Entry.objects.filter(id__gt=4)

	# Больше чем или равно
	Entry.objects.filter(id__gte=4)

	# Меньше чем
	Entry.objects.filter(id__lt=4)

	# Меньше чем или равно
	Entry.objects.filter(id__lte=4)

	# Регистрозависимая проверка начинается ли поле с указанного значения
	Entry.objects.filter(id__startswith=4)

	# Регистронезависимая проверка начинается ли поле с указанного значения
	Entry.objects.filter(id__istartswith=4)

	# Регистрозависимая проверка оканчивается ли поле с указанного значения
	Entry.objects.filter(id__endswith=4)

	# Регистронезависимая проверка оканчивается ли поле с указанного значения
	Entry.objects.filter(id__iendswith=4)

	# Проверка на вхождение в диапазон (включающий)
	Entry.objects.filter(pub_date__range=(start_date, end_date))

	# Проверка на дату
	Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))

	# Проверяет на IS NULL
	Entry.objects.filter(pub_date__isnull=True)

	# Проверяет на IS NOT NULL
	Entry.objects.filter(pub_date__isnull=False) 

	# Полнотекстовый поиск, который использует преимущества полнотекстового индекса. Работает как и contains но значительно быстрее благодаря полнотекстовому индексу
	Entry.objects.filter(headline__search="+Django -jazz Python")

	# Регистрозависимая проверка регулярным выражением
	Entry.objects.filter(title__regex=r'^(An?|The) +')

	# Регистронезависимая проверка регулярным выражением
	Entry.objects.filter(title__iregex=r'^(an?|the) +')

# Фильтры по связанным объектам
'''
	Для фильтра по полю из связанных моделей, используйте имена связывающих полей разделенных двойным нижним подчеркиванием, пока вы не достигните нужного поля.
'''

# получает все объекты Entry с Blog, name которого равен 'Beatles Blog'
Entry.objects.filter(blog__name='Beatles Blog')

# получает все объекты Blog с Entry, headline которого равен 'Lennon'
Blog.objects.filter(entry__headline='Lennon')

# фильтр через несколько связей
Blog.objects.filter(entry__authors__name='Lennon')

# Фильтрация по связям многие-ко-многим. Для выбора всех блогов, содержащих записи и с 'Lennon' в заголовке и опубликованные в 2008 (запись должна удовлетворять оба условия)
Blog.objects.filter(
	entry__headline__contains='Lennon',
    entry__pub_date__year=2008
)

# Фильтрация по связям многие-ко-многим. Для выбора блогов с записями, у которых заголовок содержит “Lennon”, а также с записями опубликованными в 2008
Blog.objects.filter(
	entry__headline__contains='Lennon'
).filter(
    entry__pub_date__year=2008
)


# Исключения по связям многие-ко-многим. запрос исключит блоги, с записями, у которых заголовок содержит “Lennon”, а также с записями опубликованными в 2008
Blog.objects.exclude(
    entry__headline__contains='Lennon',
    entry__pub_date__year=2008,
)

# Сравнение одного поля с другим
'''
	Django предоставляет класс F для сравнений одного поля с другим. Экземпляр F() рассматривается как ссылка на другое поле модели. Эти ссылки могут быть использованы для сравнения значений двух разных полей одного объекта модели.

	Django поддерживает операции суммирования, вычитания, умножения, деления и арифметический модуль для объектов F(), с константами или другими объектами F()
'''

# выбирает все записи, у которых количество комментариев больше, чем pingbacks. pingbacks это поле в этой же таблице
Entry.objects.filter(comments__gt=F('pingbacks'))

Entry.objects.filter(comments__gt=F('pingbacks') * 2)

# Кэширование и QuerySets
'''
	В только что созданном QuerySet кеш пустой. После вычисления QuerySet будет выполнен запрос к базе данных. После этого Django сохраняет результат запроса в кеше QuerySet и возвращает необходимый результат.

	Последующие вычисления QuerySet используют кеш.

	Если не сохранять результат запроса в переменную, исппользуя при этом срез или индекс, кэш не сработает.
'''

# этот код создаст два экземпляра QuerySet и вычислит их не сохраняя, что увеличит нагрузку (плохой подход)
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])

# используется кэш
queryset = Entry.objects.all()
print([p.headline for p in queryset])
print([p.pub_date for p in queryset]) # здесь уже запрос из кэша

queryset = Entry.objects.all()
print(queryset[5]) # не будет использоваться кэш

queryset = Entry.objects.all()
[entry for entry in queryset]
print(queryset[5]) # будет использоваться кэш

# Сложные запросы с помощью объектов Q
'''
	Если вам нужны более сложные запросы (например, запросы с оператором OR), вы можете использовать объекты Q.

	Объекты Q могут быть объединены операторами & и |, при этом будет создан новый объект Q.

	Если присутствует объект Q, он должен следовать перед именованными аргументами.
'''
Q(question__startswith='Who') | Q(question__startswith='What')

# SELECT * from polls WHERE question LIKE 'Who%' AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')
Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
)

# Сравнение объектов
'''
	Для сравнения двух экземпляров модели, используйте стандартный оператор сравнения ==. При этом будут сравнены первичные ключи.
'''
some_entry == other_entry

# Удаление
'''
	Метод delete() сразу удаляет объект и возвращает количество удаленных объектов, и словарь с количеством удаленных объектов для каждого типа.

	(1, {'weblog.Entry': 1})
'''
b = Blog.objects.get(pk=1)
b.delete()

# удаляет все объекты, которые попадают под условие
Entry.objects.filter(pub_date__year=2005).delete()

Entry.objects.all().delete()

# Копирование объекта
'''
	Для копирования существующего объекта нужно создать новый экземпляр с копией всех полей другого объекта, установить pk в None и сохранить.

	Если используется наследование, то нужно установить pk и id в None.
'''
blog = Blog(name='My blog', tagline='Blogging is easy')
blog.save()
blog.pk = None
blog.save()

django_blog = Blog(name='My blog', tagline='Blogging is easy')
django_blog.save()
django_blog.pk = None
django_blog.id = None
django_blog.save()

# копирование связанных объектов
entry = Entry.objects.all()[0]
old_authors = entry.authors.all()
entry.pk = None
entry.save()
entry.authors = old_authors

# Агрегация
'''
	Django предоставляет два способа использовать агрегацию. Первый способ заключается в использовании агрегации для всех объектов QuerySet, второй для каждого объекта.

	Для вычисления значения для всех объектов используется aggregate, для вычисления значения для каждого объекта используется annotate.
'''

# для вычисления среднего значения для всех объектов, aggregate() завершающая инструкция для QuerySet, которая возвращает словарь с результатом
Book.objects.aggregate(Avg('price')) # {'price__avg': 34.35}

# если нужно вычислить больше одного значения
Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))

# для вычисления значения для каждого объекта, annotate() не завершающая функция и её результатом будет QuerySet, который можно дальше менять
q = Book.objects.annotate(Count('authors'))
q[0].authors__count
q[1].authors__count

# Менеджеры
'''
	Это интерфейс, через который создаются запросы к моделям Django. 

	Каждая модель имеет хотя бы один менеджер.

	По умолчанию Django добавляет Manager с именем objects для каждого класса модели.

	Чтобы переименовать Manager добавьте в класс атрибут, значение которого экземпляр models.Manager()

	Вы можете использовать собственный менеджер.

	Создание своего менеджера может понадобиться в том случае если есть какой то кастомный метод модели, который делает сложный запрос и используется во многих местах. В таком случае мы создаём метод внутри своего менеджера и добавляем этот менеджер в модель. 
'''
class Person(models.Model):
    people = models.Manager() # переименование менеджера


class MyBookManager(models.Manager):
    def get_queryset(self):
        return super(MyBookManager, self).get_queryset().filter(author='Roald Dahl')

    def my_custom_method_hard_query():
    	pass

class Book(models.Model):
    my_objects = MyBookManager() # добавление нового менеджера

# Использование чистого SQL
'''
	Можно использовать Manager.raw() или выполнить запрос напрямую.

	Этот метод принимает чистый SQL запрос, выполняет его, и возвращает экземпляр django.db.models.query.RawQuerySet

	При использовании помнить о экранировании.

	Также следует проявлять осторожность при использовании extra() и RawSQL.

	SQL Запрос переданный в .raw() не проверяется, поэтому сли запрос возвращает не набор записей, вы получите ошибку.

	Хотя RawQuerySet и можно проитерировать как QuerySet, RawQuerySet не предоставляет все методы QuerySet. Например, __bool__() и __len__()

	raw() поддерживает доступ к объекту из набора по индексу.

	Если вам необходимо выполнить запрос с параметрами, используйте аргумент params. Используя params вы полностью защищены от Атак с внедрением SQL-кода.

	Не используйте форматирование строк в запросе!

	Если используется подключение к бд без использования моделей и нужно подключаться к разным базам данных, то можно использовать connections['my_db_alias'].cursor()

	С помощью чистого запроса без моделей можно достучаться до хранимой процедуры - cursor.callproc('test_procedure', [1, 'test'])
'''
Person.objects.raw('SELECT * FROM myapp_person')

Person.objects.raw('SELECT * FROM myapp_person')[0]

name = 'Doe'
Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [name])

# Не используйте форматирование строк в запросе!
query = 'SELECT * FROM myapp_person WHERE last_name = %s' % lname
Person.objects.raw(query)

# Использование без уровня моделей
def my_custom_sql(self):
	with connection.cursor() as cursor:
	    cursor.execute('UPDATE bar SET foo = 1 WHERE baz = 2')
	    row = cursor.fetchone()

    ''' По умолчанию вернётся результат только со значениями, без названия полей. '''

    return row

# Транзакции
'''
	Суть транзакции в том, что она объединяет последовательность действий в одну операцию "всё или ничего". Промежуточные состояния внутри последовательности не видны другим транзакциям, и если что-то помешает успешно завершить транзакцию, ни один из результатов этих действий не сохранится в базе данных.

	Изменения, производимые открытой транзакцией, невидимы для других транзакций, пока она не будет завершена, а затем они становятся видны все сразу.

	По умолчанию Django использует режим автоматической фиксации (autocommit). То есть аждый запрос сразу фиксируется в базе данных.

	При включенном autocommit, если транзакция не активна, каждый SQL запрос обернут в транзакцию. То есть транзакция для каждого запроса не только создается, но и автоматически фиксируется, если запросы был успешно выполнен.

	Если используется транзакция, то при получении запроса Django начинает транзакцию. Если ответ был создан без возникновения ошибок, Django фиксирует все ожидающие транзакции. Если функция представления вызывает исключение, Django откатывает все ожидающие транзакции.

	Вы можете выполнять частичную фиксацию или откат изменений с помощью менеджера контекста atomic().

	Создание транзакции для каждого запроса создает небольшую нагрузку на базу данных.

	Только представления оборачиваются в транзакцию.

	Декоратор @transaction.non_atomic_requests отключает транзакцию для указанного представления.

	Иногда вам необходимо выполнить какие-либо действия связанные с текущей транзакцией в базе данных, но только при успешном коммите транзакции. Это может быть задача Celery, отправка электронного письма, или сброс кэша. Django предоставляет функцию on_commit(), которая позволяет добавить обработчик, вызываемый после успешного коммита транзакции.

	Оказавшись в транзакции, можно зафиксировать выполненные изменения, используя функцию commit(), или отменить их через функцию rollback().
'''
@transaction.atomic # в этом представлении сработает транзакция для каждого действия
def viewfunc(request):
    do_stuff()

def viewfunc(request):
    do_stuff()

    with transaction.atomic(): # использование менеджера контекста с транзакцией
        do_more_stuff()

def viewfunc(request):
    try:
        with transaction.atomic():
            generate_relationships()
    except IntegrityError:
        handle_exception()


def do_something():
    pass

# использования функции если транзакция прошла успешно
transaction.on_commit(do_something)
transaction.on_commit(lambda: some_celery_task.delay('arg1'))

# если будет откат первой транзакции, вторая не сработает
with transaction.atomic():
    transaction.on_commit(foo)

    try:

        with transaction.atomic():
            transaction.on_commit(bar)
            raise SomeError()
    except SomeError:
        pass

try:
	vote = Vote.objects.get(voting=voting, person=person)

	if vote.number_of_votes < voting.limit_votes_for_win:
		with transaction.atomic():
			vote.number_of_votes = F('number_of_votes') + 1
			vote.save()
	else:
		return JsonResponse({'limit_was_reached': True})
except Vote.DoesNotExist:
	vote = Vote(voting=voting, person=person, number_of_votes=1)
	vote.save()


# Использование нескольких баз данных
'''
	Первым шагом к использованию нескольких баз данных с Django будет определение серверов БД, которые вы планируете использовать.

	Это выполняется с помощью параметра конфигурации DATABASES.

	Этот параметр привязывает к базам данных псевдонимы, по которым эти базы будут доступны в Django и словари параметров с характеристиками подключения к ним.

	Базам данных можно назначать любой псевдоним. Тем не менее, псевдоним default имеет особое значение. Django использует базу данных с псевдонимом default, если явно не указано использование другой базы данных.

	Вы должны настроить DATABASE_ROUTERS для всех моделей ваших приложений, включая те, которые расположены в сторонних приложениях, чтобы ни один запрос не был отправлен в стандартную базу.

	Команда migrate работает единовременно только с одной базой данных. По умолчанию, она работает с базой данных default, но добавив аргумент --database, вы можете указать команде, что надо работать с другой базой данных.

		./manage.py migrate

		./manage.py migrate --database=users

	Простейшим способом использования нескольких баз данных является настройка схемы роутинга.

	Стандартная схема роутинга проверяет, что если база данных не указана, то все запросы направляются к базе данных default.

	Для активации стандартной схемы роутинга делать ничего не надо. Она уже настроена для каждого проекта Django.

	Кастомные роутеры можно использовать, указав в настройке DATABASE_ROUTERS, которая находится в setting.py

	Порядок применения кастомных роутеров имеет важное значение. Роутеры вызываются в порядке, в котором они перечислены в параметре конфигурации DATABASE_ROUTERS.
'''
# Должно находиться в settings.py
DATABASES = {
    'default': {
        'NAME': 'app_data',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'postgres_user',
        'PASSWORD': 's3krit'
    },
    'users': {
        'NAME': 'user_data',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'priv4te'
    }
}

Author.objects.using('default').all() # метод using позволяет выбрать базу данных
Author.objects.using('users').all()
my_object.save(using='users')

# Перемещение объекта между базами данных
p = Person(name='Fred')
p.save(using='default')
p.save(using='users')


'''
	Этот пример показывает как можно использовать роутеры для управления несколькими БД. В нем намеренно игнорируются некоторые проблемы такой конфигурации, основная цель - продемонстрировать возможности роутеров.
'''
DATABASES = {
    'default': {},
    'author': {
        'NAME': 'author_db',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'swordfish',
    },
    'book': {
        'NAME': 'primary',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql_user',
        'PASSWORD': 'spam',
    }
}

# Данный роутер шлёт запросы от приложения author в базу данных author_db
class AuthorRouter(object):
    def db_for_read(self, model, **hints):
    	"""
			Выбирает базу данных, которая должна использоваться для операций чтения
    	"""
        if model._meta.app_label == 'author':
            return 'author_db'
        return None

    def db_for_write(self, model, **hints):
        """
        	Выбирает базу данных, которая должна использоваться для операций записи
        """
        if model._meta.app_label == 'author':
            return 'author_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        	Возвращает True, если связь между obj1 и obj2 должна быть разрешена, 
        	Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'author' or obj2._meta.app_label == 'author':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        	Определяет должна ли выполняться миграция
        """
        if app_label == 'author':
            return db == 'author_db'
        return None

# Данный роутер шлёт запросы от приложения book в базу данных book_db
class BookRouter(object):
	# Елюбую дополнительную информацию, которая может помочь в выборе базы данных можно посмотреть в словаре hints
    def db_for_read(self, model, **hints):
    	"""
			Выбирает базу данных, которая должна использоваться для операций чтения
    	"""
        if model._meta.app_label == 'book':
            return 'book_db'
        return None

    def db_for_write(self, model, **hints):
        """
        	Выбирает базу данных, которая должна использоваться для операций записи
        """
        if model._meta.app_label == 'book':
            return 'book_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        	Возвращает True, если связь между obj1 и obj2 должна быть разрешена, 
        	Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'book' or obj2._meta.app_label == 'book':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        	Определяет должна ли выполняться миграция
        """
        if app_label == 'book':
            return db == 'book_db'
        return None

# В settings.py
DATABASE_ROUTERS = ['path.to.AuthRouter', 'path.to.PrimaryReplicaRouter']

Author.objects.get(username='fred') # сделает запрос к бд author_db

Book.objects.all() # сделает запрос к бд book_db


# Табличные пространства
'''
	Используются для оптимизации производительности бд.

	Предполагают создание табличных пространст для распределения данных по дискам.

	Django не создаёт табличные пространства для вас. Пожалуйста, обратитесь к документации на вашу базу данных насчёт подробностей по созданию и управлению табличными пространствами.

	Для таблицы, созданной по модели, может быть указано табличное пространство с помощью атрибута db_tablespace внутри класса Meta. 

	Атрибут db_tablespace также имеет влияние на таблицы, которые автоматически создаются для ManyToManyField полей в модели.
	
	Вы можете использовать параметр конфигурации DEFAULT_TABLESPACE для указания значения по-умолчанию для атрибута db_tablespace.

	PostgreSQL и Oracle поддерживают табличные пространства. SQLite и MySQL не поддерживают.

	При использовании бэкэнда, который не обеспечивает поддержку табличных пространств, Django будет игнорировать все атрибуты для табличных пространств.
'''

'''
	В данном примере, таблицы, созданные для модели TablespaceExample будут размещены в табличном пространстве tables.
'''
class TablespaceExample(models.Model):
    name = models.CharField(max_length=30, db_index=True, db_tablespace="indexes")
    data = models.CharField(max_length=255, db_index=True)
    edges = models.ManyToManyField(to="self", db_tablespace="indexes")

    class Meta:
        db_tablespace = "tables"

# Оптимизация работы с базой данных
'''
	Определяем какие запросы выполняются и как быстро

		django-debug-toolbar

		from django.db import connection
		connection.queries)

	Определяем нагрузку на сервер с момощью Zabbix (бесплатный, можно мониторить rabbit) или New Relic (платный)

	Все советы ниже могут и не сработать в вашем случае, или даже понизить производительность.

	Используем индексы.

	Используем правильные типы полей.

	Понимаем QuerySets:

		QuerySets ленивый

		когда происходит вычисление QuerySets

		как данные загружаются в память

	Кэширование всего QuerySet.

	Кэширование значения атрибутов в объектах ORM.

	Для использования кэширования в QuerySet можно использовать шаблонный тэг with.

	Если очень много объектов, кэширование в QuerySet может использовать большой объем памяти. В этом случае может помочь iterator().

	Выполнять задачи базы данных в базе данных, а не в Python:
	
		использовать filter и exclude для фильтрации данных в БД

		использовать объект F() для фильтрации по другим полям модели

		ипользовать annotate для выполнения агрегации в базе данных

	Использовать RawSQL (если это необходимо)

	Использовать SQL (если возможностей моделей или RawSQL недостаточно)

	При выборке использовать уникальное или проиндексированное поле.

	Загружайте все данные сразу, если уверены, что будете использовать их. Обращение несколько раз к базе данных для получения различных частей одного “массива” данных обычно менее эффективно, чем получение всех данных одним запросом. Это особенно важно для запросов, выполняемых в цикле, что может привести к большому количеству запросов.

	Использовать QuerySet.select_related() и prefetch_related() в коде представлений и менеджерах.

	Не получать данные, которые не нужны. Для этого использовать QuerySet.values() и values_list()

	Использовать defer() и only(), если есть колонки в базе данных, которые не будут использованы. Если все же использовать потом эти колонки, то ORM сделает дополнительный запрос для их получения, что уменьшит производительность.

 	Используйте QuerySet.count() вместо len(queryset)

 	QuerySet.exists() вместо if queryset

 	Вместо загрузки данных в объекты, изменения значений и отдельного их сохранения использовать QuerySet.update() и delete(), помнить отсутствие сигналов

 	Используйте значения ключей непосредственно

 		Плохо: entry.blog.id

 		Хорошо: entry.blog_id
	
	Не сортировать данные, если вам это не требуется, потому что сортировка требует ресурсы. Добавление индекса в вашу базу данных может улучшить производительность операции сортировки.

	Используйте общее добавление.

	При создании объектов, если возможно, используйте метод bulk_create() чтобы сократить количество SQL запросов.

		Плохо:

			Entry.objects.create(headline="Python 3.0 Released")
			Entry.objects.create(headline="Python 3.1 Planned")

			my_band.members.add(me)
			my_band.members.add(my_friend

		Хорошо:

			Entry.objects.bulk_create([
			    Entry(headline="Python 3.0 Released"),
			    Entry(headline="Python 3.1 Planned")
			])
	
			my_band.members.add(me, my_friend)
'''

# Менеджер URL-ов
'''
	Определяются в файле urls.py для каждого приложения.

	Как Django обрабатывает запрос:

		Django определяет какой корневой модуль URLconf использовать. Обычно, это значение настройки ROOT_URLCONF

		Django загружает модуль конфигурации URL и ищет переменную urlpatterns

		Django перебирает каждый URL-шаблон по порядку, и останавливается при первом совпадении с запрошенным URL-ом

		После этого Django импортирует и вызывает соответствующее представление, которое является функцией или классом

		В представление передаются объект HttpRequest, позиционные аргументы (если они были в урле)

		Если совпадение не найдено, то Django вызывает соответствующий обработчик ошибок

	В урлах не нужно добавлять косую черту в начале, потому что каждый URL содержит её.

	Символ 'r' вначале урла говорит о том, что строка сырая и ничего в строке не должно быть экранировано.

	URLconf использует запрашиваемый URL как обычную строку Python. Он не учитывает параметры GET, POST и имя домена, поэтому все запросы будут обработаны одним представлением при одинаковом URL.

	Например, при запросе к https://www.example.com/myapp/, URLconf возьмет myapp/

	Каждый найденный аргумент передается в представление как строка.

	Если Django не может найти подходящий шаблон по урлу, то Django вызовет соответствующее представление обрабатывающее ошибку.

	Эти представления определены в четырёх переменных (handler400, handler403, handler404, handler500)

	Django предоставляет инструменты для получения URL-ов в различных компонентах фреймворка:

		В шаблонах это тег url - {% url 'url-name' v1 v2 %}

		Или такой вариант в шаблоне - <a href="{{ object.get_absolute_url }}">Go</a>

		В коде это функция reverse() - reverse('url-name')

		В моделях метод get_absolute_url(). Django использует get_absolute_url() в интерфейсе администратора. Если объект содержит этот метод, страница редактирования объекта будет содержать ссылку "Показать на сайте".

	При выборе названия для URL-шаблона, убедитесь что оно достаточно уникально. Мы советуем использовать myapp-comment вместо comment.
'''
urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:pk>/', views.article_list),
]

# В любой момент, ваш urlpatterns может включать и другие модули URLconf
urlpatterns = [
    path('contact/', include('django_website.contact.urls'))
]

# Функция path может принимать третий необязательный элемент. Этот элемент является словарем и аргументом для функции представления
urlpatterns = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
]

#  Можно передать дополнительные аргументы в include(). При этом, каждый URL-шаблон включенного URLconf будет дополнен этими аргументами
urlpatterns = [
    path('blog/', include('inner'), {'blog_id': 3}),
]

# Именование урла
urlpatterns = [
    path('articles/<int:year>/', views.year_archive, name='news-year-archive'),
]

# Создание представлений
'''
	Представление – это функция Python, которая принимает Web-запрос и возвращает Web-ответ.

	Ответом может быть HTML-содержимое страницы, или перенаправление, или 404 ошибка, или XML-документ, или изображение или ещё что то.

	Код представления принято держать его в файле views.py для каждого приложения.

	Название функции представления может быть каким угодно.

	В ответ представление может вернуть ошибку. Для этого в Django доступны подклассы, например HttpResponseNotFound.

	Если используем исключение Http404, то для переопределение страницы, которую возвращает Django нужно создать шаблон с названием 404.html в корне каталога с шаблонами.

	Представления обрабатывающие ошибки можно переопределить - handler404 = 'mysite.views.my_custom_page_not_found_view'
'''
def current_datetime(request):
    now = datetime.datetime.now()
    return HttpResponse(html)

# Для возвращения ошибок можно использовать встроенные исключения. Они сразу генерирует готовую html страницу.
def create(request):
	try:
		Poll.objects.get(pk=poll_id)
	except Poll.DoesNotExist:
		raise Http404('Poll does not exist')

# Декораторы представлений
'''
	Декораторы могут быть использованы для ограничения доступа к представлению в зависимости от типа запроса И возвращают HttpResponseNotAllowed.

	require_GET() - допустимы только GET запросы

	require_POST() - допустимы только POST запросы

	require_safe() - допустимы только GET и HEAD запросы

	Декораторы могут быть использованы для управления кэширования определенных представлений.

	Декораторы могут управлять сжатием ответа представления.
'''
@require_http_methods(['GET', 'POST'])
def my_view(request):
    pass

# Загрузка файлов
'''
	Когда Django обрабатывает загрузку файла, данные о нем в конце концов попадают в request.FILES

	Данные из формы будут доступны в request.FILES['file']

	request.FILES будет содержать данные только при POST запросе и если тег <form> содержит enctype="multipart/form-data"

	Использование ModelForm значительно упрочает процесс загрузки файла, потому что он сохраняется по указанному в аргументе upload_to поля FileField пути, при вызове form.save()

	Например, если ImageField назван mug_shot, вы можете получить URL к файлу в шаблоне используя {{ object.mug_shot.url }}

	Имя файла, сохраненного на диске, не будет доступно, пока объект к которому относится файл не будет сохранен.

	Когда пользователь загружает файл, Django передает содержимое файла в обработчик загрузки.

	Обработчики загрузки по умолчанию определенны в настройке FILE_UPLOAD_HANDLERS (settings.py).

	MemoryFileUploadHandler - обработчик, который загружает небольшие файлы в память 

	TemporaryFileUploadHandler - обработчик, загружает большие файлы на диск.

	Вы можете написать собственный обработчик загрузки файлов.

	Иногда различные представления требуют различной обработки файлов. В таких случаях можно переопределять обработчики загрузки на лету, изменив request.upload_handlers

		request.upload_handlers.insert(0, ProgressBarUploadHandler())
'''
class UploadFileForm(forms.Form):
	# Если используется бэкенд FileSystemStorage, значение upload_to будет добавлено к MEDIA_ROOT в котором определён путь
    file = forms.FileField(upload_to='uploads')

def upload_file(request):
    if request.method == 'POST':
    	# При работе с файлами и формой передаём файлы в форму 
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
    	# chunks(), вместо использования read(), обезопасит вас от нагрузки системы при загрузке большого файла.
        for chunk in f.chunks():
            destination.write(chunk)

# Вспомогательные функции
'''
	Пакет django.shortcuts содержит вспомогательные функции

	render - выполняет указанный шаблон с переданным словарем контекста и возвращает HttpResponse с полученным содержимым.

	render_to_response - выполняет указанный шаблон с переданным словарем контекста и возвращает HttpResponse с полученным содержимым.

	redirect - перенаправляет на URL указанный через аргументы.

	get_object_or_404 - вызывает get() для переданной модели и возвращает полученный объект, если объект не существует, то вызывает исключение Http404 вместо DoesNotExist. Вместо модели можно передать объект QuerySet.

	get_list_or_404 - возвращает результат метода filter() для переданной модели, вызывает Http404 если получен пустой список.
'''
render(request, template_name='myapp/index.html', context={"foo": "bar"}...)

render_to_response('myapp/index.html', {"foo": "bar"}...)

redirect('url-name', foo='bar')

get_object_or_404(MyModel, pk=1)

get_list_or_404(MyModel, published=True)

# Промежуточный слой (Middleware)
'''
	Это промежуточный слой между запросом и представлением.

	Каждый компонент промежуточного слоя отвечает за определенный функционал.

	Чтобы подключить промежуточный слой, добавьте его в список MIDDLEWARE_CLASSES в settings.py

	Django не требует никаких промежуточных слоёв для своей работы, но настоятельно рекомендуется использовать хотя бы CommonMiddleware.

	Порядок MIDDLEWARE_CLASSES важен, так как один промежуточный слой может зависеть от другого.

	Во время обработки запроса, перед вызовом представления, Django применяет промежуточные слои в порядке указанном в MIDDLEWARE_CLASSES.

	На этом этапе доступны 2 функции:

		process_request() - вызывается для каждого запроса перед тем, как Django решит какое представление вызывать

		process_view() - вызывается перед вызовом представления

	На этапе обработки ответа, после вызова представления, промежуточные слои применяются в обратном порядке, снизу вверх. Это значит, что классы, указанные в конце MIDDLEWARE_CLASSES, будет выполнены в первую очередь.

	На этом этапе доступны 3 функции:

		process_exception() - сработает если представление вызвало исключение

		process_template_response() - вызывается после выполнение представления, если объект ответа содержит метод render()

		process_response() - вызывается для каждого ответа перед тем, как он будет оптравлен браузеру.

	Промежуточные слои могут работать и с потоковыми ответами.

	Возможно исключать некоторые промежуточные слои на лету. Это можно сделать с помощью в методе __init__ с помощью исключения MiddlewareNotUsed.

	Класс промежуточного слоя не должен наследоваться от другого класса.

	Большое кол-во промежуточных слоёв отрицательно влияет на скорость работы приложения.
'''
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
]

# Как использовать сессии
'''
	Механизм сессии сохраняет данные на сервере и самостоятельно управляет сессионными куками.

	Куки содержат ID сессии, а не сами данные.

	Чтобы активировать сессии нужно подключить SessionMiddleware.

	Если сессии не нужны, то можно удалить SessionMiddleware и это немного повысит производительность.

	По умолчанию, Django хранит сессии в базе данных.

	Если вы хотите использовать базу данных для хранения сессии, укажите 'django.contrib.sessions' в настройке INSTALLED_APPS и выполните manage.py migrate, чтобы добавить таблицу в базу данных.

	Для улучшения производительности вы можете использовать кэш для хранения сессии.

	Вам следует использовать кэш только при использовании Memcached. Кэш в памяти не хранит данные достаточно долго, и лучше использовать файлы или базу данных для сессии, чем каждый раз обращаться к кэшу в файловой системе или базе данных.
'''
















# Книги
'''
	Django design patterns

	Two scoope...
'''

# Развёртывание (docker + nginx + gunicorn + django)
'''
	Local machine
	
		cd /etc

		sudo nano hosts

		Add 127.0.0.1 yetbetter

	Nginx (docker)

		docker run -p 80:80 --name nginx -v ~/nginx:/usr/share/nginx/html -d nginx

		docker exec -it container_name bash

		apt-get update

		apt-get install nano

		nano /etc/nginx/nginx.conf (docker container)

			user  nginx;
			worker_processes  1;

			error_log  /var/log/nginx/error.log warn;
			pid        /var/run/nginx.pid;

			events {
			    worker_connections  1024;
			}

			http {
			    access_log  /var/log/nginx/access.log;

			    sendfile on;

			    keepalive_timeout 65;

			    upstream app_servers {
			        server 172.17.0.1:8000; - ip адрес докера на локальной машине (только через него можно достучаться)
			    }

			    server {
			        listen 80;
			        server_name yetbetter;

			        location / {
			            root /usr/share/nginx/html; - здесь должен быть путь к нормальной статики django (узнать) 
			            index index.html index.htm;
			            proxy_pass http://app_servers;
			            proxy_set_header Host $host;
			        }
			    }
			}

		http://yetbetter

	Gunicorn + Django (docker)

		docker pull ubuntu (если нет этого образа на локальной машине, для проверки docker ps)

		docker run -i -t -p 8000:8000 --name container_name ubuntu

			exit

		docker ps -l -> contaner_id/container_name

		docker start container_id

		docker exec -it container_name bash

		apt-get update

		apt-get install -y python3-pip

		pip3 install virtualenv

		pip3 install virtualenvwrapper

		export WORKON_HOME=~/.virtualenvs

		VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'

		source /usr/local/bin/virtualenvwrapper.sh

		which python3

		mkvirtualenv -p /usr/bin/python3 venv_name

		workon venv_name

		pip3 install django

		cd /home

		mkdir /app

		django-admin startproject project_name

		pip3 install gunicorn

		cd django_project_name

		gunicorn -b 0.0.0.0:8000 project_name.wsgi

'''

@transaction.atomic
def first(self):
    ...
    with transaction.atomic:
        second()