{% if perms.catalog.add_queryfilter %}

// Открытие окна редактирования категории (новая)
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


// Смена статуса "публичнсоти"
$("body").delegate("[data-do='switch-queryfilter-public']", "click", function(){

	// Отправляем запрос
	$.post("/tenders/ajax/switch-queryfilter-public/", {
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


{% endif %}
