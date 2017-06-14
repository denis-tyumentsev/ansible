## Порядок развертывания систем
---

1.Сгенерировать конфигурационные файлы из xml темплейтов.

```sh
$ ./generate.sh <input> <inventory>
```
`<input>`, XML файл с DNS и IP новых хостов, находится в /var/ftp/pub/

`<inventory>`, произвольное имя для новой конфигурации, создает директорию с конфиг. файлами `/home/ansible/ansible/inventories/<inventory>`

Скрипт создает два файла.

Файл с новыми hostname для выполнения ролей на этих серверах, /home/ansible/ansible/inventories/<inventory>/hosts.

Файл с переменными и новыми IP и hostname для заполнения конфиг файлов ролей из темплейтов ролей, `/home/ansible/ansible/inventories/group_vars/all.yml`

При внесении изменений в файл hosts и all.yml также надо изменить темплейты для генерирования новых конфигов:

`/home/ansible/ansible/inventory_gen/templates/all.yml.j2`

`/home/ansible/ansible/inventory_gen/templates/hosts.j2`

ПРИМЕР:
```sh
$ cd /home/ansible/ansible/inventory_gen/ && ./generate.sh /var/ftp/pub/TESTAPP2.xml mytest
```

2.Выполнить развертывание систем из ролей

Порядок выполнения и название ролей указаны в `/home/ansible/ansible/make_configs.yml`

Выполняется под пользователем ansible.
```sh
$ ssh ansible@uds-deploy.moscow.eurochem.ru
```
Для выполнения всех ролей и настройки всех систем:
```sh
$ ansible-playbook -i /home/ansible/ansible/inventories/mytest/hosts  /home/ansible/ansible/make_configs.yml
```
Для проверки статуса всех систем можно использовать тэг `status`:
```sh
$ ansible-playbook -i /home/ansible/ansible/inventories/mytest/hosts /home/ansible/ansible/make_configs.yml --tags status
```
Для выполнения одной роли:
```sh
$ ansible-playbook -i /home/ansible/ansible/inventories/mytest/hosts  /home/ansible/ansible/make_configs.yml -l flow
```
Для тестовой проверки отработки роли без внесения изменений в файлы:
```sh
$ ansible-playbook -i /home/ansible/ansible/inventories/mytest/hosts  /home/ansible/ansible/make_configs.yml -l flow --check
```
---
---
При изменении конфига системы необходимо внести изменения в темплейты конфигов ролей.

Например, конфиг для FLOW:
```sh
$ /home/ansible/ansible/roles/flow/templates/flow/flow.conf.j2
```
---
---
Для перезагрузки сервисов рекомендуется делать include handler:
```sh
$ /home/ansible/ansible/roles/common/handlers/services.yml
```
Это решает конфликт с перезапуском и проверкой статуса сервиса после редактирования конфига, т.к.
handlers отрабатывают ПОСЛЕ выполнения всех задач роли `task/main.yml`.

При этом, в самой роли в `vars/main.yml` задается массив с названиями сервисов.

