CREATE TABLE IF NOT EXISTS users (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id bigint(20) DEFAULT NULL,
  chat_id bigint(20) DEFAULT NULL,
  tg_name text,
  user_msg text,
  phone bigint(20) DEFAULT NULL,
  category int(11) DEFAULT NULL,
  bitrix_uid int(11) DEFAULT NULL,
  bitrix_user_name text,
  bitrix_user_last_name text,
  page_num text,
  PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS tasks (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_is int(11) DEFAULT NULL,
  bitrix_id int(11) DEFAULT NULL,
  task_id int(11) DEFAULT NULL,
  task_date datetime DEFAULT NULL,
  PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS marks (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_id int(11) DEFAULT NULL,
  vote text,
  vote_date datetime DEFAULT NULL,
  bitrix_id int(11) DEFAULT NULL,
  comment text,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS categories (
    `id` int NOT NULL AUTO_INCREMENT,
    `cat_name` text,
    `cat_descr` text,
    `cat_type` text,
    `sla` int DEFAULT NULL,
    PRIMARY KEY (`id`)
);

INSERT INTO hd_bot.categories (cat_name,cat_descr,cat_type,sla) VALUES
	 ('Установка и настройка ПО','В данном разделе можно подать заявку на установку и/или настройку дополнительного программного обеспечения','tech_sup',24),
	 ('Настройка электронной почты','В данном разделе можно подать заявку на консультацию и настройку электронной почты. Предоставление доступа к корпоративной электронной почте.','tech_sup',16),
	 ('Доступ к информационным системам и сервисам','В данном разделе можно подать заявку на предоставление доступа к внутренним и внешним сервисам, порталам, папкам, VPN','tech_sup',24),
	 ('Доступ к интернет и WiFi','В данном разделе можно подать заявку на настройку работы беспроводной и проводной сети','tech_sup',8),
	 ('Печать и копирование','В данном разделе можно подать заявку на восстановение доступа к сервису печати','tech_sup',24),
	 ('Ремонт и настройка оборудования','В данном разделе можно подать заявку на ремонт и настройку оборудования','tech_sup',24),
	 ('Выдача, установка, перемещение оборудования','В данном разделе можно подать заявку на оснащение рабочего места: монитор, гарнитура, телефон и т.д.','tech_sup',24),
	 ('Выдача SIM карты','В данном разделе можно подать заявку на предоставление корпоративной мобильной связи (услуга доступна только для руководителей)','tech_sup',24),
	 ('Техническое сопровождение мероприятий','В данном разделе можно подать заявку для организации видеосовещаний. Просьба формировать заявку за 3-4 дня до проведения мероприятия.','tech_sup',24),
	 ('Система контроля и управления доступом','В данном разделе можно подать заявку на предоставление/восстановление доступа на территорию Института или маршрутизация заявки ответственному исполнителю','tech_sup',8);


CREATE TABLE IF NOT EXISTS bitrix_data (
	id INT(11) NOT NULL auto_increment,
	buid INT(11),
	name TEXT,
	last_name TEXT,
	active TEXT,
	mobile TEXT,
	tg_name TEXT,
	PRIMARY KEY (id))
