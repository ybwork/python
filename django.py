'''
	Оглавление:

		Модели:

		Один ко многим

		Многие ко многим

		Один к одному

		Связь моделей из разных модулей

		Мета настройки

		Менеджер модели

		Методы модели

		Наследование моделей

		Абстрактные модели

		Multi-table наследование

		Proxy-модели

		Множественное наследование

		Переопределение полей при наследовании

		Выполнение запросов:

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

		Агрегация (min/max, count, avg)

		Транзакции
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
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES) # позволяет выбирать значение для поля и автоматически создаёт select на его основе
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
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )

class Manufacturer(models.Model):
    pass

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

# Менеджер модели
'''
	Менеджер модели - это интерфейс, через который Django выполняет запросы к базе данных и получает объекты. Если собственный Manager не указан, название по умолчанию будет objects.
'''

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