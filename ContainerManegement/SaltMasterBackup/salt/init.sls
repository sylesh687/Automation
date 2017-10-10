apache2:
  pkg.installed:
    - name : {{ salt['pillar.get']('webserver:name') }}
    - refresh : {{ salt['pillar.get']('webserver:value') }}
  
  service.running:
    - reload: True
    - enable: True

add_repo:
  pkgrepo.managed:
   - name : deb http://ppa.launchpad.net/ondrej/php/ubuntu xenial main
   - file: /etc/apt/sources.list.d/ondrej-ubuntu-php-xenial.list

php:
  pkg.installed:
    - refresh: True
    - skip_verify: True
    - pkgs:
      - php7.0
      - libapache2-mod-php7.0
      - php7.0-mbstring
      - php7.0-curl
      - php7.0-zip
      - php7.0-gd
      - php7.0-mysql
      - php7.0-mcrypt
      - curl
      - php-apcu
      - php-curl
      - php-fpm
      - php-gd
      - php-gmp
      - php-json
      - php-mbstring
      - php-pgsql
      - php-readline
      - php-xml
      - php-zip
      - php-mysql


clone:
  git.latest:
    - name: https://github.com/cachethq/Cachet.git
    - rev: v2.3.12
    - target: /var/www/html/Cachet
    - force_clone: True

fcgi:
  cmd.run:
    - name: 'a2enmod proxy_fcgi setenvif'
    - user: root
    - cwd: /var/www/html/Cachet/

php7.1-fpm:
  cmd.run:
    - name: 'a2enconf php7.1-fpm'
    - user: root
    - cwd: /var/www/html/Cachet/

a2enmod:
  cmd.run:
    - name: 'a2enmod rewrite'
    - user: root
    - cwd: /var/www/html/Cachet/

/var/www/html/Cachet/:
  file.directory:
    - user: www-data
    - group: www-data
    - file_mode: 774
    - dir_mode: 755
    - mkdirs: True
    - recurse:
      - user
      - group

/etc/apache2/sites-available/:
  file.directory:
    - user: www-data
    - group: www-data
    - mode: 755

config_files_1:
  
  file.managed:
    - name: /var/www/html/Cachet/.env
    - user: www-data
    - group: www-data
    - mode: 755
    - replace: True
    - source: salt://.env

config_files_2:
  file.managed:
    - name: /etc/apache2/sites-available/cachet.conf
    - source: salt://cachet/cachet.conf
    - template: jinja
    - user: www-data
    - group: www-data
    - mode: 777
    - replace: True

symlink:
  file.symlink:
    - name: /etc/apache2/sites-enabled/cachet.conf
    - target: /etc/apache2/sites-available/cachet.conf
    - user: www-data
    - force: True

get-composer:
  cmd.run: 
    - name: 'curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin  --filename=composer'
    - unless: test -f /usr/local/bin/composer
  pkg.installed:
    - pkgs:
      - composer

set-env:
  environ.setenv:
    - name: COMPOSER_HOME
    - value: /usr/local/bin/
    - update_minion: True

install-composer:
  cmd.run:
   - name: 'composer install --no-dev -o'
   - user: www-data
   - cwd: /var/www/html/Cachet/

generate-key:
  cmd.run:
   - name: 'php artisan key:generate'
   - user: www-data
   - cwd: /var/www/html/Cachet/

app_install:
  cmd.run:
    - name: 'php artisan app:install'
    - user: www-data
    - cwd: /var/www/html/Cachet/

service:
  service.running:
    - name: apache2
    - reload: True
