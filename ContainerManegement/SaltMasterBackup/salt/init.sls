apache2:
  pkg.installed:
    - name : {{ salt['pillar.get']('webserver:name') }}
    - refresh : {{ salt['pillar.get']('webserver:value') }}
  
  service.running:
    - reload: True
    - enable: True


php:
  pkg.installed:
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
a2enmod:
  cmd.run:
    - name: 'a2enmod rewrite'
    - user: www-data
    - group: www-data

clone:
  git.latest:
    - name: https://github.com/cachethq/Cachet.git
    - rev: v2.3.12
    - target: /var/www/html/Cachet
    - force_clone: True


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
    - user: www-data
    - group: www-data
    - mode: 777
    - replace: True
    - source: salt://cachet.conf

symlink:
  file.symlink:
    - name: /etc/apache2/sites-available/cachet.conf
    - target: /etc/apache2/sites-enabled/cachet.conf
    - user: www-data
    - force: True

get-composer:
  cmd.run: 
    - name: 'curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin  --filename=composer'
    - unless: test -f /usr/local/bin/composer
  pkg.installed:
    - pkgs:
      - composer
      - php-xml

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
