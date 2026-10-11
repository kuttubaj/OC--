# Практическая работа № 1. Установка Linux и знакомство с терминалом
**ФИО:** [Ваши Фамилия Имя]
**Уровень:** Вариант B

## 1. Создание пользователей и настройка прав
**Команды создания пользователя и группы:**
`sudo groupadd developers`
`sudo adduser student2`
`sudo usermod -aG developers student2`

**Создание каталога и настройка прав доступа:**
`sudo mkdir -p /srv/shared`
`sudo chown root:developers /srv/shared`
`sudo chmod 775 /srv/shared`

## 2. Проверка прав на удаление
**Создание файла от имени student2:**
`su - student2`
`touch /srv/shared/testfile.txt`
`exit`

**Попытка удалить файл от имени основного пользователя (iskak):**
`iskak@AserNitro:~$ rm /srv/shared/testfile.txt`
`rm: remove write-protected regular empty file '/srv/shared/testfile.txt'? y`
`rm: cannot remove '/srv/shared/testfile.txt': Permission denied`

**Объяснение:** Файл удалить не получилось, потому что в Linux право на удаление зависит от папки, а не от самого файла. Папка `/srv/shared` принадлежит `root` и группе `developers`. Мой пользователь (`iskak`) в эту группу не входит, поэтому у меня есть права только на чтение папки, а прав на запись (и удаление) в нее нет.

## 3. Разница между su и sudo. Блокировка root
* **su** — полностью переключает на другого пользователя. При этом нужно вводить пароль того, к кому заходишь.
* **sudo** — дает права админа только на одну конкретную команду. Тут нужно вводить свой собственный пароль.
* **Почему root заблокирован:** Ради безопасности. Во-первых, никто не сможет подобрать пароль от главного админа, потому что пароля просто нет. Во-вторых, чтобы случайно не сломать систему — для любых системных изменений приходится осознанно писать `sudo`.

## 4. Настройка ~/.bashrc
В конец файла `~/.bashrc` были добавлены следующие строки (одна переменная и два алиаса):
`export OS_COURSE="Linux is awesome"`
`alias c='clear'`
`alias update='sudo apt update'`

**Проверка работы в новой сессии:**
`iskak@AserNitro:~$ echo $OS_COURSE`
`Linux is awesome`

`iskak@AserNitro:~$ update`
`[sudo] password for iskak:` 
`Hit:1 http://archive.ubuntu.com/ubuntu ...`

Созданные алиасы проверены: сокращение `c` очищает экран терминала, а `update` запускает обновление списков пакетов.