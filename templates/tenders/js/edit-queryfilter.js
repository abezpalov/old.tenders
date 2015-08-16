{% if perms.catalog.add_queryfilter or perms.tenders.change_queryfilter %}

var queryfilter = new Object()

{% endif %}

{% if perms.catalog.add_queryfilter %}

// Открытие окна создания
$("body").delegate("[data-do='open-new-queryfilter']", "click", function(){

	// Заполняем значение полей
	$('#modal-edit-queryfilter-header').text('Добавить фильтр запроса');
	$('#edit-queryfilter-id').val('0');
	$('#edit-queryfilter-name').val('');
	$('#edit-queryfilter-state').prop('checked', true);
	$('#edit-queryfilter-public').prop('checked', false);

	// Открываем модальное окно
	$('#modal-edit-queryfilter').foundation('reveal', 'open');
	return false;
});

{% endif %}

{% if perms.tenders.change_queryfilter %}

// Открытие окна редактирования
$("body").delegate("[data-do='open-edit-queryfilter']", "click", function(){

	// Получаем информацию о загрузчике
	$.post("/tenders/ajax/get-queryfilter/", {
		queryfilter_id: $(this).data('id'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {
			if ('success' == data.status){

				// Заполняем значение полей
				$('#modal-edit-queryfilter-header').text('Редактировать фильтр запроса');
				$('#edit-queryfilter-id').val(data.queryfilter['id']);
				$('#edit-queryfilter-name').val(data.queryfilter['name']);

				queryfilter.regions   = data.queryfilter['regions'];
				queryfilter.customers = data.queryfilter['customers'];
				queryfilter.owners    = data.queryfilter['owners'];
				queryfilter.okveds    = data.queryfilter['okveds'];
				queryfilter.okpds     = data.queryfilter['okpds'];
				queryfilter.words     = data.queryfilter['words'];

				$('#edit-queryfilter-regions-in').prop('checked', data.queryfilter['regions_in']);
				$('#edit-queryfilter-customers-in').prop('checked', data.queryfilter['customers_in']);
				$('#edit-queryfilter-owners-in').prop('checked', data.queryfilter['owners_in']);
				$('#edit-queryfilter-okveds-in').prop('checked', data.queryfilter['okveds_in']);
				$('#edit-queryfilter-okpds-in').prop('checked', data.queryfilter['okpds_in']);
				$('#edit-queryfilter-words-in').prop('checked', data.queryfilter['words_in']);

				$('#edit-queryfilter-state').prop('checked', data.queryfilter['state']);
				$('#edit-queryfilter-public').prop('checked', data.queryfilter['public']);

				// Открываем окно
				$('#modal-edit-queryfilter').foundation('reveal', 'open');

			} else {

				// Показываем сообщение с ошибкой
				var notification = new NotificationFx({
					wrapper : document.body,
					message : '<p>' + data.message + '</p>',
					layout : 'growl',
					effect : 'genie',
					type : data.status,
					ttl : 3000,
					onClose : function() { return false; },
					onOpen : function() { return false; }
				});
				notification.show();
			}
		}
	}, "json");

	return false;
});


{% endif %}

{% if perms.catalog.add_queryfilter or perms.tenders.change_queryfilter %}


// Сохранение
$("body").delegate("[data-do='edit-queryfilter-save']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/save-queryfilter/", {
		queryfilter_id:      $('#edit-queryfilter-id').val(),
		queryfilter_name:    $('#edit-queryfilter-name').val(),
		queryfilter_state:   $('#edit-queryfilter-state').prop('checked'),
		queryfilter_public:  $('#edit-queryfilter-public').prop('checked'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			// Показываем сообщение
			var notification = new NotificationFx({
				wrapper: document.body,
				message: '<p>' + data.message + '</p>',
				layout:  'growl',
				effect:  'genie',
				type:    data.status,
				ttl:     3000,
				onClose: function() { return false; },
				onOpen:  function() { return false; }
			});
			notification.show();

			if ('success' == data.status){

				// Обновлем информацию на странице
				$("[data-queryfilter-name='" + $('#edit-queryfilter-id').val() + "']").text($('#edit-queryfilter-name').val());
				$("[data-queryfilter-state='" + $('#edit-queryfilter-id').val() + "']").prop('checked', $('#edit-queryfilter-state').prop('checked'));
				$("[data-queryfilter-public='" + $('#edit-queryfilter-id').val() + "']").prop('checked', $('#edit-queryfilter-public').prop('checked'));

				if ('0' == $('#edit-queryfilter-id').val()) {

					// Закрываем окно
					$('#modal-edit-queryfilter').foundation('reveal', 'close');

					// Обновляем страницу
					setTimeout(function () {location.reload();}, 3000);

				} else {

					// Закрываем окно
					$('#modal-edit-queryfilter').foundation('reveal', 'close');

					// Заполняем значение полей
					$('#edit-queryfilter-id').val('0');
					$('#edit-queryfilter-name').val('');
					$('#edit-queryfilter-state').prop('checked', true);
					$('#edit-queryfilter-public').prop('checked', false);
				}
			}
		}
	}, "json");

	return false;
});


// Отмена редактирования
$("body").delegate("[data-do*='edit-queryfilter-cancel']", "click", function(){

	// Заполняем значение полей
	$('#edit-queryfilter-id').val('0');
	$('#edit-queryfilter-name').val('');
	$('#edit-queryfilter-state').prop('checked', true);
	$('#edit-queryfilter-public').prop('checked', false);

	// Закрываем окно
	$('#modal-edit-queryfilter').foundation('reveal', 'close');

	return false;
});

{% endif %}

{% if perms.tenders.change_queryfilter %}


// Смена статуса
$("body").delegate("[data-do='switch-queryfilter-state']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/switch-queryfilter-state/", {
		queryfilter_id:      $(this).data('id'),
		queryfilter_state:   $(this).prop('checked'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			// Показываем сообщение
			var notification = new NotificationFx({
				wrapper: document.body,
				message: '<p>' + data.message + '</p>',
				layout:  'growl',
				effect:  'genie',
				type:    data.status,
				ttl:     3000,
				onClose: function() { return false; },
				onOpen:  function() { return false; }
			});
			notification.show();
		}
	}, "json");

	return true;
});


// Смена статуса "публичности"
$("body").delegate("[data-do='switch-queryfilter-public']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/switch-queryfilter-public/", {
		queryfilter_id:      $(this).data('id'),
		queryfilter_public:  $(this).prop('checked'),
		csrfmiddlewaretoken: '{{ csrf_token }}'
	},
	function(data) {
		if (null != data.status) {

			// Показываем сообщение
			var notification = new NotificationFx({
				wrapper: document.body,
				message: '<p>' + data.message + '</p>',
				layout:  'growl',
				effect:  'genie',
				type:    data.status,
				ttl:     3000,
				onClose: function() { return false; },
				onOpen:  function() { return false; }
			});
			notification.show();
		}
	}, "json");

	return true;
});


// Открытие/закрытие ветви категорий ОКПД
$("body").delegate("[data-do='switch-li-okpd-status']", "click", function(){
	if ($(this).data('state') == 'closed') {

		okpd_id = $(this).data('id')

		// Получаем дочерние объекты с сервера
		$.post("/tenders/ajax/get-okpd-childrens/", {
			okpd_id:             $(this).data('id'),
			csrfmiddlewaretoken: '{{ csrf_token }}'
		},
		function(data) {
			if (null != data.status) {

				if ('success' == data.status){

					html_data = ""

					for(i = 0; i < data.okpds.length; i++) {
						li = "<li>"
						if (data.okpds[i].childs_count > 0) {
							li = li + '<i data-do="switch-li-okpd-status" data-id="' + data.okpds[i]['id'] + '" data-state="closed" class="fa fa-plus-square-o"></i>'
						} else {
							li = li + '<i class="fa fa-circle-thin"></i>'
						}
						li = li + '<a data-do="select-okpd" data-id="' + data.okpds[i]['id'] + '" data-okpd="' + data.okpds[i]['id'] + '">'
						li = li + '<span>' + data.okpds[i]['code'] + '</span>'
						li = li + '<span>' + data.okpds[i]['name'] + '</span>'
						li = li + '</a>'
						if (data.okpds[i].childs_count > 0) {
							li = li + '<ul id="okpd-' + data.okpds[i]['id'] + '-childs"></ul>'
						}

						li = li + '</li>'

						html_data = html_data + li;
					}

					$('#okpd-' + okpd_id + '-childs').html(html_data);

				} else {
					var notification = new NotificationFx({
						wrapper: document.body,
						message: '<p>' + data.message + '</p>',
						layout: 'growl',
						effect: 'genie',
						type: data.status,
						ttl: 3000,
						onClose: function() { return false; },
						onOpen: function() { return false; }
					});
					notification.show();
				}
			}
		}, "json");

		$(this).parent("li").removeClass('closed');
		$(this).parent("li").addClass('opened');
		$(this).removeClass('fa-plus-square-o');
		$(this).addClass('fa-minus-square-o');
		$(this).data('state', 'opened');

	} else {
		$(this).parent("li").removeClass('opened');
		$(this).parent("li").addClass('closed');
		$(this).removeClass('fa-minus-square-o');
		$(this).addClass('fa-plus-square-o');
		$(this).data('state', 'closed');
	}
	return false;
});


// Поиск по справочнику ОКПД
$("body").delegate("[data-do='okpds-search']", "keypress", function(e){
	var search_text = $(this).val().toLowerCase();
	var key         = e.which;

	if(key == 13) {

		// Если в строке поиска пусто, показываем полный каталог
		if (search_text == '') {
			$("[data-content='okpds-search-result']").addClass('hidden');
			$("[data-content='okpds-catalog']").removeClass('hidden');
			$("[data-content='okpds-search-result']").html('');
		// Иначе, прячем каталог и показываем результаты поиска
		} else {
			$("[data-content='okpds-search-result']").removeClass('hidden');
			$("[data-content='okpds-catalog']").addClass('hidden');

			// Получаем объекты с сервера
			$.post("/tenders/ajax/search-okpds/", {
				search_text:         search_text,
				csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			function(data) {
				if (null != data.status) {

					if ('success' == data.status){

						html_data = ""

						if (data.okpds.length > 0) {
							for(i = 0; i < data.okpds.length; i++) {
								li = '<li>'
								li = li + '<a data-do="select-okpd" data-id="' + data.okpds[i]['id'] + '" data-okpd="' + data.okpds[i]['id'] + '">'
								li = li + '<span>' + data.okpds[i]['code'] + '</span>'
								li = li + '<span>' + data.okpds[i]['name'] + '</span>'
								li = li + '</a></li>'
								html_data = html_data + li;
							}
						} else {
							html_data = '<li class="alert-box secondary radius">Ничего не найдено.</li>'
						}
						$("[data-content='okpds-search-result']").html(html_data);

					} else {
						var notification = new NotificationFx({
							wrapper: document.body,
							message: '<p>' + data.message + '</p>',
							layout: 'growl',
							effect: 'genie',
							type: data.status,
							ttl: 3000,
							onClose: function() { return false; },
							onOpen: function() { return false; }
						});
						notification.show();
					}
				}
			}, "json");
		}
	}
});


// Открытие/закрытие ветви категорий ОКВЭД
$("body").delegate("[data-do='switch-li-okved-status']", "click", function(){
	if ($(this).data('state') == 'closed') {

		okved_id = $(this).data('id')

		// Получаем дочерние объекты с сервера
		$.post("/tenders/ajax/get-okved-childrens/", {
			okved_id:            $(this).data('id'),
			csrfmiddlewaretoken: '{{ csrf_token }}'
		},
		function(data) {
			if (null != data.status) {

				if ('success' == data.status){

					html_data = ""

					for(i = 0; i < data.okveds.length; i++) {
						li = "<li>"
						if (data.okveds[i].childs_count > 0) {
							li = li + '<i data-do="switch-li-okved-status" data-id="' + data.okveds[i]['id'] + '" data-state="closed" class="fa fa-plus-square-o"></i>'
						} else {
							li = li + '<i class="fa fa-circle-thin"></i>'
						}
						if (data.okveds[i]['code']) {
							li = li + '<span>' + data.okveds[i]['code'] + '</span>'
						}
						li = li + '<span>' + data.okveds[i]['name'] + '</span>'
						if (data.okveds[i].childs_count > 0) {
							li = li + '<ul id="okved-' + data.okveds[i]['id'] + '-childs"></ul>'
						}

						li = li + '</li>'

						html_data = html_data + li;
					}

					$('#okved-' + okved_id + '-childs').html(html_data);

				} else {
					var notification = new NotificationFx({
						wrapper: document.body,
						message: '<p>' + data.message + '</p>',
						layout: 'growl',
						effect: 'genie',
						type: data.status,
						ttl: 3000,
						onClose: function() { return false; },
						onOpen: function() { return false; }
					});
					notification.show();
				}
			}
		}, "json");

		$(this).parent("li").removeClass('closed');
		$(this).parent("li").addClass('opened');
		$(this).removeClass('fa-plus-square-o');
		$(this).addClass('fa-minus-square-o');
		$(this).data('state', 'opened');

	} else {
		$(this).parent("li").removeClass('opened');
		$(this).parent("li").addClass('closed');
		$(this).removeClass('fa-minus-square-o');
		$(this).addClass('fa-plus-square-o');
		$(this).data('state', 'closed');
	}
	return false;
});


// Поиск по справочнику ОКВЭД
$("body").delegate("[data-do='okveds-search']", "keypress", function(e){
	var search_text = $(this).val().toLowerCase();
	var key         = e.which;

	if(key == 13) {

		// Если в строке поиска пусто, показываем полный каталог
		if (search_text == '') {
			$("[data-content='okveds-search-result']").addClass('hidden');
			$("[data-content='okveds-catalog']").removeClass('hidden');
			$("[data-content='okveds-search-result']").html('');
		// Иначе, прячем каталог и показываем результаты поиска
		} else {
			$("[data-content='okveds-search-result']").removeClass('hidden');
			$("[data-content='okveds-catalog']").addClass('hidden');

			// Получаем объекты с сервера
			$.post("/tenders/ajax/search-okveds/", {
				search_text:         search_text,
				csrfmiddlewaretoken: '{{ csrf_token }}'
			},
			function(data) {
				if (null != data.status) {

					if ('success' == data.status){

						html_data = ""

						if (data.okveds.length > 0) {
							for(i = 0; i < data.okveds.length; i++) {
								li = '<li><span>' + data.okveds[i]['code'] + '</span><span>' + data.okveds[i]['name'] + '</span></li>'
								html_data = html_data + li;
							}
						} else {
							html_data = '<li class="alert-box secondary radius">Ничего не найдено.</li>'
						}
						$("[data-content='okveds-search-result']").html(html_data);

					} else {
						var notification = new NotificationFx({
							wrapper: document.body,
							message: '<p>' + data.message + '</p>',
							layout: 'growl',
							effect: 'genie',
							type: data.status,
							ttl: 3000,
							onClose: function() { return false; },
							onOpen: function() { return false; }
						});
						notification.show();
					}
				}
			}, "json");
		}
	}
});

{% endif %}
