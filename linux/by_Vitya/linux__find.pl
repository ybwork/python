find
Поиск
find . -name "*my*"         # найти от текущей директории и ниже
find /etc -name "*my*"      # найти в директории /etc
find . -iname "*my*"        # регистронезависимый поиск
По размеру
file . -size +10M       # файлы больше 10 мегабайт (-10 - меньше десяти)
                        # [bckMG] - 512-блоки, байты, килобайты, мегабайты, гигабайты
По типу
find . -type d          # найти все каталоги
                        # f - файл, d - каталог, l - симлинк, остальное - редко используется
Группировка
find . -name "*functional*" -a -type d    # (AND) найти все каталоги с маской "*functional*"
find . -size +10M -o -size 10M            # (OR) найти файлы 10 и больше Мб
find -n \( -name "*mp3" \)                # (NOT) найти все кроме mp3-файлов
find . \( -name "*mp3" -o -name "*ogg" \) -a -type f    # найти все файлы mp3 и ogg
Разное
find . -name "*mp3" -a -type -f | wc -l		# подсчитать количество mp3-файлов
 
 
find . -user shadowuser     # найти файлы пользователя shadowuser
find . -group web           # найти файлы, принадлежащие группе web
 
 
find . -name "*MP3" -exec rename 's/MP3/mp3/g' {} \;    # выполнить действие над каждым найденным файлом
find . -name "*my*" -fprint myfile.txt                  # вывод результатов в файл
