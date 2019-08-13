джокеры, wildcard, glob-подстановки, символы групповых операций - это всякие спецсимволы при поиске, типа *.txt



*  0 или более символов
	*	все файлы в каталоге
	rm libby*.*	libby1.jpg, libby2.jpg, ..., libby12.jpg, libby1.txt
	ls -d /etc/g*	все конфиги, начинающиеся с g
	
?	один любой символ
	rm libby1?.jpg	libby10.jpg, libby11.jpg, libby12.jpg, но не libby1.jpg

[]	один любой символ из набора
	rm libby[12].jpg		libby1.jpg, libby2.jpg
	rm libby[6-8].jpg		libby6.jpg, libby7.jpg, libby8.jpg
	[Cc]hange[Ll]og
	ls /etc/[0-9]*		все файлы в /etc, начинающиеся с десятичной цифры
	ls /tmp/[A-Za-z]*	все файлы в /tmp, начинающиеся с латинской буквы
	rm myfile[!9]		удалит все файлы myfile плюс один символ, кроме myfile9

Glob-шаблоны разворачиваются только если совпадают с объектами файлвой системы! В противном случае остаются нетронутыми и буквально передаются в вызов программы.
При использовании таких символов в команде надо заключать их в одинарные кавычки:
echo '[fo]*' > /tmp/mynewfile.txt
Glog-подстановки это НЕ регулярки!

Нюанс:
rm -rf .*/* - удаляет файлы, начинающиеся с точки; но! указанному критерию удовлетворяет и .. так что файлы удалятся и в каталоге выше!